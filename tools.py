import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @tool("Read Financial Document")
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path
        
        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.
            
        Returns:
            str: Full Financial Document file
        """
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            full_report = ""
            for count, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_report += text + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("Analyze Investment")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """Processes and analyzes financial document data for investments."""
        processed_data = financial_document_data
        
        # Clean up the data format
        processed_data = processed_data.replace("  ", " ")
                
        return f"Investment analysis for data: {processed_data[:100]}..."

## Creating Risk Assessment Tool
class RiskTool:
    @tool("Risk Assessment")
    def create_risk_assessment_tool(financial_document_data: str) -> str:        
        """Assesses risk from financial document data."""
        return f"Risk assessment for data: {financial_document_data[:100]}..."