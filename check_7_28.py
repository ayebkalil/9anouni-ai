import glob, json
path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = '\n'.join([b['text'] for l in lines for b in json.loads(l).get('blocks', [])])
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'الفصل 7 ' in line or 'الفصل 7.' in line or 'الفصل 7' == line.strip():
        print(f'Line {i}: {repr(line)}')
    if 'الفصل 28 ' in line or 'الفصل 28.' in line or 'الفصل 28' == line.strip():
        print(f'Line {i}: {repr(line)}')
