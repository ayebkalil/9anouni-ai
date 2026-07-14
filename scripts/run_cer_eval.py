import json
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.ocr.evaluator import evaluate_run_quality

def run_evaluation():
    processed_dir = os.path.join(project_root, "data", "processed")
    eval_dir = os.path.join(project_root, "data", "eval")
    gold_ref_path = os.path.join(eval_dir, "gold_reference.json")
    
    if not os.path.exists(gold_ref_path):
        print(f"Error: Gold reference not found at {gold_ref_path}")
        sys.exit(1)
        
    with open(gold_ref_path, "r", encoding="utf-8") as f:
        gold_references = json.load(f)
        
    # Find the 2026 run folder
    target_folder = None
    target_run_id = None
    for folder in os.listdir(processed_dir):
        if folder.startswith("prod-run-finance_law_2026-"):
            target_folder = os.path.join(processed_dir, folder)
            target_run_id = folder
            break

    if not target_folder:
        print("Could not find 2026 folder.")
        sys.exit(1)
        
    ocr_path = os.path.join(target_folder, "ocr_text.jsonl")
    
    print(f"Running CER Evaluation on Run: {target_run_id}")
    print(f"Using {len(gold_references)} gold reference blocks.")
    
    report_path = evaluate_run_quality(
        ocr_jsonl_path=ocr_path,
        gold_references=gold_references,
        run_id=target_run_id,
        base_processed_dir=processed_dir,
        source_format="scanned_pdf",
        modern_threshold=0.01,
        scanned_threshold=0.03
    )
    
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
        
    print("\n================ EVALUATION REPORT ================")
    print(f"Status:            {report['validation_status']}")
    print(f"Blocks Evaluated:  {report['blocks_evaluated_count']}")
    print(f"Average CER:       {report['average_cer']:.4%}")
    if report["failed_blocks"]:
        print(f"Failed Blocks:     {len(report['failed_blocks'])}")
        for fail in report["failed_blocks"]:
            print(f"  - Block {fail['block_id']}: {fail['error']}")
    print("===================================================\n")
    print(f"Full report saved to: {report_path}")

if __name__ == "__main__":
    run_evaluation()
