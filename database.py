from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./financial_analysis.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AnalysisResult(Base):
    """Database model for storing financial analysis results."""
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, index=True)
    query = Column(String)
    file_name = Column(String)
    status = Column(String) # 'pending', 'completed', 'failed'
    result = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)
