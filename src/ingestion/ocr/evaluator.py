"""
Module to calculate Character Error Rate (CER) using Levenshtein distance.
Compares OCR hypothesis text against manually transcribed ground-truth reference sets.
"""

import json
import os
from typing import Any, Dict, List


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes the edit distance (Levenshtein distance) between two strings.
    Memory-efficient O(min(N, M)) space implementation.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_cer(reference: str, hypothesis: str) -> float:
    """
    Calculates the Character Error Rate (CER).
    Normalizes whitespace differences before computation.

    Args:
        reference: The ground-truth gold reference string.
        hypothesis: The OCR-extracted hypothesis string.

    Returns:
        The float CER value (e.g. 0.02 for 2% error rate).
    """
    # Clean extra whitespaces and normalise
    ref_clean = " ".join(reference.split())
    hyp_clean = " ".join(hypothesis.split())

    if not ref_clean:
        return 1.0 if hyp_clean else 0.0

    edit_dist = levenshtein_distance(ref_clean, hyp_clean)
    return float(edit_dist) / len(ref_clean)

def evaluate_run_quality(
    ocr_jsonl_path: str,
    gold_references: Dict[str, str],  # Maps block_id to ground-truth text
    run_id: str,
    base_processed_dir: str,
    source_format: str = "scanned_pdf", # e.g. "text_pdf" or "scanned_pdf"
    modern_threshold: float = 0.01,  # 1% error rate limit
    scanned_threshold: float = 0.03   # 3% error rate limit for older scans
) -> str:
    """
    Evaluates OCR output in ocr_text.jsonl against gold reference transcriptions.
    Generates validation_report.json documenting CER values and flags blocks failing thresholds.

    Args:
        ocr_jsonl_path: Path to the ocr_text.jsonl containing hypothesis blocks.
        gold_references: Dictionary mapping block_id keys to ground-truth strings.
        run_id: Process run ID.
        base_processed_dir: Base directory for processed outputs.
        source_format: format of the source (e.g. "text_pdf" or "scanned_pdf")
        modern_threshold: Maximum allowed CER for clean modern text.
        scanned_threshold: Maximum allowed CER for older scanned text.

    Returns:
        The absolute path to the generated validation_report.json file.
    """
    if not os.path.exists(ocr_jsonl_path):
        raise FileNotFoundError(f"OCR results JSONL file not found at: {ocr_jsonl_path}")

    report_path = os.path.join(base_processed_dir, run_id, "validation_report.json")
    
    evaluated_blocks: List[Dict[str, Any]] = []
    failed_blocks: List[Dict[str, Any]] = []
    
    total_cer = 0.0
    evaluated_count = 0
    
    # Determine the applicable threshold
    is_modern = source_format in ("text_pdf", "html", "manual_fixture")
    applicable_threshold = modern_threshold if is_modern else scanned_threshold

    with open(ocr_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            page_id = record["page_id"]
            
            for block in record.get("blocks", []):
                block_id = block["block_id"]
                
                # Check if we have gold reference for this block
                if block_id in gold_references:
                    ref_text = gold_references[block_id]
                    hyp_text = block["text"]
                    
                    cer_val = calculate_cer(ref_text, hyp_text)
                    total_cer += cer_val
                    evaluated_count += 1
                    
                    is_failed = cer_val > applicable_threshold
                    
                    eval_entry = {
                        "page_id": page_id,
                        "block_id": block_id,
                        "cer": cer_val,
                        "threshold_applied": applicable_threshold,
                        "status": "rejected" if is_failed else "accepted"
                    }
                    evaluated_blocks.append(eval_entry)
                    
                    if is_failed:
                        err_msg = f"CER {cer_val:.2%} exceeds limit of {applicable_threshold:.2%}"
                        failed_blocks.append({
                            "block_id": block_id,
                            "cer": cer_val,
                            "error": err_msg
                        })

    avg_cer = total_cer / evaluated_count if evaluated_count > 0 else 0.0

    report = {
        "run_id": run_id,
        "validation_status": "rejected" if failed_blocks else "accepted",
        "average_cer": avg_cer,
        "blocks_evaluated_count": evaluated_count,
        "failed_blocks": failed_blocks,
        "evaluations": evaluated_blocks
    }

    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    return os.path.abspath(report_path)

if __name__ == "__main__":
    # Smoke test for edit distance and CER
    ref = "الفصل الأول - تونس دولة حرة"
    hyp = "الفصل الأول - تونس دولة حرة"
    hyp_err = "الفصل الاول - تونس دوله حره" # Minor diffs: أ to ا and ة to ه
    
    print("Test 1 (Perfect Match) CER:", calculate_cer(ref, hyp))
    print("Test 2 (Errors) CER:", calculate_cer(ref, hyp_err))
    
    # Assertions for correctness
    assert calculate_cer(ref, hyp) == 0.0
    assert calculate_cer(ref, hyp_err) > 0.0
    print("Smoke tests passed successfully.")
