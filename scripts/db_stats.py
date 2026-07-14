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
        # Query 1: Total count by code_id
        query = text("""
            SELECT code_id, COUNT(*) as article_count
            FROM legal_article_version
            GROUP BY code_id
            ORDER BY code_id;
        """)
        
        result = session.execute(query)
        rows = result.fetchall()
        
        total_articles = 0
        print("\n📊 DATABASE STATISTICS: ARTICLES PER LAW")
        print("-" * 50)
        print(f"{'Source Law (code_id)'.ljust(30)} | {'Article Count'}")
        print("-" * 50)
        for row in rows:
            print(f"{row.code_id.ljust(30)} | {row.article_count}")
            total_articles += row.article_count
            
        print("-" * 50)
        print(f"{'TOTAL'.ljust(30)} | {total_articles}")
        print("\n")
        
    except Exception as e:
        print(f"❌ Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
