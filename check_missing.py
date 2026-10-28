import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = ' '.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
missing=[7, 17, 18, 28, 30, 31, 47, 49, 52, 58]
for m in missing:
    matches = [line.strip() for line in text.split('\n') if f'الفصل {m} ' in line or f'الفصل {m}.' in line]
    if matches:
        print(f'Missing {m}:', repr(matches[0]))
