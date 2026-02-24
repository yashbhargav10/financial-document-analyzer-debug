## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

verification = Task(
    description="Verify the uploaded document using the provided tools. Check if it's a valid financial document. Query context: {query}",
    expected_output="A confirmation of whether the document is a genuine financial document or not.",
    agent=verifier,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False
)

analyze_financial_document = Task(
    description="Extract key insights from the financial document and answer the user query: {query}.",
    expected_output="A detailed financial analysis report highlighting the main trends, figures, and market insights.",
    agent=financial_analyst,
    tools=[search_tool, FinancialDocumentTool().read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="Provide sound investment recommendations based on the previous financial analysis. User query: {query}",
    expected_output="A well-reasoned set of investment recommendations and portfolio strategies.",
    agent=investment_advisor,
    async_execution=False,
)

risk_assessment = Task(
    description="Identify and assess any risks associated with the financial insights and investment strategies proposed. User query: {query}",
    expected_output="A robust risk assessment report outlining potential downsides and mitigation strategies.",
    agent=risk_assessor,
    async_execution=False,
)