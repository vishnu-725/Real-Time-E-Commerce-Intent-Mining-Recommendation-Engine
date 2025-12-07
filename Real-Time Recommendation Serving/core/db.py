from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine: Engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def execute_sql(sql: str, params: dict = None):
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        conn.commit()
    return result

def read_sql(sql: str, params: dict = None):
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return result.fetchall()
