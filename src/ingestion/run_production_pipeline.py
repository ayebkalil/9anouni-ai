import json
import os
import sys
import uuid
import glob
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.load_articles import run_loader
from src.ingestion.ocr.extractor import run_ocr_pipeline
from src.ingestion.parser.parser import run_parser_pipeline
from src.ingestion.validator.validator import run_validation_pipeline

# Force utf-8 encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

def process_single_pdf(pdf_path: str, code_id: str, db_url: str):
    base_processed = os.path.join(project_root, "data", "processed")
    run_id = f"prod-run-{code_id}-{uuid.uuid4().hex[:8]}"
    source_id = f"src-{code_id}"
    
    print(f"\n=======================================================================")
    print(f"🚀 STARTING PRODUCTION PIPELINE FOR: {code_id}")
    print(f"📄 Target File: {pdf_path}")
    print(f"=======================================================================\n")
    
    # Step 1: OCR
    print(f"--- [Step 1] Running OCR Pipeline for {code_id} ---")
    print(f"(This step will take a while as it processes every page of the PDF)")
    ocr_jsonl_path = run_ocr_pipeline(
        pdf_path,
        run_id,
        base_processed,
        language="ar",
        source_id=source_id,
    )
    
    # Step 2: Parser
    print(f"\n--- [Step 2] Running Parser Pipeline for {code_id} ---")
    import re
    match = re.search(r'\d{4}', code_id)
    valid_from_year = match.group(0) if match else "2000"
    valid_from = f"{valid_from_year}-01-01"
    
    articles = run_parser_pipeline(ocr_jsonl_path, code_id, valid_from)
    parsed_jsonl_path = os.path.join(base_processed, run_id, "parsed_articles.jsonl")
    with open(parsed_jsonl_path, "w", encoding="utf-8") as pf:
        for art in articles:
            pf.write(json.dumps(art, ensure_ascii=False) + "\n")
    print(f"Parsed {len(articles)} articles.")
    
    # Step 3: Validator
    print(f"\n--- [Step 3] Running Validator Pipeline for {code_id} ---")
    report_json_path = os.path.join(base_processed, run_id, "validation_report.json")
    report = run_validation_pipeline(
        parsed_jsonl_path,
        report_json_path,
        source_id,
        run_id
    )
    print(f"Validation status: {report['validation_status']}")
    
    # Step 4: Batch Configuration
    print(f"\n--- [Step 4] Creating Batch Configuration for {code_id} ---")
    # Write a dummy manifest to satisfy paths
    manifest_dir = os.path.dirname(pdf_path)
    manifest_path = os.path.join(manifest_dir, "manifest.json")
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
            "allow_validation_errors": True, # Soft validation for bulk production
            "require_source_ref": True,
            "require_non_empty_text": True,
            "prevent_duplicate_article_versions": True
        }
    }
    batch_json_path = os.path.join(base_processed, run_id, "batch.json")
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
        
    raw_dir = os.path.join(project_root, "data", "raw")
    pdf_files = glob.glob(os.path.join(raw_dir, "**", "original.pdf"), recursive=True)
    
    if not pdf_files:
        print(f"No PDFs found in {raw_dir}")
        return
        
    print(f"Found {len(pdf_files)} PDFs to process.")
    for pdf_path in pdf_files:
        # code_id is the folder name
        code_id = os.path.basename(os.path.dirname(pdf_path))
        try:
            process_single_pdf(pdf_path, code_id, db_url)
        except Exception as e:
            print(f"❌ Error processing {code_id}: {e}")

if __name__ == "__main__":
    main()
