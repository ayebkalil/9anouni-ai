import psycopg2
import os
from dotenv import load_dotenv

def create_views():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return
        
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        print("Creating current_article_versions view...")
        # This view exposes only the currently active version of each article
        # It's optimized for Pillar C (Search Indexing)
        cur.execute("""
            CREATE OR REPLACE VIEW current_article_versions AS
            SELECT 
                version_id,
                article_id,
                code_id,
                article_number,
                hierarchy_path,
                text_ar,
                text_fr,
                valid_from,
                valid_to,
                status
            FROM legal_article_version
            WHERE status = 'active'
              AND valid_to > CURRENT_DATE;
        """)
        
        print("Creating article_versions_by_date view...")
        # This view allows time-travel queries (what did the law look like on a specific date?)
        cur.execute("""
            CREATE OR REPLACE VIEW article_versions_by_date AS
            SELECT 
                version_id,
                article_id,
                code_id,
                article_number,
                hierarchy_path,
                text_ar,
                text_fr,
                valid_from,
                valid_to
            FROM legal_article_version;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Successfully created Pillar C read views in the database!")
        
    except Exception as e:
        print(f"Error creating views: {e}")

if __name__ == "__main__":
    create_views()
