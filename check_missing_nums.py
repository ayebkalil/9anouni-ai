from src.consolidation.consolidator import get_engine
from sqlalchemy.orm import sessionmaker
from src.ingestion.models import LegalArticleVersion
session = sessionmaker(bind=get_engine())()

def get_missing(code, max_num):
    articles = session.query(LegalArticleVersion.article_number).filter(LegalArticleVersion.code_id == code).all()
    nums = set([int(a[0]) for a in articles if a[0].isdigit()])
    return [i for i in range(1, max_num+1) if i not in nums]

print('2020 missing:', get_missing('finance_law_2020', 58))
print('2021 missing:', get_missing('finance_law_2021', 42))
print('2026 missing:', get_missing('finance_law_2026', 110))
