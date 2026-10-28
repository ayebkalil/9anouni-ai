import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = ' '.join([b['text'] for l in lines for b in json.loads(l).get('blocks', []) if 'الفصل 58' in b['text']][-1:])
for line in text.split('\n'):
    if '58' in line:
        print(repr(line))
