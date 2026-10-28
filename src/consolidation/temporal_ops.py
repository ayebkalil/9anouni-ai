import uuid
from typing import Dict, Optional

from sqlalchemy.orm import Session

from src.ingestion.models import LegalArticleVersion

def apply_repeal(session: Session, target_code_id: str, target_article_number: str,
                 amending_article: LegalArticleVersion) -> bool:
    """
    Finds the active version of the target article and closes it using the
    effective date (valid_from) of the amending article.
    Updates status to 'repealed'.
    Returns True if an article was successfully closed, False otherwise.
    """
    # Find the active version of the article being repealed
    old_version = session.query(LegalArticleVersion).filter(
        LegalArticleVersion.code_id == target_code_id,
        LegalArticleVersion.article_number == target_article_number,
        LegalArticleVersion.status == "active"
    ).first()

    if not old_version:
        return False

    # Close the old version
    old_version.valid_to = amending_article.valid_from
    old_version.status = "repealed"
    
    session.add(old_version)
    return True

def apply_replace(session: Session, target_code_id: str, target_article_number: str,
                  amending_article: LegalArticleVersion) -> bool:
    """
    Finds the active version of the target article, closes it, and spawns a NEW
    version for the target code with the new text found in the amending_article.
    """
    # 1. Close the old version
    old_version = session.query(LegalArticleVersion).filter(
        LegalArticleVersion.code_id == target_code_id,
        LegalArticleVersion.article_number == target_article_number,
        LegalArticleVersion.status == "active"
    ).first()

    if not old_version:
        return False

    old_version.valid_to = amending_article.valid_from
    old_version.status = "superseded"
    session.add(old_version)

    # 2. Spawn the new version of the article
    new_version = LegalArticleVersion(
        version_id=str(uuid.uuid4()),
        article_id=old_version.article_id,
        code_id=old_version.code_id,
        article_number=old_version.article_number,
        hierarchy_path=old_version.hierarchy_path,
        text_ar=amending_article.text_ar,  # The new text comes from the amendment
        text_fr=amending_article.text_fr,
        valid_from=amending_article.valid_from,
        valid_to=old_version.valid_to,  # 9999-12-31 logically unless already known
        status="active",
        source_ref=amending_article.source_ref,  # Traced back to the amending document!
        created_by_op="consolidation-run-regex"
    )
    
    session.add(new_version)
    return True
