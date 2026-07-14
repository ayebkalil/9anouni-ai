"""
Module to load structured legal article versions into the PostgreSQL database.
Enforces validation reports, ensures idempotency, and respects dry-run vs commit.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, cast

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion


def load_batch_config(config_path: str) -> Dict[str, Any]:
    """Loads and validates the loader batch configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Loader batch configuration not found at: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return cast(Dict[str, Any], json.load(f))

def run_loader(batch_config_path: str, database_url: str, is_dry_run: bool) -> None:
    """Executes the database load process based on batch configuration."""
    # 1. Load batch configuration
    config = load_batch_config(batch_config_path)
    inputs = config.get("inputs", {})
    rules = config.get("acceptance_rules", {})
    load_run_id = config.get("load_run_id", "default-run")
    
    manifest_path = inputs.get("manifest")
    parsed_path = inputs.get("parsed_articles")
    report_path = inputs.get("validation_report")
    
    # Resolve relative paths relative to project root if they don't exist
    def resolve_path(p: str) -> str:
        if os.path.isabs(p) or os.path.exists(p):
            return p
        return os.path.join(project_root, p)
        
    resolved_manifest_path = resolve_path(manifest_path)
    resolved_parsed_path = resolve_path(parsed_path)
    resolved_report_path = resolve_path(report_path)
    
    # 2. Read manifest to get source metadata
    if not os.path.exists(resolved_manifest_path):
        print(f"Error: Manifest file not found at: {resolved_manifest_path}")
        sys.exit(1)
        
    with open(resolved_manifest_path, "r", encoding="utf-8") as mf:
        manifest = json.load(mf)
    source_id = manifest.get("source_id")
    code_id = manifest.get("code_id")
    source_date = manifest.get("source_date")
    
    print(f"Processing Load Run '{load_run_id}' for Source '{source_id}' ({code_id})...")
    
    # 3. Read and check validation report
    if not os.path.exists(resolved_report_path):
        print(f"Error: Validation report file not found at: {resolved_report_path}")
        sys.exit(1)
        
    with open(resolved_report_path, "r", encoding="utf-8") as rf:
        report = json.load(rf)
        
    validation_status = report.get("validation_status", "rejected")
    allow_validation_errors = rules.get("allow_validation_errors", False)
    
    if validation_status == "rejected" and not allow_validation_errors:
        print("Error: Validation status is REJECTED. Loader refuses to load the records.")
        print("Validation Errors summary:")
        for err in report.get("errors", []):
            print(f" - [{err.get('code')}]: {err.get('message')} (Pages: {err.get('page_ids')})")
        sys.exit(1)
        
    # 4. Connect to database
    print(f"Connecting to database at: {database_url}")
    try:
        engine = create_engine(database_url)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
        
    # 5. Read parsed articles
    if not os.path.exists(resolved_parsed_path):
        print(f"Error: Parsed articles file not found at: {resolved_parsed_path}")
        sys.exit(1)
        
    parsed_articles = []
    with open(resolved_parsed_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parsed_articles.append(json.loads(line))
                
    # 6. Begin transaction
    try:
        # Check if table exists
        session.query(LegalArticleVersion).limit(1).all()
    except Exception as e:
        print(f"Error: Target table 'legal_article_version' not accessible. Ensure Alembic migrations are applied. Details: {e}")
        session.close()
        sys.exit(1)
        
    if not is_dry_run:
        # Idempotency: Clear existing records for the same source_id to prevent duplicates
        print(f"Clearing existing records for source_id '{source_id}' to ensure idempotency...")
        try:
            # PostgreSQL JSONB search on source_ref->'source_id'
            session.query(LegalArticleVersion).filter(
                LegalArticleVersion.source_ref['source_id'].astext == source_id
            ).delete(synchronize_session=False)
            session.flush()
        except Exception as e:
            print(f"Error clearing existing records: {e}")
            session.rollback()
            session.close()
            sys.exit(1)
            
    # 7. Convert and prepare records
    records_to_insert = []
    seen_article_ids = set()
    
    for art in parsed_articles:
        valid_from = art.get("valid_from", source_date or "2000-01-01")
        valid_to = art.get("valid_to", "9999-12-31")
        
        valid_from_date = datetime.strptime(valid_from, "%Y-%m-%d").date()
        valid_to_date = datetime.strptime(valid_to, "%Y-%m-%d").date()
        
        # Build source_ref with load metadata
        source_ref = art.get("source_ref", {})
        source_ref["source_id"] = source_id
        source_ref["load_run_id"] = load_run_id
        
        article_number = art.get("article_number")
        article_id = art.get("article_id") or f"{code_id}:article-{article_number}"
        
        # Deduplicate to prevent constraint violations
        if article_id in seen_article_ids:
            print(f"Warning: Duplicate article_id '{article_id}' found in batch. Skipping duplicate.")
            continue
            
        seen_article_ids.add(article_id)
        
        import uuid
        record = LegalArticleVersion(
            version_id=art.get("version_id") or str(uuid.uuid4()),
            article_id=article_id,
            code_id=art.get("code_id") or code_id,
            article_number=article_number,
            hierarchy_path=art.get("hierarchy_path", "General"),
            text_ar=art.get("text_ar", ""),
            text_fr=art.get("text_fr"),
            valid_from=valid_from_date,
            valid_to=valid_to_date,
            status=art.get("status", "active"),
            source_ref=source_ref,
            created_by_op=load_run_id
        )
        records_to_insert.append(record)
        
    print(f"Prepared {len(records_to_insert)} records to load.")
    
    if is_dry_run:
        print("--- DRY RUN MODE: Rolling back transaction, database untouched ---")
        session.rollback()
        session.close()
        print("Dry run completed successfully.")
    else:
        try:
            session.bulk_save_objects(records_to_insert)
            session.commit()
            print(f"Successfully loaded {len(records_to_insert)} article versions into the database!")
        except Exception as e:
            print(f"Error executing database commit: {e}")
            session.rollback()
            session.close()
            sys.exit(1)
        finally:
            session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Idempotent database loader for legal article versions.")
    parser.add_argument("--batch", required=True, help="Path to the loader batch configuration JSON.")
    parser.add_argument("--database-url", required=True, help="SQLAlchemy database URL connection string.")
    
    # Exclusive group for mode selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--commit", action="store_true", help="Commit the transaction to target database.")
    group.add_argument("--dry-run", action="store_true", help="Perform database insertion checks, but rollback without committing.")
    
    args = parser.parse_args()
    
    run_loader(args.batch, args.database_url, args.dry_run)
