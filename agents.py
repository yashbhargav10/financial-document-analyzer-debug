## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI

from tools import search_tool, FinancialDocumentTool

# Explicitly initialize the LLM to ensure the API key is picked up
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.environ.get("OPENAI_API_KEY"))

# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="Provide incredibly accurate analysis of financial data and give well-reasoned investment advice to solve the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You're a seasoned financial analyst with decades of experience working for top tier investment banks."
        "You adhere to strict regulatory compliance and base all your insights firmly on hard data from financial documents."
        "You pride yourself on your ability to extract meaningful trends from complex financial statements."
    ),
    tools=[search_tool, FinancialDocumentTool().read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Carefully verify if the provided document is a genuine financial document. Strictly ensure only valid financial data is analyzed.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert compliance officer and auditor. Your job is to meticulously check any document uploaded to the system."
        "If a document is lacking proper financial context or is just a random text, you accurately flag it."
        "Your attention to detail ensures the analysis remains highly accurate and compliant."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Professional Investment Advisor",
    goal="Based on verified financial analysis, recommend prudent, well-balanced investment strategies.",
    verbose=True,
    backstory=(
        "You are a fiduciary investment advisor known for putting client interests first."
        "You rely exclusively on detailed financial reports and market realities to guide your recommendations."
        "You never engage in risky speculation and always ensure your advice is well-founded and heavily diversified."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Senior Risk Management Analyst",
    goal="Objectively evaluate and quantify the potential risks associated with the financial insights and suggest mitigation strategies.",
    verbose=True,
    backstory=(
        "You are a risk assessor with a background in actuarial science and institutional risk management."
        "Your strength lies in spotting both obvious and hidden risks in market conditions and company fundamentals."
        "You never overstate risks for drama, but you ensure every investor is fully informed of potential downsides."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)
