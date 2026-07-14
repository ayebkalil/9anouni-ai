import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion  # noqa: E402


def load_fixtures() -> None:
    # 1. Load environment variables
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not set in environment or .env file.")
        sys.exit(1)
        
    print(f"Connecting to database at: {db_url}")
    try:
        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
        
    # 2. Read fixtures file
    fixtures_path = os.path.join(project_root, "data", "fixtures_200_articles.json")
    if not os.path.exists(fixtures_path):
        print(f"Error: Fixtures file not found at {fixtures_path}")
        sys.exit(1)
        
    with open(fixtures_path, "r", encoding="utf-8") as f:
        fixtures_data = json.load(f)
        
    print(f"Loaded {len(fixtures_data)} fixtures from JSON.")
    
    # 3. Check table existence by inserting/querying, catching missing table errors
    try:
        # Check if table exists by querying row count
        session.query(LegalArticleVersion).limit(1).all()
    except Exception as e:
        print(
            "Error: Could not query the database table. "
            "Ensure you have run the Alembic migrations first! "
            f"Details: {e}"
        )
        session.rollback()
        sys.exit(1)
        
    # 4. Clean existing fixtures to avoid duplicate insert errors (idempotency)
    print("Clearing existing records to avoid primary key collisions...")
    try:
        session.query(LegalArticleVersion).delete()
        session.commit()
    except Exception as e:
        print(f"Error clearing table: {e}")
        session.rollback()
        sys.exit(1)
        
    # 5. Load and insert fixtures
    print("Inserting fixtures...")
    records_to_insert = []
    for item in fixtures_data:
        try:
            # Parse dates from YYYY-MM-DD string to python date objects
            valid_from_date = datetime.strptime(item["valid_from"], "%Y-%m-%d").date()
            valid_to_date = datetime.strptime(item["valid_to"], "%Y-%m-%d").date()
            
            record = LegalArticleVersion(
                version_id=item["version_id"],
                article_id=item["article_id"],
                code_id=item["code_id"],
                article_number=item["article_number"],
                hierarchy_path=item["hierarchy_path"],
                text_ar=item["text_ar"],
                text_fr=item["text_fr"],
                valid_from=valid_from_date,
                valid_to=valid_to_date,
                status=item["status"],
                source_ref=item["source_ref"],
                created_by_op=item["created_by_op"]
            )
            records_to_insert.append(record)
        except Exception as e:
            print(f"Error parsing fixture item: {item}. Error: {e}")
            
    try:
        session.bulk_save_objects(records_to_insert)
        session.commit()
        print(
            f"Successfully loaded {len(records_to_insert)} "
            "legal article versions into the database!"
        )
    except Exception as e:
        print(f"Error bulk saving objects to database: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    load_fixtures()
