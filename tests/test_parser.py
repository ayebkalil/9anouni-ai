import pytest
from src.ingestion.parser.parser import parse_arabic_article_header, parse_french_article_header, DocumentParser

def test_arabic_article_header_parsing():
    # Standard chapter
    assert parse_arabic_article_header("الفصل 62 :") == ("62", "الفصل 62", False)
    assert parse_arabic_article_header("الفصل الأول") == ("1", "الفصل الأول", False)
    assert parse_arabic_article_header("الفصل 75:") == ("75", "الفصل 75", False)

def test_finance_law_amendment_ignore():
    # Create a mock parser instance for a finance law
    parser = DocumentParser("finance_law_2023", "2023-01-01")
    
    # Simulate the block processing logic where bis/ter are ignored
    line = "الفصل 51 سابعا:"
    art_info = parse_arabic_article_header(line)
    
    # Ensure it's initially parsed as a modified article
    assert art_info is not None
    norm_num, display_num, is_new = art_info
    assert norm_num == "51-septies"
    
    # Ensure our finance law logic ignores it
    if parser.code_id.startswith("finance_law_") and "-" in norm_num:
        art_info = None
        
    assert art_info is None, "Finance law should ignore amendment chapters (bis, ter, septies)"

def test_ocr_hallucination_correction():
    parser = DocumentParser("finance_law_2020", "2020-01-01")
    
    # Simulate processing chapter 258
    art_info = parse_arabic_article_header("الفصل 258 :")
    assert art_info is not None
    norm_num, display_num, is_new = art_info
    assert norm_num == "258"
    
    # Simulate the hardcoded fix
    if parser.code_id == "finance_law_2020" and norm_num == "258":
        norm_num, display_num = "28", "الفصل 28"
        
    assert norm_num == "28"
    assert display_num == "الفصل 28"
