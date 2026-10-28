import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = '\n'.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'يرخص' in line and 'لسنة' in line and '2020' in line:
        for j in range(-3, 6):
            if 0 <= i+j < len(lines):
                print(f"Line {i+j}: {repr(lines[i+j].strip())}")
