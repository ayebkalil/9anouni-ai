import json
import os
import sys
import uuid
import glob
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.ingestion.load_articles import run_loader
from src.ingestion.parser.parser import run_parser_pipeline
from src.ingestion.validator.validator import run_validation_pipeline

sys.stdout.reconfigure(encoding='utf-8')

def process_rect_pdf(run_dir: str, code_id: str, db_url: str):
    print(f"\n=======================================================================")
    print(f"🚀 RESUMING PIPELINE FOR: {code_id}")
    print(f"=======================================================================\n")
    
    ocr_jsonl_path = os.path.join(run_dir, "ocr_text.jsonl")
    if not os.path.exists(ocr_jsonl_path):
        print(f"❌ OCR file not found: {ocr_jsonl_path}")
        return
        
    run_id = os.path.basename(run_dir)
    source_id = f"src-{code_id}"
    
    # Use regex to extract the 4-digit year safely
    import re
    match = re.search(r'\d{4}', code_id)
    valid_from_year = match.group(0) if match else "2000"
    valid_from = f"{valid_from_year}-01-01"
    
    # Step 2: Parser
    print(f"--- [Step 2] Running Parser Pipeline for {code_id} ---")
    articles = run_parser_pipeline(ocr_jsonl_path, code_id, valid_from)
    parsed_jsonl_path = os.path.join(run_dir, "parsed_articles.jsonl")
    with open(parsed_jsonl_path, "w", encoding="utf-8") as pf:
        for art in articles:
            pf.write(json.dumps(art, ensure_ascii=False) + "\n")
    print(f"Parsed {len(articles)} articles.")
    
    # Step 3: Validator
    print(f"\n--- [Step 3] Running Validator Pipeline for {code_id} ---")
    report_json_path = os.path.join(run_dir, "validation_report.json")
    report = run_validation_pipeline(
        parsed_jsonl_path,
        report_json_path,
        source_id,
        run_id
    )
    print(f"Validation status: {report['validation_status']}")
    
    # Step 4: Batch Configuration
    print(f"\n--- [Step 4] Creating Batch Configuration for {code_id} ---")
    manifest_path = os.path.join(project_root, "data", "raw", code_id, "manifest.json")
    if not os.path.exists(manifest_path):
        with open(manifest_path, "w", encoding="utf-8") as m:
            json.dump({"code_id": code_id, "layout": "single_column"}, m)
            
    batch_data = {
        "load_run_id": run_id,
        "schema_version": "2026_07_legal_truth_v1",
        "mode": "dry_run_then_commit",
        "inputs": {
            "manifest": os.path.relpath(manifest_path, project_root),
            "parsed_articles": os.path.relpath(parsed_jsonl_path, project_root),
            "validation_report": os.path.relpath(report_json_path, project_root)
        },
        "acceptance_rules": {
            "allow_validation_errors": True,
            "require_source_ref": True,
            "require_non_empty_text": True,
            "prevent_duplicate_article_versions": True
        }
    }
    batch_json_path = os.path.join(run_dir, "batch.json")
    with open(batch_json_path, "w", encoding="utf-8") as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
    # Step 5 & 6: Database Loading
    print(f"\n--- [Step 5] Database Loading for {code_id} ---")
    run_loader(batch_json_path, db_url, is_dry_run=False)
    
    print(f"\n✅ SUCCESSFULLY PROCESSED AND LOADED {code_id}\n")

def main():
    load_dotenv(os.path.join(project_root, ".env"))
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set in .env")
        return
        
    base_processed = os.path.join(project_root, "data", "processed")
    rect_dirs = [
        ("finance_law_2020_rect", os.path.join(base_processed, "prod-run-finance_law_2020_rect-3b14e79d")),
        ("finance_law_2021_rect", os.path.join(base_processed, "prod-run-finance_law_2021_rect-9b04e347"))
    ]
    
    for code_id, d in rect_dirs:
        process_rect_pdf(d, code_id, db_url)

if __name__ == "__main__":
    main()
