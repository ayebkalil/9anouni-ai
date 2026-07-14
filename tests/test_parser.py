import json
import os
import sys

import pytest

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.parser.parser import (
    DocumentParser,
    align_bilingual_articles,
    parse_arabic_article_header,
    parse_french_article_header,
    parse_hierarchy_heading,
)
from src.ingestion.validator.validator import validate_articles


def test_arabic_article_header_parsing():
    # Test standard number written in words
    res = parse_arabic_article_header("الفصل الأول - تونس دولة حرة")
    assert res is not None
    assert res[0] == "1"
    assert res[1] == "الفصل الأول"
    assert res[2] is False

    # Test digits and nuevo/جديد
    res = parse_arabic_article_header("الفصل 12 (جديد):")
    assert res is not None
    assert res[0] == "12"
    assert res[1] == "الفصل 12"
    assert res[2] is True

    # Test bis modifier
    res = parse_arabic_article_header("الفصل 12 مكرر:")
    assert res is not None
    assert res[0] == "12-bis"
    assert res[1] == "الفصل 12 مكرر"

    # Test ter modifier
    res = parse_arabic_article_header("الفصل 12 ثالثا")
    assert res is not None
    assert res[0] == "12-ter"
    assert res[1] == "الفصل 12 ثالثا"

def test_french_article_header_parsing():
    # Test premier
    res = parse_french_article_header("Article premier - La Tunisie est un Etat libre")
    assert res is not None
    assert res[0] == "1"
    assert res[1] == "Article premier"
    assert res[2] is False

    # Test digit and bis
    res = parse_french_article_header("Article 12 bis (nouveau)")
    assert res is not None
    assert res[0] == "12-bis"
    assert res[1] == "Article 12 bis"
    assert res[2] is True

def test_hierarchy_parsing():
    assert parse_hierarchy_heading("الكتاب الأول") == ("book", "الكتاب الأول")
    assert parse_hierarchy_heading("الباب الأول") == ("part", "الباب الأول")
    assert parse_hierarchy_heading("القسم الثالث") == ("section", "القسم الثالث")
    assert parse_hierarchy_heading("Livre I") == ("book", "Livre I")
    assert parse_hierarchy_heading("Chapitre II") == ("chapter", "Chapitre II")

def test_align_bilingual_articles():
    ar_art = [{
        "article_id": "test:article-1",
        "code_id": "test",
        "article_number": "1",
        "display_number_ar": "الفصل الأول",
        "display_number_fr": "",
        "hierarchy_path": "General",
        "text_ar": "نص عربي",
        "text_fr": "",
        "source_ref": {"source_id": "src-ar", "page_ids": ["p0001"], "blocks": ["b1"]},
        "paragraphs": []
    }]
    fr_art = [{
        "article_id": "test:article-1",
        "code_id": "test",
        "article_number": "1",
        "display_number_ar": "",
        "display_number_fr": "Article premier",
        "hierarchy_path": "General",
        "text_ar": "",
        "text_fr": "texte francais",
        "source_ref": {"source_id": "src-fr", "page_ids": ["p0002"], "blocks": ["b2"]},
        "paragraphs": []
    }]

    merged = align_bilingual_articles(ar_art, fr_art)
    assert len(merged) == 1
    assert merged[0]["article_number"] == "1"
    assert merged[0]["text_ar"] == "نص عربي"
    assert merged[0]["text_fr"] == "texte francais"
    assert "p0001" in merged[0]["source_ref"]["page_ids"]
    assert "p0002" in merged[0]["source_ref"]["page_ids"]

def test_validator_rules():
    # 1. Test empty text validation
    art_empty = [{
        "article_number": "1",
        "hierarchy_path": "General",
        "text_ar": "",
        "text_fr": "",
        "source_ref": {"source_id": "src", "page_ids": ["p1"], "blocks": ["b1"]}
    }]
    report = validate_articles(art_empty, "src", "run")
    assert report["validation_status"] == "rejected"
    assert any(err["code"] == "EMPTY_TEXT" for err in report["errors"])

    # 2. Test missing source ref validation
    art_no_ref = [{
        "article_number": "2",
        "hierarchy_path": "General",
        "text_ar": "نص",
        "text_fr": "",
        "source_ref": {}
    }]
    report = validate_articles(art_no_ref, "src", "run")
    assert report["validation_status"] == "rejected"
    assert any(err["code"] == "MISSING_SOURCE_REF" for err in report["errors"])

    # 3. Test duplicate article number validation
    art_dups = [
        {
            "article_number": "3",
            "hierarchy_path": "General",
            "text_ar": "نص 1",
            "text_fr": "",
            "source_ref": {"source_id": "src", "page_ids": ["p1"], "blocks": ["b1"]}
        },
        {
            "article_number": "3",
            "hierarchy_path": "General",
            "text_ar": "نص 2",
            "text_fr": "",
            "source_ref": {"source_id": "src", "page_ids": ["p1"], "blocks": ["b2"]}
        }
    ]
    report = validate_articles(art_dups, "src", "run")
    assert report["validation_status"] == "rejected"
    assert any(err["code"] == "DUPLICATE_ARTICLE_NUMBER" for err in report["errors"])

def test_document_parser_full_loop():
    ocr_record = {
        "run_id": "test-run",
        "source_id": "test-source",
        "page_id": "p0001",
        "blocks": [
            {
                "block_id": "b1",
                "type": "column_body",
                "bbox": [0, 0, 100, 100],
                "text": "الباب الأول\nالفصل الأول (جديد):\nمداخيل ميزانية الدولة 100 دينار\nالفصل الثاني مكرر\nنفقات ميزانية الدولة 50 دينار",
                "language": "ar"
            }
        ]
    }
    
    parser = DocumentParser("test_code", "2020-01-01")
    articles = parser.parse_blocks([ocr_record], "ar")
    
    assert len(articles) == 2
    assert articles[0]["article_number"] == "1"
    assert articles[0]["hierarchy_path"] == "الباب الأول"
    assert "مداخيل ميزانية الدولة" in articles[0]["text_ar"]
    assert articles[1]["article_number"] == "2-bis"
    assert "نفقات ميزانية الدولة" in articles[1]["text_ar"]

def test_parser_and_validator_pipelines(tmp_path):
    ocr_record = {
        "run_id": "test-run",
        "source_id": "test-source",
        "page_id": "p0001",
        "blocks": [
            {
                "block_id": "b1",
                "type": "column_body",
                "bbox": [0, 0, 100, 100],
                "text": "Livre I\nArticle premier\nTexte de l'article premier.\nArticle 2\nTexte de l'article 2.",
                "language": "fr"
            }
        ]
    }
    
    # Save mock OCR records to a temp file
    ocr_jsonl = tmp_path / "ocr_text.jsonl"
    with open(ocr_jsonl, "w", encoding="utf-8") as f:
        f.write(json.dumps(ocr_record) + "\n")
        
    # Run parser pipeline
    from src.ingestion.parser.parser import run_parser_pipeline
    articles = run_parser_pipeline(str(ocr_jsonl), "test_code_fr", "2020-01-01")
    
    assert len(articles) == 2
    assert articles[0]["article_number"] == "1"
    assert articles[0]["hierarchy_path"] == "Livre I"
    assert "article premier" in articles[0]["text_fr"].lower()
    
    # Write parsed articles to a temp file
    parsed_jsonl = tmp_path / "parsed_articles.jsonl"
    with open(parsed_jsonl, "w", encoding="utf-8") as pf:
        for art in articles:
            pf.write(json.dumps(art) + "\n")
            
    # Run validation pipeline
    from src.ingestion.validator.validator import run_validation_pipeline
    report_json = tmp_path / "validation_report.json"
    report = run_validation_pipeline(str(parsed_jsonl), str(report_json), "test-source", "test-run")
    
    assert report["validation_status"] == "accepted"
    assert os.path.exists(report_json)

def test_database_loader(tmp_path):
    from dotenv import load_dotenv
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        pytest.skip("DATABASE_URL not set in environment, skipping loader integration test.")

    # 1. Create a mock manifest
    manifest_data = {
        "source_id": "src-loader-test",
        "code_id": "loader_test_code",
        "source_date": "2020-01-01",
        "language": "ar",
        "format": "scanned_pdf",
        "page_count": 1,
        "sha256": "mock_sha256",
        "official_reference": {"publisher": "JORT", "title": "Test Law"},
        "reuse_status": "official"
    }
    manifest_json = tmp_path / "manifest.json"
    with open(manifest_json, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f)

    # 2. Create mock parsed articles
    article_data = {
        "article_id": "loader_test_code:article-1",
        "code_id": "loader_test_code",
        "article_number": "1",
        "hierarchy_path": "General",
        "text_ar": "نص الفصل الأول للمختبر",
        "text_fr": None,
        "valid_from": "2020-01-01",
        "valid_to": "9999-12-31",
        "status": "active",
        "source_ref": {
            "source_id": "src-loader-test",
            "page_ids": ["p0001"],
            "blocks": ["b1"]
        }
    }
    parsed_jsonl = tmp_path / "parsed_articles.jsonl"
    with open(parsed_jsonl, "w", encoding="utf-8") as f:
        f.write(json.dumps(article_data) + "\n")

    # 3. Create mock validation report
    report_data = {
        "validation_status": "accepted",
        "run_id": "test-run-123",
        "source_id": "src-loader-test",
        "errors": []
    }
    report_json = tmp_path / "validation_report.json"
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(report_data, f)

    # 4. Create batch configuration
    batch_data = {
        "load_run_id": "test-load-run",
        "schema_version": "2026_07_legal_truth_v1",
        "mode": "dry_run_then_commit",
        "inputs": {
            "manifest": str(manifest_json),
            "parsed_articles": str(parsed_jsonl),
            "validation_report": str(report_json)
        },
        "acceptance_rules": {
            "allow_validation_errors": False,
            "require_source_ref": True,
            "require_non_empty_text": True,
            "prevent_duplicate_article_versions": True
        }
    }
    batch_json = tmp_path / "batch.json"
    with open(batch_json, "w", encoding="utf-8") as f:
        json.dump(batch_data, f)

    # 5. Run the loader in dry-run mode
    from src.ingestion.load_articles import run_loader
    run_loader(str(batch_json), db_url, is_dry_run=True)

    # 6. Run the loader in commit mode
    run_loader(str(batch_json), db_url, is_dry_run=False)

    # Verify that the article was inserted into the database
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from src.ingestion.models import LegalArticleVersion

    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        loaded = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.source_ref["source_id"].astext == "src-loader-test"
        ).all()
        assert len(loaded) == 1
        assert loaded[0].article_number == "1"
        assert loaded[0].text_ar == "نص الفصل الأول للمختبر"
        
        # Cleanup loader records
        session.query(LegalArticleVersion).filter(
            LegalArticleVersion.source_ref["source_id"].astext == "src-loader-test"
        ).delete(synchronize_session=False)
    finally:
        session.close()

def test_fixture_parser_simple_fr():
    fixture_path = os.path.join(project_root, "tests", "fixtures", "fixture_parser_simple_fr.json")
    from src.ingestion.parser.parser import run_parser_pipeline
    articles = run_parser_pipeline(fixture_path, "test_code_fr", "2020-01-01")
    assert len(articles) == 3
    assert articles[0]["article_number"] == "1"
    assert articles[1]["article_number"] == "2"
    assert articles[2]["article_number"] == "3"
    assert articles[0]["hierarchy_path"] == "Livre I > Chapitre I"

def test_fixture_parser_bis_ter_ar():
    fixture_path = os.path.join(project_root, "tests", "fixtures", "fixture_parser_bis_ter_ar.json")
    from src.ingestion.parser.parser import run_parser_pipeline
    articles = run_parser_pipeline(fixture_path, "test_code_ar", "2020-01-01")
    assert len(articles) == 3
    assert articles[0]["article_number"] == "12"
    assert articles[1]["article_number"] == "12-bis"
    assert articles[2]["article_number"] == "12-ter"

def test_fixture_parser_table_tax():
    fixture_path = os.path.join(project_root, "tests", "fixtures", "fixture_parser_table_tax.json")
    from src.ingestion.parser.parser import run_parser_pipeline
    articles = run_parser_pipeline(fixture_path, "test_code_table", "2020-01-01")
    assert len(articles) == 1
    assert "جدول الضرائب" in articles[0]["text_ar"]
    assert "10% | 1000" in articles[0]["text_ar"]

def test_fixture_parser_duplicate_reject(tmp_path):
    fixture_path = os.path.join(project_root, "tests", "fixtures", "fixture_parser_duplicate_reject.json")
    from src.ingestion.parser.parser import run_parser_pipeline
    from src.ingestion.validator.validator import run_validation_pipeline
    
    articles = run_parser_pipeline(fixture_path, "test_code_dup", "2020-01-01")
    
    parsed_jsonl = tmp_path / "parsed.jsonl"
    with open(parsed_jsonl, "w", encoding="utf-8") as pf:
        for art in articles:
            pf.write(json.dumps(art) + "\n")
            
    report_json = tmp_path / "report.json"
    report = run_validation_pipeline(str(parsed_jsonl), str(report_json), "src-fixture-dup", "test-run")
    
    assert report["validation_status"] == "rejected"
    assert any(err["code"] == "DUPLICATE_ARTICLE_NUMBER" for err in report["errors"])

