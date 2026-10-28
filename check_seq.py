from src.consolidation.consolidator import get_engine
from sqlalchemy.orm import sessionmaker
from src.ingestion.models import LegalArticleVersion
from collections import defaultdict

session = sessionmaker(bind=get_engine())()
articles = session.query(LegalArticleVersion.code_id, LegalArticleVersion.article_number).all()
d = defaultdict(list)
for a in articles:
    d[a[0]].append(a[1])

for k, v in d.items():
    nums = sorted([int(x) for x in v if x.isdigit()])
    print(f"{k}: {nums}")
