"""
Module to perform structural validation checks on parsed legal articles.
Generates a validation report mapping errors like duplicates, empty content, 
or missing source references.
"""

import json
import os
from typing import Any, Dict, List


def validate_articles(
    articles: List[Dict[str, Any]], 
    source_id: str,
    run_id: str
) -> Dict[str, Any]:
    """
    Validates parsed articles and generates a validation report.
    Checks for duplicates, empty text, and missing source references.
    """
    errors: List[Dict[str, Any]] = []
    seen_articles: Dict[str, List[str]] = {}  # Maps article_number to list of hierarchies
    
    for art in articles:
        art_num = art.get("article_number")
        hierarchy = art.get("hierarchy_path", "General")
        page_ids = art.get("source_ref", {}).get("page_ids", [])
        
        # 1. Empty Text check
        text_ar = art.get("text_ar", "").strip()
        text_fr = art.get("text_fr", "").strip()
        if not text_ar and not text_fr:
            errors.append({
                "code": "EMPTY_TEXT",
                "message": f"Article {art_num} has empty text in both Arabic and French.",
                "page_ids": page_ids,
                "suggested_action": "Verify OCR page content or check layout crop configurations."
            })
            
        # 2. Missing Source Reference check
        source_ref = art.get("source_ref", {})
        if not source_ref or not source_ref.get("source_id") or not page_ids or not source_ref.get("blocks"):
            errors.append({
                "code": "MISSING_SOURCE_REF",
                "message": f"Article {art_num} has no page/block source span mapping.",
                "page_ids": page_ids,
                "suggested_action": "Verify parser block accumulation logic."
            })
            
        # 3. Duplicate Article Number check
        if art_num:
            if art_num in seen_articles:
                # Same article number in the same code/hierarchy
                if hierarchy in seen_articles[art_num]:
                    errors.append({
                        "code": "DUPLICATE_ARTICLE_NUMBER",
                        "message": f"Article {art_num} appears multiple times under the hierarchy '{hierarchy}'.",
                        "page_ids": page_ids,
                        "suggested_action": "Review whether it is an amendment, a table continuation, or a layout error."
                    })
                seen_articles[art_num].append(hierarchy)
            else:
                seen_articles[art_num] = [hierarchy]
                
        # 4. Invalid Date check
        valid_from = art.get("valid_from")
        valid_to = art.get("valid_to")
        if valid_from and valid_to:
            try:
                from datetime import datetime
                d_from = datetime.strptime(valid_from, "%Y-%m-%d").date()
                d_to = datetime.strptime(valid_to, "%Y-%m-%d").date()
                if d_to < d_from:
                    errors.append({
                        "code": "INVALID_DATES",
                        "message": f"Article {art_num} has valid_to ({valid_to}) earlier than valid_from ({valid_from}).",
                        "page_ids": page_ids,
                        "suggested_action": "Correct the validity dates."
                    })
            except ValueError:
                errors.append({
                    "code": "INVALID_DATE_FORMAT",
                    "message": f"Article {art_num} has malformed dates.",
                    "page_ids": page_ids,
                    "suggested_action": "Ensure dates are in YYYY-MM-DD format."
                })
                
        # 5. Missing Hierarchy check
        if not hierarchy:
            errors.append({
                "code": "MISSING_HIERARCHY",
                "message": f"Article {art_num} has an empty hierarchy path.",
                "page_ids": page_ids,
                "suggested_action": "Ensure parser sets a fallback hierarchy path like 'General'."
            })
                
    validation_status = "rejected" if errors else "accepted"
    
    return {
        "validation_status": validation_status,
        "run_id": run_id,
        "source_id": source_id,
        "errors": errors
    }

def run_validation_pipeline(
    parsed_jsonl_path: str,
    report_output_path: str,
    source_id: str,
    run_id: str
) -> Dict[str, Any]:
    """Reads parsed_articles.jsonl, runs validation, and writes validation_report.json."""
    if not os.path.exists(parsed_jsonl_path):
        raise FileNotFoundError(f"Parsed articles file not found: {parsed_jsonl_path}")
        
    articles = []
    with open(parsed_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                articles.append(json.loads(line))
                
    report = validate_articles(articles, source_id, run_id)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(report_output_path), exist_ok=True)
    
    with open(report_output_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    return report
