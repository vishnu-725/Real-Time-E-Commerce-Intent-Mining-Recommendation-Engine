from sqlalchemy import create_engine, text
import pandas as pd
from config import Config

# Create SQLAlchemy engine using the database URI from config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

def read_sql(query: str):
    """
    Execute a SQL query and return a pandas DataFrame.
    """
    return pd.read_sql(query, engine)

def execute_sql(query: str):
    """
    Execute a SQL command (INSERT/UPDATE/DELETE/DDL) using the engine.
    """
    with engine.begin() as conn:
        conn.execute(text(query))
