import glob, json
from src.ingestion.parser.parser import parse_arabic_article_header

path = glob.glob('data/processed/prod-run-finance_law_2020-*/ocr_text.jsonl')[0]
lines = open(path, encoding='utf-8').readlines()
text = ' '.join([b['text'] for l in lines for b in json.loads(l).get('blocks', []) if 'الفصل 58' in b['text']][-1:])
for line in text.split('\n'):
    line = line.strip()
    if not line: continue
    if '58' in line:
        print('Line:', repr(line))
        print('Parse result:', parse_arabic_article_header(line))
