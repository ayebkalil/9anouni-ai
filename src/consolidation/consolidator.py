import os
import sys
from typing import List, Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion
from src.consolidation.patterns import detect_amendments as detect_amendments_regex
from src.consolidation.gemini_extractor import extract_amendments_with_gemini
from src.consolidation.temporal_ops import apply_repeal, apply_replace

def get_engine():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_root, ".env"))
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env")
    return create_engine(db_url)

def run_consolidation(dry_run: bool = True, use_gemini: bool = True):
    """
    Main engine for Pillar B: Temporal Consolidation.
    Scans the database chronologically and resolves amendments using
    a hybrid Regex + Gemini Pro pipeline.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Starting Temporal Consolidation... (Dry Run: {dry_run}, Use Gemini: {use_gemini})")
    
    # 1. Fetch all currently active articles, sorted chronologically
    articles = session.query(LegalArticleVersion).filter(
        LegalArticleVersion.status == "active"
    ).order_by(LegalArticleVersion.valid_from.asc()).all()

    total_amendments_found = 0
    total_applied = 0

    for article in articles:
        # Detect amendments declared in this article
        # First attempt fast regex detection
        amendments = detect_amendments_regex(article.text_ar)
        
        # If no regex match and Gemini is enabled, try Gemini Pro
        if not amendments and use_gemini and ("تنقح" in article.text_ar or "تلغى" in article.text_ar or "تعدل" in article.text_ar or "modifié" in (article.text_fr or "")):
            gemini_amds = extract_amendments_with_gemini(article.text_ar, article.text_fr)
            for gamd in gemini_amds:
                amendments.append({
                    "action": gamd.get("action", "replace"),
                    "target_code_id": gamd.get("target_code_id"),
                    "target_article_number": str(gamd.get("target_article_number")),
                    "original_match": "Gemini-extracted"
                })
        
        for amd in amendments:
            action = amd["action"]
            target_code = amd["target_code_id"]
            target_num = amd["target_article_number"]
            
            if not target_code or not target_num:
                continue

            total_amendments_found += 1
            print(f"[{article.valid_from}] Found '{action}' for {target_code} Article {target_num} (Source: {article.article_id})")
                  
            success = False
            if action == "repeal":
                success = apply_repeal(session, target_code, target_num, article)
            elif action in ["replace", "modify", "amend"]:
                success = apply_replace(session, target_code, target_num, article)
                
            if success:
                print(f"  -> Successfully applied {action} to {target_code} Art. {target_num}!")
                total_applied += 1
            else:
                print(f"  -> Target article not found or already closed.")

    print("-" * 50)
    print(f"Consolidation Summary:")
    print(f"  Amendments Detected: {total_amendments_found}")
    print(f"  Amendments Applied:  {total_applied}")

    if not dry_run:
        print("Committing changes to database...")
        try:
            session.commit()
            print("Commit successful!")
        except Exception as e:
            session.rollback()
            print(f"Failed to commit: {e}")
    else:
        print("Dry run complete. No changes committed.")
        session.rollback()

    session.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Temporal Consolidation (Pillar B)")
    parser.add_argument("--commit", action="store_true", help="Commit changes to DB (disables dry-run)")
    parser.add_argument("--no-gemini", action="store_true", help="Disable Gemini LLM fallback")
    args = parser.parse_args()
    
    run_consolidation(dry_run=not args.commit, use_gemini=not args.no_gemini)
