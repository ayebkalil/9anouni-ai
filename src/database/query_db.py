import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Set project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion  # noqa: E402


def query_database() -> None:
    # 1. Load environment variables
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not set in .env file.")
        sys.exit(1)
        
    # 2. Connect to the database
    try:
        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
        
    # 3. Query general stats
    print("--- Database Connection Successful ---")
    try:
        total_rows = session.query(func.count(LegalArticleVersion.version_id)).scalar()
        print(f"Total Legal Article Versions: {total_rows}")
        
        # Group by code_id
        grouped = session.query(
            LegalArticleVersion.code_id, 
            func.count(LegalArticleVersion.version_id)
        ).group_by(LegalArticleVersion.code_id).all()
        
        print("\nArticle count by Code:")
        for code, count in grouped:
            print(f"- {code}: {count} articles")
            
        # Get first 5 rows to write to a text file for inspection
        first_five = session.query(LegalArticleVersion).order_by(
            LegalArticleVersion.code_id, 
            LegalArticleVersion.article_number
        ).limit(5).all()
        
        output_file_path = os.path.join(project_root, "src", "database", "query_results.txt")
        
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write("=== DATABASE QUERY RESULTS (Sample Articles) ===\n")
            f.write(f"Total Rows in Database: {total_rows}\n\n")
            for idx, art in enumerate(first_five, 1):
                f.write(f"Article Sample {idx}:\n")
                f.write(f"  - Version ID: {art.version_id}\n")
                f.write(f"  - Article ID: {art.article_id}\n")
                f.write(f"  - Code ID: {art.code_id}\n")
                f.write(f"  - Article Number: {art.article_number}\n")
                f.write(f"  - Hierarchy Path: {art.hierarchy_path}\n")
                f.write(f"  - Text (Arabic): {art.text_ar}\n")
                f.write(f"  - Text (French): {art.text_fr}\n")
                f.write(f"  - Status: {art.status}\n")
                f.write(f"  - Validity: {art.valid_from} to {art.valid_to}\n")
                f.write("-" * 50 + "\n")
                
        print(f"\nWritten sample data to inspect in: {output_file_path}")
        
    except Exception as e:
        print(f"Error querying database tables: {e}")
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    query_database()
