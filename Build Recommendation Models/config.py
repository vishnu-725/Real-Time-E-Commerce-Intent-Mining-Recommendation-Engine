
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI") or (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER','postgres')}:"
    f"{os.getenv('POSTGRES_PASSWORD','postgres')}@"
    f"{os.getenv('POSTGRES_HOST','localhost')}:"
    f"{os.getenv('POSTGRES_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB','ecom')}"
)

OUTPUT_DIR = os.getenv("PHASE3_OUTPUT_DIR", "./phase3_output")
