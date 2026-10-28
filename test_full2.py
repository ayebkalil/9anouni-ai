import glob, json
from src.ingestion.parser.parser import DocumentParser

path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
records = []
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            records.append(json.loads(line))

parser = DocumentParser('finance_law_2020')
for record in records:
    for block in record.get("blocks", []):
        raw_text = block["text"]
        from src.ingestion.parser.parser import clean_ocr_text, parse_arabic_article_header
        cleaned_text = clean_ocr_text(raw_text)
        block_type = block.get("type", "article_body")
        for line in cleaned_text.split("\n"):
            line = line.strip()
            if not line: continue
            if '58' in line and block_type != "table":
                res = parse_arabic_article_header(line)
                if res:
                    print(f"Parsed {res} from line: {repr(line)}")
