from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# load environment variable
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": SSL_CA_PATH
        }
    }
)

def load_data_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        
        jobs = []
        for row in result.all():
            jobs.append(dict(row._mapping))
        return jobs
    
def load_job_info(job_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), {"val" : job_id})

        row = result.mappings().fetchone()

        return dict(row) if row else None
