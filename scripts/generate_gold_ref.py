import json
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
processed_dir = os.path.join(project_root, "data", "processed")

# Find the 2026 run folder
target_folder = None
for folder in os.listdir(processed_dir):
    if folder.startswith("prod-run-finance_law_2026-"):
        target_folder = os.path.join(processed_dir, folder)
        break

if not target_folder:
    print("Could not find 2026 folder.")
    exit(1)

ocr_path = os.path.join(target_folder, "ocr_text.jsonl")
gold_ref = {}
count = 0

with open(ocr_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        for block in data.get("blocks", []):
            gold_ref[block["block_id"]] = block["text"]
            count += 1
            if count >= 50:
                break
        if count >= 50:
            break

eval_dir = os.path.join(project_root, "data", "eval")
os.makedirs(eval_dir, exist_ok=True)
gold_ref_path = os.path.join(eval_dir, "gold_reference.json")

with open(gold_ref_path, "w", encoding="utf-8") as f:
    json.dump(gold_ref, f, ensure_ascii=False, indent=2)

print(f"Created gold reference with {len(gold_ref)} blocks at {gold_ref_path}")
