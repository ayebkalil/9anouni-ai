import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.consolidation.patterns import detect_amendments

def test_detect_repeal():
    text = "تلغى أحكام الفصل 14 من قانون المالية لسنة 2020."
    amendments = detect_amendments(text)
    
    assert len(amendments) == 1
    assert amendments[0]["action"] == "repeal"
    assert amendments[0]["target_code_id"] == "finance_law_2020"
    assert amendments[0]["target_article_number"] == "14"

def test_detect_repeal_bis():
    text = "تلغى أحكام الفصل 14 مكرر من مجلة الأداء على القيمة المضافة."
    amendments = detect_amendments(text)
    
    assert len(amendments) == 1
    assert amendments[0]["action"] == "repeal"
    assert amendments[0]["target_code_id"] == "code_tva"
    assert amendments[0]["target_article_number"] == "14 مكرر"

def test_detect_replace():
    text = "تعوض أحكام الفصل 5 من مجلة الضريبة على دخل الأشخاص الطبيعيين والضريبة على الشركات بما يلي:"
    amendments = detect_amendments(text)
    
    assert len(amendments) == 1
    assert amendments[0]["action"] == "replace"
    assert amendments[0]["target_code_id"] == "code_irpp_is"
    assert amendments[0]["target_article_number"] == "5"

def test_no_amendments():
    text = "هذا فصل عادي لا يحتوي على أي تعديلات."
    amendments = detect_amendments(text)
    assert len(amendments) == 0

def test_multiple_amendments():
    text = """
    تلغى أحكام الفصل 10 من قانون المالية لسنة 2021.
    كما تعوض أحكام الفصل 20 من مجلة الديوانة بما يلي:
    """
    amendments = detect_amendments(text)
    assert len(amendments) == 2
    
    assert amendments[0]["action"] == "repeal"
    assert amendments[0]["target_code_id"] == "finance_law_2021"
    assert amendments[0]["target_article_number"] == "10"
    
    assert amendments[1]["action"] == "replace"
    assert amendments[1]["target_code_id"] == "code_douane"
    assert amendments[1]["target_article_number"] == "20"
