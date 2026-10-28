from src.consolidation.consolidator import get_engine
from sqlalchemy.orm import sessionmaker
from src.ingestion.models import LegalArticleVersion

session = sessionmaker(bind=get_engine())()
articles = session.query(LegalArticleVersion).all()

max_articles = {
    'finance_law_2020': 60,
    'finance_law_2020_rect': 20,
    'finance_law_2021': 50,
    'finance_law_2021_rect': 20,
    'finance_law_2022': 80,
    'finance_law_2023': 80,
    'finance_law_2024': 80,
    'finance_law_2025': 90,
    'finance_law_2026': 120,
}

to_delete = []
for a in articles:
    if a.code_id not in max_articles:
        continue
    
    # Condition 1: non-digit
    if not a.article_number.isdigit():
        to_delete.append(a)
        continue
        
    # Condition 2: exceeds max for that law
    if int(a.article_number) > max_articles[a.code_id]:
        to_delete.append(a)
        continue

print(f"Deleting {len(to_delete)} rogue articles across all documents...")
for a in to_delete:
    print(f"Deleting {a.code_id} Article {a.article_number}")
    session.delete(a)
    
session.commit()
print("Cleanup complete!")
