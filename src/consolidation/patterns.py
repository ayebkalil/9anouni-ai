import re
from typing import Dict, List, Optional

# Basic map for standard Tunisian legal codes to our internal code_ids.
# For month 1, we are focusing mostly on Finance Laws.
CODE_MAP = {
    "قانون المالية": "finance_law_{year}",
    "مجلة الضريبة على دخل الأشخاص الطبيعيين والضريبة على الشركات": "code_irpp_is",
    "مجلة معاليم التسجيل والطابع الجبائي": "code_enregistrement",
    "مجلة الأداء على القيمة المضافة": "code_tva",
    "مجلة الديوانة": "code_douane",
    "مجلة المحاسبة العمومية": "code_cp",
    "مجلة الشركات التجارية": "commercial_companies_code",
    "مجلة الشغل": "labor_code"
}

# 1. REPEAL PATTERN (تلغى أحكام الفصل X من ...)
# Matches: تلغى أحكام الفصل 14 من قانون المالية لسنة 2020
# Group 1: Article Number
# Group 2: Code Name
# Group 3: Year (Optional, for Finance Laws)
REPEAL_PATTERN = re.compile(
    r"تلغى\s+(?:أحكام\s+)?الفصل\s+(\d+(?:\s+مكرر|\s+ثالثا)?)\s+من\s+(.+?)(?:\s+لسنة\s+(\d{4}))?(?=\s*$|\.)"
)

# 2. REPLACE/AMEND PATTERN (تعوض أحكام الفصل X من ... بما يلي)
# Matches: تعوض أحكام الفصل 14 من قانون المالية لسنة 2020 بما يلي
REPLACE_PATTERN = re.compile(
    r"(?:تعوض|تنقح)\s+(?:أحكام\s+)?الفصل\s+(\d+(?:\s+مكرر|\s+ثالثا)?)\s+من\s+(.+?)(?:\s+لسنة\s+(\d{4}))?(?=\s+بما\s+يلي|\s*$|\.)"
)

def _normalize_code_name(arabic_name: str, year: Optional[str] = None) -> Optional[str]:
    """Converts the Arabic legal code name into the internal DB code_id."""
    clean_name = arabic_name.strip()
    
    # Specific rule for Finance Laws
    if "قانون المالية" in clean_name and year:
        if "التعديلي" in clean_name:
            return f"finance_law_{year}_rect"
        return f"finance_law_{year}"
        
    # Match against standard codes
    for ar_name, internal_id in CODE_MAP.items():
        if ar_name in clean_name:
            return internal_id
            
    # Fallback to generic representation
    return None

def detect_amendments(text_ar: str) -> List[Dict]:
    """
    Parses Arabic legal text and returns a list of detected amendments.
    Example return:
    [
        {"action": "repeal", "target_code_id": "finance_law_2020", "target_article": "14"},
        {"action": "replace", "target_code_id": "code_tva", "target_article": "5"}
    ]
    """
    amendments = []
    
    # 1. Search for Repeals
    for match in REPEAL_PATTERN.finditer(text_ar):
        article_num = match.group(1).strip()
        code_name = match.group(2).strip()
        year = match.group(3)
        
        target_code_id = _normalize_code_name(code_name, year)
        if target_code_id:
            amendments.append({
                "action": "repeal",
                "target_code_id": target_code_id,
                "target_article_number": article_num,
                "original_match": match.group(0)
            })

    # 2. Search for Replacements / Amendments
    for match in REPLACE_PATTERN.finditer(text_ar):
        article_num = match.group(1).strip()
        code_name = match.group(2).strip()
        year = match.group(3)
        
        target_code_id = _normalize_code_name(code_name, year)
        if target_code_id:
            amendments.append({
                "action": "replace",
                "target_code_id": target_code_id,
                "target_article_number": article_num,
                "original_match": match.group(0)
            })

    return amendments
