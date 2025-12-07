import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # PostgreSQL settings
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
    # Kafka settings
    KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "")
    KAFKA_GROUP = os.getenv("KAFKA_GROUP", "")
    # Session timeout and output
    SESSION_TIMEOUT_SECONDS = int(os.getenv("SESSION_TIMEOUT_SECONDS", 1800))
    BATCH_OUTPUT_DIR = os.getenv("BATCH_OUTPUT_DIR", "output")
    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
