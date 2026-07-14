import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
load_dotenv(os.path.join(project_root, ".env"))

# Force utf-8 encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set in .env")
        return
        
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    
    try:
        print(f"Connecting to {db_url} to clear database...")
        # TRUNCATE table completely clears it quickly
        session.execute(text("TRUNCATE TABLE legal_article_version CASCADE;"))
        session.commit()
        print("✅ Successfully cleared all data from the database.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
