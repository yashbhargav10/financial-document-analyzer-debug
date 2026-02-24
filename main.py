"""
Main FastAPI application for Financial Document Analyzer.

This module provides the API endpoints for analyzing financial documents,
utilizing a Queue Worker Model and a SQLite database to handle concurrent
requests smoothly and store the results.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid
from typing import Optional

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment

from database import SessionLocal, AnalysisResult, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf") -> str:
    """
    To run the whole crew to analyze the provided financial document.
    
    Args:
        query (str): The user's query context.
        file_path (str): The path to the uploaded PDF.
        
    Returns:
        str: The consolidated analysis result from the Crew execution.
    """
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
    )
    
    augmented_query = f"Target document file path: {file_path}\\nUser query: {query}"
    result = financial_crew.kickoff(inputs={'query': augmented_query})
    return str(result)

def process_analysis_task(task_id: str, query: str, file_path: str):
    """
    Background worker function that runs the CrewAI logic asynchronously.
    Updates the database with the result or any error.
    
    Args:
        task_id (str): The UUID of the database task record.
        query (str): The user's query.
        file_path (str): The file path where the PDF is stored.
    """
    db = SessionLocal()
    task_record = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    if not task_record:
        db.close()
        return
        
    try:
        response = run_crew(query=query.strip(), file_path=file_path)
        task_record.status = 'completed'
        task_record.result = str(response)
    except Exception as e:
        task_record.status = 'failed'
        task_record.result = str(e)
    finally:
        db.commit()
        db.close()
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass  # Ignore cleanup errors

@app.get("/")
async def root():
    """Health check endpoint to verify that the API is running."""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_api(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Submit a financial document for analysis queue.
    
    Args:
        background_tasks (BackgroundTasks): Injected dependency for queuing jobs.
        file (UploadFile): PDF document file.
        query (str): Instructions for the analysts.
        
    Returns:
        dict: A acknowledgment object detailing the status, query, and task_id.
    """
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Validate query
    if query == "" or query is None:
        query = "Analyze this financial document for investment insights"
    
    # Create DB entry with pending status
    db = SessionLocal()
    db_task = AnalysisResult(
        id=file_id, 
        query=query, 
        file_name=file.filename, 
        status='pending'
    )
    db.add(db_task)
    db.commit()
    db.close()
    
    # Add to background tasks (Queue Worker Model)
    background_tasks.add_task(process_analysis_task, file_id, query, file_path)
    
    return {
        "status": "queued",
        "task_id": file_id,
        "message": "The document has been queued for analysis. Use /status/{task_id} to check results.",
        "file_processed": file.filename
    }

@app.get("/status/{task_id}")
async def get_analysis_status(task_id: str):
    """
    Retrieve the status and results of a queued analysis task.
    
    Args:
        task_id (str): The UUID of the analysis task.
        
    Returns:
        dict: Status object mapping to database values.
    """
    db = SessionLocal()
    task_record = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    db.close()
    
    if not task_record:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return {
        "task_id": task_record.id,
        "status": task_record.status,
        "file_name": task_record.file_name,
        "query": task_record.query,
        "result": task_record.result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)