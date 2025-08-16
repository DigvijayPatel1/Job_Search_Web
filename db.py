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

#connecting with the database
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": SSL_CA_PATH
        }
    }
)

#getting the jobs data form the database
def load_data_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        
        jobs = []
        for row in result.all():
            jobs.append(dict(row._mapping))
        return jobs
    
#getting the spaecific data form the database whose id is defined
def load_job_info(job_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), {"val" : job_id})

        row = result.mappings().fetchone()

        return dict(row) if row else None
    

# load the user data to the database
def load_user_info(data):
    print("DEBUG: inserting ->", data)
    with engine.begin() as conn:  # auto-commit
        query = text("INSERT INTO user (email, password) VALUES (:email, :password)")
        result = conn.execute(query, {"email": data['email'], "password": data['password']})
        print("DEBUG: rows inserted ->", result.rowcount)
