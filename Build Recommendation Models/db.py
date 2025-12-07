
from sqlalchemy import create_engine, text
import pandas as pd
from config import DB_URI

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DB_URI, future=True)
    return _engine

def read_sql(query: str, params: dict = None) -> pd.DataFrame:
    """
    Read SQL into pandas DataFrame.
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

def execute_sql(query: str, params: dict = None):
    """
    Execute non-select SQL (DDL/insert/update).
    """
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(query), params or {})
