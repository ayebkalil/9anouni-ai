import json
import os
import sys

# Add project root to sys.path
project_root = r"c:\Users\ayebk\OneDrive\Desktop\ocr pip"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.load_articles import run_loader
from src.ingestion.ocr.extractor import run_ocr_pipeline
from src.ingestion.parser.parser import run_parser_pipeline
from src.ingestion.validator.validator import run_validation_pipeline


def main() -> None:
    # 1. Define paths
    pdf_path = os.path.join(project_root, "data", "raw", "finance_law_2020_rect", "original.pdf")
    run_id = "verify-e2e-run"
    base_processed = os.path.join(project_root, "data", "processed")
    
    # Extract only page 1 for a fast run
    import fitz
    temp_pdf_path = os.path.join(base_processed, "temp_e2e.pdf")
    os.makedirs(base_processed, exist_ok=True)
    
    src = fitz.open(pdf_path)
    dest = fitz.open()
    dest.insert_pdf(src, from_page=0, to_page=0)  # page 1 only
    dest.save(temp_pdf_path)
    dest.close()
    src.close()
    
    print("\n--- [Step 1] Running OCR Pipeline ---")
    try:
        # Run OCR with single column layout
        ocr_jsonl_path = run_ocr_pipeline(
            temp_pdf_path,
            run_id,
            base_processed,
            language="ar",
            source_id="src-finance-law-2020-rect-e2e",
            columns_count=1
        )
        print(f"OCR output written to: {ocr_jsonl_path}")
        
        print("\n--- [Step 2] Running Parser Pipeline ---")
        articles = run_parser_pipeline(ocr_jsonl_path, "finance_law_2020_rect", "2020-12-14")
        parsed_jsonl_path = os.path.join(base_processed, run_id, "parsed_articles.jsonl")
        with open(parsed_jsonl_path, "w", encoding="utf-8") as pf:
            for art in articles:
                pf.write(json.dumps(art, ensure_ascii=False) + "\n")
        print(f"Parsed {len(articles)} articles. Written to: {parsed_jsonl_path}")
        
        print("\n--- [Step 3] Running Validator Pipeline ---")
        report_json_path = os.path.join(base_processed, run_id, "validation_report.json")
        report = run_validation_pipeline(
            parsed_jsonl_path,
            report_json_path,
            "src-finance-law-2020-rect-e2e",
            run_id
        )
        print(f"Validation status: {report['validation_status']}")
        
        print("\n--- [Step 4] Creating Batch Configuration ---")
        batch_data = {
            "load_run_id": run_id,
            "schema_version": "2026_07_legal_truth_v1",
            "mode": "dry_run_then_commit",
            "inputs": {
                "manifest": "data/raw/finance_law_2020_rect/manifest.json",
                "parsed_articles": os.path.relpath(parsed_jsonl_path, project_root),
                "validation_report": os.path.relpath(report_json_path, project_root)
            },
            "acceptance_rules": {
                "allow_validation_errors": False,
                "require_source_ref": True,
                "require_non_empty_text": True,
                "prevent_duplicate_article_versions": True
            }
        }
        batch_json_path = os.path.join(base_processed, run_id, "batch.json")
        with open(batch_json_path, "w", encoding="utf-8") as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        print(f"Batch config written to: {batch_json_path}")
        
        # Get Database URL from environment
        from dotenv import load_dotenv
        load_dotenv(os.path.join(project_root, ".env"))
        # 5. Database Loading
        # Ensure DATABASE_URL is set or provide a default for type checking
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/legal_truth_db")
        if db_url:
            print(f"\n--- [Step 5] Database Loading: {db_url} ---")
            run_loader(batch_json_path, db_url, is_dry_run=True)
            
            print("\n--- [Step 6] Running Loader in Commit Mode ---")
            run_loader(batch_json_path, db_url, is_dry_run=False)
        
        print("\n--- [Step 7] Querying Database for Verification ---")
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        from src.ingestion.models import LegalArticleVersion
        
        engine = create_engine(db_url)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        
        try:
            records = session.query(LegalArticleVersion).filter(
                LegalArticleVersion.code_id == "finance_law_2020_rect"
            ).all()
            print(f"Successfully loaded {len(records)} records for finance_law_2020_rect:")
            verify_log = os.path.join(base_processed, run_id, "verification_log.txt")
            with open(verify_log, "w", encoding="utf-8") as vf:
                vf.write(f"Successfully loaded {len(records)} records for finance_law_2020_rect:\n")
                for idx, r in enumerate(records, 1):
                    vf.write(f"  {idx}. Article {r.article_number} ({r.hierarchy_path}):\n")
                    snippet = r.text_ar[:100].replace('\n', ' ')
                    vf.write(f"     Text snippet: {snippet}\n")
                    vf.write(f"     Source Page: {r.source_ref.get('page_ids')}\n")
            print(f"Verification output written to: {verify_log}")
        finally:
            session.close()
            
    finally:
        # Cleanup
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        # We don't remove the processed run dir immediately so the user can inspect it if needed.
        print(f"\nIngestion run files preserved at: {os.path.join(base_processed, run_id)}")

if __name__ == "__main__":
    main()
