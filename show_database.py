import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup project path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
load_dotenv(os.path.join(project_root, ".env"))

# Force utf-8 encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

from src.ingestion.models import LegalArticleVersion

def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set in .env")
        return
        
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    
    try:
        # Query all active articles
        records = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.status == 'active'
        ).all()
        
        print("\n=======================================================================================================================")
        print(f"📊 FOUND {len(records)} ACTIVE ARTICLES IN THE LEGAL TRUTH DATABASE")
        print("=======================================================================================================================\n")
        
        if not records:
            print("The database is currently empty.")
            return

        # Print header
        print(f"{'Code ID':<25} | {'Article':<8} | {'Valid From':<12} | {'Text Snippet (AR)'}")
        print("-" * 119)
        
        # Print rows
        for r in records:
            snippet = r.text_ar[:70].replace('\n', ' ') + "..." if r.text_ar else "No Arabic Text"
            print(f"{r.code_id:<25} | {r.article_number:<8} | {str(r.valid_from):<12} | {snippet}")
            
        print("\n=======================================================================================================================\n")
        
    finally:
        session.close()

if __name__ == "__main__":
    main()
