from src.consolidation.consolidator import get_engine
from sqlalchemy.orm import sessionmaker
from src.ingestion.models import LegalArticleVersion

session = sessionmaker(bind=get_engine())()
articles = session.query(LegalArticleVersion).filter(LegalArticleVersion.code_id == 'finance_law_2023').all()
to_delete = []
for a in articles:
    if not a.article_number.isdigit():
        to_delete.append(a)

for a in to_delete:
    session.delete(a)
session.commit()
print(f'Deleted {len(to_delete)} rogue articles from finance_law_2023.')
