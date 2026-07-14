"""
Module to parse layout OCR text blocks into structured legal articles.
Extracts headings, hierarchical paths (Book, Part, Chapter, Section), 
article numbers (normalized to canonical formats), and aligns bilingual text.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

# Mapping of Arabic written numbers to digits
ARABIC_NUMBERS = {
    "الأول": "1", "الأولى": "1",
    "الثاني": "2", "الثانية": "2",
    "الثالث": "3", "الثالثة": "3",
    "الرابع": "4", "الرابعة": "4",
    "الخامس": "5", "الخامسة": "5",
    "السادس": "6", "السادسة": "6",
    "السابع": "7", "السابعة": "7",
    "الثامن": "8", "الثامنة": "8",
    "التاسع": "9", "التاسعة": "9",
    "العاشر": "10", "العاشرة": "10",
    "الحادي عشر": "11", "الحادية عشرة": "11",
    "الثاني عشر": "12", "الثانية عشرة": "12",
    "الثالث عشر": "13", "الثالثة عشرة": "13",
    "الرابع عشر": "14", "الرابعة عشرة": "14",
    "الخامس عشر": "15", "الخامسة عشرة": "15",
    "السادس عشر": "16", "السادسة عشرة": "16",
    "السابع عشر": "17", "السابعة عشرة": "17",
    "الثامن عشر": "18", "الثامنة عشرة": "18",
    "التاسع عشر": "19", "التاسعة عشرة": "19",
    "العشرون": "20", "العشرينات": "20",
    "الحادي والعشرون": "21", "الحادية والعشرون": "21",
    "الثاني والعشرون": "22", "الثانية والعشرون": "22",
}

# Arabic/French modifier mapping (bis, ter, etc.)
MODIFIERS = {
    "مكرر": "bis",
    "ثالثا": "ter",
    "رابعا": "quater",
    "خامسا": "quinquies",
    "سادسا": "sexies",
    "سابعا": "septies",
    "ثامنا": "octies",
    "تاسعا": "novies",
    "عاشرا": "decies",
    "bis": "bis",
    "ter": "ter",
    "quater": "quater",
    "quinquies": "quinquies",
    "sexies": "sexies",
    "septies": "septies",
    "octies": "octies",
    "novies": "novies",
    "decies": "decies"
}

def clean_ocr_text(text: str) -> str:
    """Removes standard gazette page/date headers and footers from OCR text."""
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip empty lines
        if not stripped:
            continue
        # Skip JORT gazette headers/footers
        if "الرائد الرسمي" in stripped or "الجمهورية التونسية" in stripped:
            continue
        if re.search(r"صفحــة\s*\d+", stripped) or re.search(r"صفحة\s*\d+", stripped):
            continue
        if re.search(r"عدد\s*\d+", stripped) or re.search(r"ديسمبر\s*\d+", stripped) or re.search(r"جانفي|فيفري|مارس|أفريل|ماي|جوان|جويلية|أوت|سبتمبر|أكتوبر|نوفمبر|ديسمبر", stripped):
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)

def parse_arabic_article_header(line: str) -> Optional[Tuple[str, str, bool]]:
    """
    Parses Arabic article headers.
    Returns: (normalized_number, display_number, is_new) or None
    Example: 'الفصل الأول (جديد):' -> ('1', 'الفصل الأول', True)
    """
    # Regex: الفصل + written number or digit + optional modifier + optional (جديد)
    pattern = r"^\s*الفصل\s+((?:\d+|الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|الحادي عشر|الثاني عشر|الثالث عشر|الرابع عشر|الخامس عشر|السادس عشر|السابع عشر|الثامن عشر|التاسع عشر|العشرون|الحادي والعشرون|الثاني والعشرون))\s*(مكرر|ثالثا|رابعا|خامسا|سادسا|سابعا|ثامنا|تاسعا|عاشرا)?\s*(\(جديد\))?(?:[:\.\-\s]|$)"
    match = re.search(pattern, line)
    if not match:
        return None
    
    raw_num = match.group(1).strip()
    modifier = match.group(2)
    is_new = bool(match.group(3))
    
    # Normalize the number part
    norm_num = ARABIC_NUMBERS.get(raw_num, raw_num)
    if modifier:
        suffix = MODIFIERS.get(modifier, modifier)
        norm_num = f"{norm_num}-{suffix}"
        
    display_name = f"الفصل {raw_num}"
    if modifier:
        display_name += f" {modifier}"
        
    return norm_num, display_name, is_new

def parse_french_article_header(line: str) -> Optional[Tuple[str, str, bool]]:
    """
    Parses French article headers.
    Returns: (normalized_number, display_number, is_new) or None
    Example: 'Article premier (nouveau)' -> ('1', 'Article premier', True)
    """
    pattern = r"^\s*Article\s+(premier|\d+)\s*(bis|ter|quater|quinquies|sexies|septies|octies|novies|decies)?\s*(\(nouveau\))?(?:[:\.\-\s]|$)"
    match = re.search(pattern, line, re.IGNORECASE)
    if not match:
        return None
    
    raw_num = match.group(1).strip().lower()
    modifier = match.group(2)
    is_new = bool(match.group(3))
    
    norm_num = "1" if raw_num == "premier" else raw_num
    if modifier:
        norm_num = f"{norm_num}-{modifier.lower()}"
        
    display_name = f"Article {match.group(1)}"
    if modifier:
        display_name += f" {modifier}"
        
    return norm_num, display_name, is_new

def parse_hierarchy_heading(line: str) -> Optional[Tuple[str, str]]:
    """
    Identifies hierarchy headings like Book, Part, Chapter, Section.
    Returns: (level, value) or None
    """
    # Arabic patterns
    ar_book = re.search(r"^\s*الكتاب\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|\d+)", line)
    if ar_book:
        return "book", ar_book.group(0).strip()
        
    ar_part = re.search(r"^\s*الباب\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|\d+)", line)
    if ar_part:
        return "part", ar_part.group(0).strip()
        
    ar_section = re.search(r"^\s*القسم\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|\d+)", line)
    if ar_section:
        return "section", ar_section.group(0).strip()

    ar_subsection = re.search(r"^\s*الفرع\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|\d+)", line)
    if ar_subsection:
        return "subsection", ar_subsection.group(0).strip()

    # French patterns (Longer Roman numerals placed first to prevent prefix match issues)
    fr_book = re.search(r"^\s*Livre\s+(\d+|VIII|III|VII|XII|II|IV|VI|IX|XI|V|I|X)\b", line, re.IGNORECASE)
    if fr_book:
        return "book", fr_book.group(0).strip()
        
    fr_title = re.search(r"^\s*Titre\s+(\d+|VIII|III|VII|XII|II|IV|VI|IX|XI|V|I|X|premier)\b", line, re.IGNORECASE)
    if fr_title:
        return "part", fr_title.group(0).strip()
        
    fr_chapter = re.search(r"^\s*Chapitre\s+(\d+|VIII|III|VII|XII|II|IV|VI|IX|XI|V|I|X|premier)\b", line, re.IGNORECASE)
    if fr_chapter:
        return "chapter", fr_chapter.group(0).strip()
        
    fr_section = re.search(r"^\s*Section\s+(\d+|VIII|III|VII|XII|II|IV|VI|IX|XI|V|I|X)\b", line, re.IGNORECASE)
    if fr_section:
        return "section", fr_section.group(0).strip()

    return None

class DocumentParser:
    """Parser to read OCR page blocks and group them into hierarchical articles."""
    
    def __init__(self, code_id: str, default_valid_from: str = "2000-01-01"):
        self.code_id = code_id
        self.default_valid_from = default_valid_from
        self.current_hierarchy: Dict[str, str] = {
            "book": "",
            "part": "",
            "chapter": "",
            "section": "",
            "subsection": ""
        }
        
    def get_hierarchy_path(self) -> str:
        """Returns the current hierarchy path string."""
        parts = []
        for level in ["book", "part", "chapter", "section", "subsection"]:
            val = self.current_hierarchy[level]
            if val:
                parts.append(val)
        return " > ".join(parts) if parts else "General"

    def parse_blocks(self, records: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
        """Parses list of OCR page records for a single language."""
        articles: List[Dict[str, Any]] = []
        current_article: Optional[Dict[str, Any]] = None
        
        for record in records:
            page_id = record["page_id"]
            
            for block in record.get("blocks", []):
                block_id = block["block_id"]
                raw_text = block["text"]
                cleaned_text = clean_ocr_text(raw_text)
                
                lines = cleaned_text.split("\n")
                
                for _idx, line in enumerate(lines):
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                        
                    # Check for hierarchy changes
                    h_info = parse_hierarchy_heading(stripped_line)
                    if h_info:
                        level, val = h_info
                        self.current_hierarchy[level] = val
                        # Reset child hierarchies
                        if level == "book":
                            self.current_hierarchy["part"] = ""
                            self.current_hierarchy["chapter"] = ""
                            self.current_hierarchy["section"] = ""
                            self.current_hierarchy["subsection"] = ""
                        elif level == "part":
                            self.current_hierarchy["chapter"] = ""
                            self.current_hierarchy["section"] = ""
                            self.current_hierarchy["subsection"] = ""
                        elif level == "chapter":
                            self.current_hierarchy["section"] = ""
                            self.current_hierarchy["subsection"] = ""
                        elif level == "section":
                            self.current_hierarchy["subsection"] = ""
                        continue
                        
                    # Check for article starts
                    art_info = None
                    if language == "ar":
                        art_info = parse_arabic_article_header(stripped_line)
                    else:
                        art_info = parse_french_article_header(stripped_line)
                        
                    if art_info:
                        # Save the previous article if we had one
                        if current_article:
                            articles.append(current_article)
                            
                        norm_num, display_num, is_new = art_info
                        article_id = f"{self.code_id}:article-{norm_num}"
                        
                        current_article = {
                            "article_id": article_id,
                            "code_id": self.code_id,
                            "article_number": norm_num,
                            "display_number_ar": display_num if language == "ar" else "",
                            "display_number_fr": display_num if language == "fr" else "",
                            "language": language,
                            "hierarchy_path": self.get_hierarchy_path(),
                            "text_ar": "",
                            "text_fr": "",
                            "valid_from": self.default_valid_from,
                            "valid_to": "9999-12-31",
                            "status": "active",
                            "source_ref": {
                                "source_id": record["source_id"],
                                "page_ids": [page_id],
                                "blocks": [block_id],
                                "spans": []
                            },
                            "paragraphs": []
                        }
                        
                        # If there is body text after the header on the same line, append it
                        header_match = stripped_line.find(display_num)
                        body_part = stripped_line[header_match + len(display_num):].strip("() :.-")
                        if body_part:
                            if language == "ar":
                                current_article["text_ar"] = body_part
                            else:
                                current_article["text_fr"] = body_part
                                
                            current_article["paragraphs"].append({
                                "paragraph_index": 1,
                                "text_ar": body_part if language == "ar" else "",
                                "text_fr": body_part if language == "fr" else "",
                                "source_spans": [{
                                    "page_id": page_id,
                                    "block_id": block_id,
                                    "char_start": raw_text.find(body_part),
                                    "char_end": raw_text.find(body_part) + len(body_part)
                                }]
                            })
                        continue
                        
                    # Check for table blocks
                    block_type = block.get("type", "article_body")
                    if block_type == "table" and current_article:
                        if page_id not in current_article["source_ref"]["page_ids"]:
                            current_article["source_ref"]["page_ids"].append(page_id)
                        if block_id not in current_article["source_ref"]["blocks"]:
                            current_article["source_ref"]["blocks"].append(block_id)
                            
                        p_idx = len(current_article["paragraphs"]) + 1
                        current_article["paragraphs"].append({
                            "paragraph_index": p_idx,
                            "type": "table",
                            "text_ar": raw_text if language == "ar" else "",
                            "text_fr": raw_text if language == "fr" else "",
                            "caption": block.get("caption", ""),
                            "rows": block.get("rows", []),
                            "columns": block.get("columns", []),
                            "source_spans": [{
                                "page_id": page_id,
                                "block_id": block_id,
                                "char_start": 0,
                                "char_end": len(raw_text)
                            }]
                        })
                        continue
                        
                    # Accumulate text to the current article body
                    if current_article:
                        if page_id not in current_article["source_ref"]["page_ids"]:
                            current_article["source_ref"]["page_ids"].append(page_id)
                        if block_id not in current_article["source_ref"]["blocks"]:
                            current_article["source_ref"]["blocks"].append(block_id)
                            
                        char_start = raw_text.find(stripped_line)
                        char_end = char_start + len(stripped_line) if char_start >= 0 else 0
                        
                        if language == "ar":
                            if current_article["text_ar"]:
                                current_article["text_ar"] += " " + stripped_line
                            else:
                                current_article["text_ar"] = stripped_line
                        else:
                            if current_article["text_fr"]:
                                current_article["text_fr"] += " " + stripped_line
                            else:
                                current_article["text_fr"] = stripped_line
                                
                        # Simple paragraph append (treat line as paragraph for trace)
                        p_idx = len(current_article["paragraphs"]) + 1
                        current_article["paragraphs"].append({
                            "paragraph_index": p_idx,
                            "text_ar": stripped_line if language == "ar" else "",
                            "text_fr": stripped_line if language == "fr" else "",
                            "source_spans": [{
                                "page_id": page_id,
                                "block_id": block_id,
                                "char_start": char_start,
                                "char_end": char_end
                            }]
                        })
                        
        # Append the final article
        if current_article:
            articles.append(current_article)
            
        return articles

def align_bilingual_articles(ar_articles: List[Dict[str, Any]], fr_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aligns Arabic and French articles based on normalized article number."""
    aligned_map: Dict[str, Dict[str, Any]] = {}
    
    # Process Arabic articles
    for art in ar_articles:
        num = art["article_number"]
        aligned_map[num] = art
        aligned_map[num]["language"] = "bilingual"
        
    # Merge French articles
    for art in fr_articles:
        num = art["article_number"]
        if num in aligned_map:
            # Merge
            aligned_map[num]["display_number_fr"] = art["display_number_fr"]
            aligned_map[num]["text_fr"] = art["text_fr"]
            # Merge source references
            aligned_map[num]["source_ref"]["page_ids"] = list(set(aligned_map[num]["source_ref"]["page_ids"] + art["source_ref"]["page_ids"]))
            aligned_map[num]["source_ref"]["blocks"] = list(set(aligned_map[num]["source_ref"]["blocks"] + art["source_ref"]["blocks"]))
            # Combine paragraphs
            aligned_map[num]["paragraphs"].extend(art["paragraphs"])
        else:
            # French only
            art["language"] = "bilingual"
            aligned_map[num] = art
            
    # Sort by article number (converting to float/tuple if possible for clean sorting)
    def get_sort_key(num: str) -> tuple:
        match = re.match(r"^(\d+)(?:-(.+))?$", num)
        if match:
            val = int(match.group(1))
            suffix = match.group(2) or ""
            return (val, suffix)
        return (9999, num)
        
    sorted_nums = sorted(aligned_map.keys(), key=get_sort_key)
    return [aligned_map[num] for num in sorted_nums]

def run_parser_pipeline(ocr_jsonl_path: str, code_id: str, default_valid_from: str = "2000-01-01") -> List[Dict[str, Any]]:
    """Runs the parser pipeline on a single language OCR JSONL file."""
    if not os.path.exists(ocr_jsonl_path):
        raise FileNotFoundError(f"OCR input file not found: {ocr_jsonl_path}")
        
    records = []
    with open(ocr_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
                
    # Detect language of the source from the first record
    lang = "ar"
    if records:
        for b in records[0].get("blocks", []):
            if b.get("language"):
                lang = b["language"]
                break
                
    parser = DocumentParser(code_id, default_valid_from)
    return parser.parse_blocks(records, lang)
