import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2026-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = ' '.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
for l in text.split('\n'):
    if 'الفصل 29' in l or 'الفصل 58' in l:
        print(repr(l.strip()))
