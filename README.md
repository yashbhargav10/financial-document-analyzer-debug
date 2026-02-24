# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirement.txt
```

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

**Note:** Current `data/sample.pdf` is a placeholder - replace with actual Tesla financial document for proper testing.

# You're All Not Set!
🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code in each file and understand the expected behavior. There is a bug in each line of code. So be careful.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights

---

## Developer Log: Bug Fixes & Enhancements

The following improvements were made to complete the assignment:

### 1. CrewAI & AI Agent Bug Fixes
* **`agents.py`**: Rewrote agent definitions to eliminate hallucination-heavy or unprofessional system prompts. Assigned high-quality roles and goals fitting for financial advisors. Fixed the `llm=llm` undefined variable issue by instantiating `ChatOpenAI` and passing the instance to explicitly set the LLM and the API Key from the `.env` file environment. 
* **`task.py`**: Overhauled task descriptions to follow a logical and professional Crew workflow. The tasks now map correctly to `verification`, `analyze_financial_document`, `investment_analysis`, and `risk_assessment`. Added proper inputs via the `{query}` template so the user prompt and document path map smoothly.
* **`tools.py`**: Removed the buggy mock PDF class. Fully implemented the `read_data_tool` using `PyPDF2` via the official `@tool` class decorator, enabling true text extraction from uploaded financial PDFs.
* **`main.py`**: Restructured the entry point to import all tasks and agents properly into the `Crew` initialization. Fixed the `run_crew` execution method so it injects the target `file_path` properly into the context mapping for the agents. Replaced the `uvicorn.run(app...)` with `uvicorn.run("main:app"...)` to resolve the fastAPI reload syntax error.

### 2. Bonus Features
* **Asynchronous Queue Worker Model**: Modified `main.py` so the `POST /analyze` endpoint utilizes `FastAPI BackgroundTasks`. Large analysis jobs run fully detached, keeping the main process unblocked and snappy.
* **Database Integration**: Added `database.py` with SQLAlchemy to track analysis jobs in a SQLite database (`financial_analysis.db`). 
* **Status Endpoint**: Created a `GET /status/{task_id}` endpoint to query the execution status of a background job submitted to the new queue (returns `pending`, `completed`, or `failed` with the report data).

### 3. Testing & Code Quality
* **Tests**: Added a test suite using `pytest` located in `tests/test_main.py` to verify the application's endpoints.
* **Tox Config**: Created a `tox.ini` config file to automate test suite requirements configuration.
* **Docstrings**: Formatted all Python files to include detailed class-level and function-level docstrings, improving overall maintenance and readability.
