import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Set project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

def create_db() -> None:
    # 1. Load environment variables
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not set in .env file.")
        sys.exit(1)
        
    # Extract target database name from URL (e.g. "legal_truth_db" from "postgresql://.../legal_truth_db")
    try:
        base_url, db_name = db_url.rsplit("/", 1)
        # Handle trailing query params if any
        if "?" in db_name:
            db_name = db_name.split("?", 1)[0]
    except Exception:
        print(f"Error: Could not parse database name from URL: {db_url}")
        sys.exit(1)
        
    # 2. Connect to the default "postgres" database first
    default_db_url = f"{base_url}/postgres"
    print(f"Connecting to default database to create '{db_name}'...")
    
    # We must use isolation_level="AUTOCOMMIT" to run CREATE DATABASE queries
    engine = create_engine(default_db_url, isolation_level="AUTOCOMMIT")
    
    # 3. Execute CREATE DATABASE
    with engine.connect() as conn:
        # Check if database already exists
        check_query = text("SELECT 1 FROM pg_database WHERE datname = :dbname")
        result = conn.execute(check_query, {"dbname": db_name}).fetchone()
        
        if result:
            print(f"Database '{db_name}' already exists. No action needed!")
        else:
            print(f"Creating database '{db_name}'...")
            try:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Successfully created database '{db_name}'!")
            except Exception as e:
                print(f"Error creating database: {e}")
                print(
                    "\nTip: Make sure PostgreSQL service is running "
                    "and the password in your .env file is correct."
                )
                sys.exit(1)

if __name__ == "__main__":
    create_db()
