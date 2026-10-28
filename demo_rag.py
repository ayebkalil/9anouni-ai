import os
import psycopg2
from dotenv import load_dotenv
import time

def print_typewriter(text, delay=0.01):
    """Prints text slowly like an AI typing."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def search_database(query):
    """Searches the PostgreSQL database using basic keyword matching (Mock Pillar C)."""
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Simple search in both Arabic and French texts
        search_term = f"%{query}%"
        cur.execute("""
            SELECT article_number, hierarchy_path, text_ar, text_fr 
            FROM current_article_versions 
            WHERE text_ar ILIKE %s OR text_fr ILIKE %s
            LIMIT 1;
        """, (search_term, search_term))
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None

def main():
    print("==================================================")
    print("🤖 Legal AI - Pillar C & D Proof of Concept")
    print("==================================================")
    print("Type a legal keyword to search (e.g., 'سيادة', 'independant', 'دينها').")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("\n👤 You: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        print("\n🔍 AI Searching Truth Database (Pillar C)...")
        time.sleep(1) # Fake loading time for dramatic effect in the video
        
        result = search_database(query)
        
        print("\n⚖️ AI Legal Assistant (Pillar D):")
        if result:
            art_num, hierarchy, text_ar, text_fr = result
            
            response = f"I found the relevant law in the database.\n"
            response += f"📍 Source: Article {art_num} ({hierarchy})\n\n"
            
            if text_ar:
                response += f"📜 Arabic: {text_ar}\n"
            if text_fr:
                response += f"📜 French: {text_fr}\n"
                
            print_typewriter(response)
        else:
            print_typewriter("I'm sorry, I could not find any laws matching that query in the database. Ensure Pillar A has ingested the relevant laws.")

if __name__ == "__main__":
    main()
