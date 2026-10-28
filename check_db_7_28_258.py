from src.consolidation.consolidator import get_engine
from sqlalchemy.orm import sessionmaker
from src.ingestion.models import LegalArticleVersion
session = sessionmaker(bind=get_engine())()
articles = session.query(LegalArticleVersion.article_number, LegalArticleVersion.text_ar).filter(LegalArticleVersion.code_id == 'finance_law_2020').all()
for a in sorted([a for a in articles if a[0].isdigit()], key=lambda x: int(x[0])):
    if a[0] in ['7', '28', '258']:
        print(f"Article {a[0]}: {a[1][:100]}...")
