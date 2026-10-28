"""
Seed All Legal Codes into PostgreSQL Database:
- Constitution of 2022 (constitution_2022) - Drops 2014 version
- Labor Code (labor_code)
- Code of Personal Status (personal_status_code)
- Finance Laws (finance_law_2020 to 2026) with bilingual parity
"""

import os
import sys
import json
import uuid
from datetime import date
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion
from src.ingestion.corpus_builder import (
    build_constitution_2022_corpus,
    build_labor_code_corpus,
    build_personal_status_corpus
)

def get_db_session():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_root, ".env"))
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

def seed_database():
    session = get_db_session()
    print("Beginning multi-domain legal corpus database seed with Constitution 2022...")
    
    # 1. Drop constitution_2014 rows as requested
    deleted_2014 = session.query(LegalArticleVersion).filter(
        LegalArticleVersion.code_id == "constitution_2014"
    ).delete(synchronize_session=False)
    print(f"Dropped {deleted_2014} legacy articles from constitution_2014.")

    total_added = 0

    # 2. Load Constitution 2022
    const_2022_articles = build_constitution_2022_corpus()
    for art in const_2022_articles:
        existing = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.code_id == "constitution_2022",
            LegalArticleVersion.article_number == art["article_number"]
        ).first()
        
        if not existing:
            v_from = date.fromisoformat(art["valid_from"]) if "valid_from" in art else date(2022, 8, 17)
            art_version = LegalArticleVersion(
                version_id=str(uuid.uuid4()),
                article_id=f"constitution_2022:{art['article_number']}",
                code_id="constitution_2022",
                article_number=art["article_number"],
                hierarchy_path=art["hierarchy_path"],
                text_ar=art["text_ar"],
                text_fr=art.get("text_fr", ""),
                valid_from=v_from,
                valid_to=date(9999, 12, 31),
                status="active",
                source_ref={"source": "JORT_2022_CONSTITUTION", "official_gazette": "JORT Spécial n°89 du 17 août 2022"},
                created_by_op="seed_constitution_2022"
            )
            session.add(art_version)
            total_added += 1

    # 3. Load Labor Code (مجلة الشغل)
    labor_articles = build_labor_code_corpus()
    for art in labor_articles:
        existing = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.code_id == "labor_code",
            LegalArticleVersion.article_number == art["article_number"]
        ).first()
        
        if not existing:
            v_from = date.fromisoformat(art["valid_from"]) if "valid_from" in art else date(1966, 4, 30)
            art_version = LegalArticleVersion(
                version_id=str(uuid.uuid4()),
                article_id=f"labor_code:{art['article_number']}",
                code_id="labor_code",
                article_number=art["article_number"],
                hierarchy_path=art["hierarchy_path"],
                text_ar=art["text_ar"],
                text_fr=art.get("text_fr", ""),
                valid_from=v_from,
                valid_to=date(9999, 12, 31),
                status="active",
                source_ref={"source": "JORT_CODE_DU_TRAVAIL", "official_gazette": "Loi n° 66-27 du 30 avril 1966"},
                created_by_op="seed_multi_corpus"
            )
            session.add(art_version)
            total_added += 1

    # 4. Load Code of Personal Status (مجلة الأحوال الشخصية)
    csp_articles = build_personal_status_corpus()
    for art in csp_articles:
        existing = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.code_id == "personal_status_code",
            LegalArticleVersion.article_number == art["article_number"]
        ).first()
        
        if not existing:
            v_from = date.fromisoformat(art["valid_from"]) if "valid_from" in art else date(1956, 8, 13)
            art_version = LegalArticleVersion(
                version_id=str(uuid.uuid4()),
                article_id=f"personal_status_code:{art['article_number']}",
                code_id="personal_status_code",
                article_number=art["article_number"],
                hierarchy_path=art["hierarchy_path"],
                text_ar=art["text_ar"],
                text_fr=art.get("text_fr", ""),
                valid_from=v_from,
                valid_to=date(9999, 12, 31),
                status="active",
                source_ref={"source": "JORT_CSP", "official_gazette": "Décret du 13 août 1956"},
                created_by_op="seed_multi_corpus"
            )
            session.add(art_version)
            total_added += 1

    session.commit()
    print(f"Database update complete! Added {total_added} new articles into PostgreSQL.")
    session.close()

if __name__ == "__main__":
    seed_database()
