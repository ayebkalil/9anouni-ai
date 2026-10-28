import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = ' '.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
for l in text.split('\n'):
    if '7' in l and 'الفصل' in l and ('يرخص' in l or 'يستخلص' in l):
        print(repr(l.strip()))
    if '28' in l and 'الفصل' in l and 'توضيح' in l:
        print(repr(l.strip()))
