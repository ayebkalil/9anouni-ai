"""
Comprehensive Parser for:
1. Constitution 2022 (French: Constitution-de-la-Republique-Tunisienne-du-25-juillet-2022-2.pdf)
2. Constitution 2022 (Arabic: constitution-2022.pdf / OCR extracted)
3. Code du Travail (French: code de travail.pdf)
4. Code du Travail (Arabic: مجلة الشغل.pdf)
"""

import os
import sys
import re
import json
import uuid
import fitz
from typing import Dict, List, Any

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Comprehensive Arabic ordinal mapping
ARABIC_NUM_WORDS = [
    (142, [r'الثاني\s+والأربعون\s+بعد\s+المائة', r'142']),
    (141, [r'الحادي\s+والأربعون\s+بعد\s+المائة', r'141']),
    (140, [r'الأربعون\s+بعد\s+المائة', r'140']),
    (139, [r'التاسع\s+والثلاثون\s+بعد\s+المائة', r'139']),
    (138, [r'الثامن\s+والثلاثون\s+بعد\s+المائة', r'138']),
    (137, [r'السابع\s+والثلاثون\s+بعد\s+المائة', r'137']),
    (136, [r'السادس\s+والثلاثون\s+بعد\s+المائة', r'136']),
    (135, [r'الخامس\s+والثلاثون\s+بعد\s+المائة', r'135']),
    (134, [r'الرابع\s+والثلاثون\s+بعد\s+المائة', r'134']),
    (133, [r'الثالث\s+والثلاثون\s+بعد\s+المائة', r'133']),
    (132, [r'الثاني\s+والثلاثون\s+بعد\s+المائة', r'132']),
    (131, [r'الحادي\s+والثلاثون\s+بعد\s+المائة', r'131']),
    (130, [r'الثلاثون\s+بعد\s+المائة', r'130']),
    (129, [r'التاسع\s+والعشرون\s+بعد\s+المائة', r'129']),
    (128, [r'الثامن\s+والعشرون\s+بعد\s+المائة', r'128']),
    (127, [r'السابع\s+والعشرون\s+بعد\s+المائة', r'127']),
    (126, [r'السادس\s+والعشرون\s+بعد\s+المائة', r'126']),
    (125, [r'المائة\s+وخمسة\s+وعشرون', r'الخامس\s+والعشرون\s+بعد\s+المائة', r'125']),
    (124, [r'المائة\s+وأربعة\s+وعشرون', r'الرابع\s+والعشرون\s+بعد\s+المائة', r'124']),
    (123, [r'المائة\s+وثلاثة\s+وعشرون', r'الثالث\s+والعشرون\s+بعد\s+المائة', r'123']),
    (122, [r'المائة\s+واثنان\s+وعشرون', r'الثاني\s+والعشرون\s+بعد\s+المائة', r'122']),
    (121, [r'المائة\s+واحد\s+وعشرون', r'الحادي\s+والعشرون\s+بعد\s+المائة', r'121']),
    (120, [r'المائة\s+والعشرون', r'العشرون\s+بعد\s+المائة', r'120']),
    (119, [r'المائة\s+وتسعة\s+عشر', r'التاسع\s+عشر\s+بعد\s+المائة', r'119']),
    (118, [r'المائة\s+وثمانية\s+عشر', r'الثامن\s+عشر\s+بعد\s+المائة', r'118']),
    (117, [r'المائة\s+وسبعة\s+عشر', r'السابع\s+عشر\s+بعد\s+المائة', r'117']),
    (116, [r'المائة\s+وستة\s+عشر', r'السادس\s+عشر\s+بعد\s+المائة', r'116']),
    (115, [r'المائة\s+وخمسة\s+عشر', r'الخامس\s+عشر\s+بعد\s+المائة', r'115']),
    (114, [r'المائة\s+وأربعة\s+عشر', r'الرابع\s+عشر\s+بعد\s+المائة', r'114']),
    (113, [r'المائة\s+وثلاثة\s+عشر', r'الثالث\s+عشر\s+بعد\s+المائة', r'113']),
    (112, [r'المائة\s+واثنا\s+عشر', r'الثاني\s+عشر\s+بعد\s+المائة', r'112']),
    (111, [r'المائة\s+وأحد\s+عشر', r'الحادي\s+عشر\s+بعد\s+المائة', r'111']),
    (110, [r'المائة\s+والعاشر', r'العاشر\s+بعد\s+المائة', r'110']),
    (109, [r'المائة\s+والتاسع', r'التاسع\s+بعد\s+المائة', r'109']),
    (108, [r'المائة\s+والثامن', r'الثامن\s+بعد\s+المائة', r'108']),
    (107, [r'المائة\s+والسابع', r'السابع\s+بعد\s+المائة', r'107']),
    (106, [r'المائة\s+والسادس', r'السادس\s+بعد\s+المائة', r'106']),
    (105, [r'المائة\s+والخامس', r'الخامس\s+بعد\s+المائة', r'105']),
    (104, [r'المائة\s+والرابع', r'الرابع\s+بعد\s+المائة', r'104']),
    (103, [r'المائة\s+والثالث', r'الثالث\s+بعد\s+المائة', r'103']),
    (102, [r'المائة\s+والثاني', r'الثاني\s+بعد\s+المائة', r'102']),
    (101, [r'المائة\s+والأول', r'المائة\s+والحادي', r'الحادي\s+بعد\s+المائة', r'101']),
    (100, [r'المائة', r'100']),
    (99, [r'التاسع\s+والتسعون', r'99']),
    (98, [r'الثامن\s+والتسعون', r'98']),
    (97, [r'السابع\s+والتسعون', r'97']),
    (96, [r'السادس\s+والتسعون', r'96']),
    (95, [r'الخامس\s+والتسعون', r'95']),
    (94, [r'الرابع\s+والتسعون', r'94']),
    (93, [r'الثالث\s+والتسعون', r'93']),
    (92, [r'الثاني\s+والتسعون', r'92']),
    (91, [r'الحادي\s+والتسعون', r'91']),
    (90, [r'التسعون', r'90']),
    (89, [r'التاسع\s+والثمانون', r'89']),
    (88, [r'الثامن\s+والثمانون', r'88']),
    (87, [r'السابع\s+والثمانون', r'87']),
    (86, [r'السادس\s+والثمانون', r'86']),
    (85, [r'الخامس\s+والثمانون', r'85']),
    (84, [r'الرابع\s+والثمانون', r'84']),
    (83, [r'الثالث\s+والثمانون', r'83']),
    (82, [r'الثاني\s+والثمانون', r'82']),
    (81, [r'الحادي\s+والثمانون', r'81']),
    (80, [r'الثمانون', r'80']),
    (79, [r'التاسع\s+والسبعون', r'79']),
    (78, [r'الثامن\s+والسبعون', r'78']),
    (77, [r'السابع\s+والسبعون', r'77']),
    (76, [r'السادس\s+والسبعون', r'76']),
    (75, [r'الخامس\s+والسبعون', r'75']),
    (74, [r'الرابع\s+والسبعون', r'74']),
    (73, [r'الثالث\s+والسبعون', r'73']),
    (72, [r'الثاني\s+والسبعون', r'72']),
    (71, [r'الحادي\s+والسبعون', r'71']),
    (70, [r'السبعون', r'70']),
    (69, [r'التاسع\s+والستون', r'69']),
    (68, [r'الثامن\s+والستون', r'68']),
    (67, [r'السابع\s+والستون', r'67']),
    (66, [r'السادس\s+والستون', r'66']),
    (65, [r'الخامس\s+والستون', r'65']),
    (64, [r'الرابع\s+والستون', r'64']),
    (63, [r'الثالث\s+والستون', r'63']),
    (62, [r'الثاني\s+والستون', r'62']),
    (61, [r'الحادي\s+والستون', r'61']),
    (60, [r'الستون', r'60']),
    (59, [r'التاسع\s+والخمسون', r'59']),
    (58, [r'الثامن\s+والخمسون', r'58']),
    (57, [r'السابع\s+والخمسون', r'57']),
    (56, [r'السادس\s+والخمسون', r'56']),
    (55, [r'الخامس\s+والخمسون', r'55']),
    (54, [r'الرابع\s+والخمسون', r'54']),
    (53, [r'الثالث\s+والخمسون', r'53']),
    (52, [r'الثاني\s+والخمسون', r'52']),
    (51, [r'الحادي\s+والخمسون', r'51']),
    (50, [r'الخمسون', r'50']),
    (49, [r'التاسع\s+والأربعون', r'49']),
    (48, [r'الثامن\s+والأربعون', r'48']),
    (47, [r'السابع\s+والأربعون', r'47']),
    (46, [r'السادس\s+والأربعون', r'46']),
    (45, [r'الخامس\s+والأربعون', r'45']),
    (44, [r'الرابع\s+والأربعون', r'44']),
    (43, [r'الثالث\s+والأربعون', r'43']),
    (42, [r'الثاني\s+والأربعون', r'42']),
    (41, [r'الحادي\s+والأربعون', r'41']),
    (40, [r'الأربعون', r'40']),
    (39, [r'التاسع\s+والثلاثون', r'39']),
    (38, [r'الثامن\s+والثلاثون', r'38']),
    (37, [r'السابع\s+والثلاثون', r'37']),
    (36, [r'السادس\s+والثلاثون', r'36']),
    (35, [r'الخامس\s+والثلاثون', r'35']),
    (34, [r'الرابع\s+والثلاثون', r'34']),
    (33, [r'الثالث\s+والثلاثون', r'33']),
    (32, [r'الثاني\s+والثلاثون', r'32']),
    (31, [r'الحادي\s+والثلاثون', r'31']),
    (30, [r'الثلاثون', r'30']),
    (29, [r'التاسع\s+والعشرون', r'29']),
    (28, [r'الثامن\s+والعشرون', r'28']),
    (27, [r'السابع\s+والعشرون', r'27']),
    (26, [r'السادس\s+والعشرون', r'26']),
    (25, [r'الخامس\s+والعشرون', r'25']),
    (24, [r'الرابع\s+والعشرون', r'24']),
    (23, [r'الثالث\s+والعشرون', r'23']),
    (22, [r'الثاني\s+والعشرون', r'22']),
    (21, [r'الحادي\s+والعشرون', r'21']),
    (20, [r'العشرون', r'20']),
    (19, [r'التاسع\s+عشر', r'19']),
    (18, [r'الثامن\s+عشر', r'18']),
    (17, [r'السابع\s+عشر', r'17']),
    (16, [r'السادس\s+عشر', r'16']),
    (15, [r'الخامس\s+عشر', r'15']),
    (14, [r'الرابع\s+عشر', r'14']),
    (13, [r'الثالث\s+عشر', r'13']),
    (12, [r'الثاني\s+عشر', r'12']),
    (11, [r'الحادي\s+عشر', r'11']),
    (10, [r'العاشر', r'10']),
    (9, [r'التاسع', r'9']),
    (8, [r'الثامن', r'8']),
    (7, [r'السابع', r'7']),
    (6, [r'السادس|السسادس', r'6']),
    (5, [r'الخامس', r'5']),
    (4, [r'الرابع', r'4']),
    (3, [r'الثالث', r'3']),
    (2, [r'الثاني', r'2']),
    (1, [r'الأول', r'الأولى', r'1'])
]

def parse_constitution_2022_fr() -> Dict[str, Dict[str, Any]]:
    pdf_path = os.path.join(project_root, "Constitution-de-la-Republique-Tunisienne-du-25-juillet-2022-2.pdf")
    if not os.path.exists(pdf_path):
        return {}

    doc = fitz.open(pdf_path)
    full_text = "\n".join([p.get_text("text") for p in doc])
    
    full_text = re.sub(r'Page \d+ sur \d+', '', full_text)
    full_text = re.sub(r'Base de données.*?\n', '', full_text)
    full_text = re.sub(r'www\.legislation-securite\.tn', '', full_text, flags=re.IGNORECASE)
    full_text = re.sub(r'Accès aux lois.*?\n', '', full_text)
    full_text = re.sub(r'(?:^|\n)\s*Article\s+premier\s*[-–—:]?\s*', '\nArt. 1 – ', full_text, flags=re.IGNORECASE)

    pattern = re.compile(r'(?:^|\n)\s*(?:Art\s*\.?|Article)\s*(\d+)\s*[-–—:]\s*', re.IGNORECASE)
    matches = list(pattern.finditer(full_text))

    articles = {}
    current_chapter = "Chapitre I – Dispositions générales"
    
    for i in range(len(matches)):
        art_num = matches[i].group(1)
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(full_text)
        chunk = full_text[start:end].strip()

        pre_chunk = full_text[max(0, start-300):start]
        chap_match = re.findall(r'(Chapitre\s+[IVXLCDM\w]+\s*[-–—]\s*[^\n]+)', pre_chunk)
        if chap_match:
            current_chapter = chap_match[-1].strip()

        clean_text = re.sub(r'\s+', ' ', chunk).strip()
        articles[art_num] = {
            "article_number": art_num,
            "hierarchy_path": current_chapter,
            "text_fr": clean_text
        }
    
    return articles

def parse_constitution_2022_ar() -> Dict[str, str]:
    ocr_path = os.path.join(project_root, "data", "constitution_2022_ocr_ar.txt")
    if not os.path.exists(ocr_path):
        return {}

    with open(ocr_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = re.sub(r'=== Page \d+ ===', '', text)
    text = re.sub(r'وست[ورر]+\s*[\d\s]*الجمهوري[ةه]\s*التونسي[ةه][\d\s]*', '', text)
    text = re.sub(r'الجمهوري[ةه]\s*التونسي[ةه]\s*[\d\s]*', '', text)

    # Standardize all Arabic article headers to: \nالفصل X - 
    for num, words in ARABIC_NUM_WORDS:
        for w in words:
            pattern = r'(?:^|\n)\s*الفصل\s+' + w + r'[:\s\.]*'
            text = re.sub(pattern, f'\n###ARTICLE_{num}###\n', text)

    articles_ar = {}
    for num in range(1, 143):
        tag = f"###ARTICLE_{num}###"
        if tag in text:
            parts = text.split(tag, 1)[1]
            # Next article tag
            next_tag_m = re.search(r'###ARTICLE_\d+###', parts)
            chunk = parts[:next_tag_m.start()] if next_tag_m else parts
            clean_chunk = re.sub(r'\s+', ' ', chunk).strip()
            articles_ar[str(num)] = f"الفصل {num} - " + clean_chunk

    return articles_ar

def parse_code_du_travail_fr() -> Dict[str, Dict[str, Any]]:
    pdf_path = os.path.join(project_root, "code de travail.pdf")
    if not os.path.exists(pdf_path):
        return {}

    doc = fitz.open(pdf_path)
    full_text = "\n".join([doc[p].get_text("text") for p in range(5, len(doc))])
    
    full_text = re.sub(r"Imprimerie Officielle de la République Tunisienne", "", full_text)
    full_text = re.sub(r"CODE DU TRAVAIL", "", full_text)
    full_text = re.sub(r"-\s*\d+\s*-", "", full_text)
    full_text = re.sub(r'(?:^|\n)\s*Article\s+premier\s*[-–—:\.]\s*', '\nArticle 1 - ', full_text, flags=re.IGNORECASE)

    pattern = re.compile(
        r'(?:^|\n)\s*(Article|Art\.)\s*(\d+(?:[-–]\d+|\s*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies))?)\s*[-–—:\.]\s*',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(full_text))

    articles = {}
    current_hierarchy = "Code du Travail > Dispositions Générales"

    for i in range(len(matches)):
        art_tag = matches[i].group(2).strip()
        art_key = re.sub(r'\s+', ' ', art_tag)
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(full_text)
        chunk = full_text[start:end].strip()

        pre_chunk = full_text[max(0, start-400):start]
        livre_m = re.findall(r'(LIVRE\s+[IVXLCDM\w]+[^\n]*)', pre_chunk, flags=re.IGNORECASE)
        titre_m = re.findall(r'(TITRE\s+[IVXLCDM\w]+[^\n]*)', pre_chunk, flags=re.IGNORECASE)
        chap_m = re.findall(r'(CHAPITRE\s+[IVXLCDM\w]+[^\n]*)', pre_chunk, flags=re.IGNORECASE)
        
        path_parts = ["Code du Travail"]
        if livre_m: path_parts.append(livre_m[-1].strip())
        if titre_m: path_parts.append(titre_m[-1].strip())
        if chap_m: path_parts.append(chap_m[-1].strip())
        current_hierarchy = " > ".join(path_parts)

        clean_text = re.sub(r'\s+', ' ', chunk).strip()
        if len(clean_text) > 20:
            articles[art_key] = {
                "article_number": art_key,
                "hierarchy_path": current_hierarchy,
                "text_fr": clean_text
            }

    return articles

def parse_code_du_travail_ar() -> Dict[str, Dict[str, Any]]:
    pdf_path = os.path.join(project_root, "مجلة الشغل.pdf")
    if not os.path.exists(pdf_path):
        return {}

    doc = fitz.open(pdf_path)
    full_text = "\n".join([doc[p].get_text("text") for p in range(2, len(doc))])
    
    full_text = re.sub(r'(?:^|\n)\s*\d+\s*(?:\n|$)', '\n', full_text)
    full_text = re.sub(r'الجمهورية التونسية\s*مجلـة الشغـل', '', full_text)

    pattern = re.compile(
        r'(?:^|\n)\s*الفصل\s*(\d+(?:[-–]\d+|\s*(?:مكرر|أولا|ثانيا|ثالثا|رابعا|خامسا|سادسا|سابعا|ثامنا|تاسعا|عاشرا))?)\s*[-–—:\.]?\s*',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(full_text))

    articles = {}
    current_hierarchy = "مجلة الشغل > أحكام عامة"

    for i in range(len(matches)):
        art_tag = matches[i].group(1).strip()
        art_key = re.sub(r'\s+', ' ', art_tag)
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(full_text)
        chunk = full_text[start:end].strip()

        pre_chunk = full_text[max(0, start-400):start]
        kitab_m = re.findall(r'(الكتاب\s+[^\n]+)', pre_chunk)
        bab_m = re.findall(r'(الباب\s+[^\n]+)', pre_chunk)
        unwan_m = re.findall(r'(العنوان\s+[^\n]+)', pre_chunk)

        path_parts = ["مجلة الشغل"]
        if kitab_m: path_parts.append(kitab_m[-1].strip())
        if unwan_m: path_parts.append(unwan_m[-1].strip())
        if bab_m: path_parts.append(bab_m[-1].strip())
        current_hierarchy = " > ".join(path_parts)

        clean_text = re.sub(r'\s+', ' ', chunk).strip()
        if len(clean_text) > 15:
            articles[art_key] = {
                "article_number": art_key,
                "hierarchy_path": current_hierarchy,
                "text_ar": clean_text
            }

    return articles
