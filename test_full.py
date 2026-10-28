import glob, json
from src.ingestion.parser.parser import DocumentParser

path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
records = []
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            records.append(json.loads(line))

parser = DocumentParser('finance_law_2020')
articles = parser.parse_blocks(records, 'ar')
nums = sorted([int(a['article_number']) for a in articles if a['article_number'].isdigit()])
print(f"Total parsed digit articles: {len(nums)}")
print(nums)
