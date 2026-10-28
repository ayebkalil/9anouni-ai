import glob, json, re
path = glob.glob('data/processed/prod-run-finance_law_2026-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = '\n'.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
lines = text.split('\n')
for i, line in enumerate(lines):
    match = re.search(r"^\s*الفصل\s+(\d+)", line)
    if match:
        print(f"Line {i}: Found Chapter {match.group(1)}")
