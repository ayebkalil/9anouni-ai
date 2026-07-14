import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
load_dotenv(os.path.join(project_root, ".env"))

sys.stdout.reconfigure(encoding='utf-8')

def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set")
        return
        
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    
    try:
        # We will use a PostgreSQL window function to get exactly 2 articles per code_id
        query = text("""
            SELECT code_id, article_id, valid_from, text_ar
            FROM (
                SELECT 
                    code_id, 
                    article_id, 
                    valid_from, 
                    text_ar,
                    ROW_NUMBER() OVER(PARTITION BY code_id ORDER BY article_number) as rn
                FROM legal_article_version
            ) sub
            WHERE rn <= 2
            ORDER BY code_id, article_id;
        """)
        
        result = session.execute(query)
        rows = result.fetchall()
        
        current_code = ""
        for row in rows:
            if row.code_id != current_code:
                print(f"\n### Source: {row.code_id}")
                current_code = row.code_id
                
            # Truncate text to keep the output readable
            text_preview = row.text_ar.replace('\n', ' ')
            if len(text_preview) > 150:
                text_preview = text_preview[:150] + "..."
                
            print(f"- **Article ID**: `{row.article_id}`")
            print(f"  - **Valid From**: {row.valid_from}")
            print(f"  - **Text snippet**: {text_preview}")
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
