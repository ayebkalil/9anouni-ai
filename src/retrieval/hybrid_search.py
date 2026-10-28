import os
import sys
import re
from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

def get_db_session():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_root, ".env"))
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

# Stopwords to filter out from search queries
STOPWORDS = {
    "ما", "هي", "هو", "كيف", "في", "من", "على", "إلى", "عن", "مع", "هذا", "هذه", "التي", "الذي", "أن", "إن",
    "وفقا", "وفق", "حسب", "طبق", "طبقا", "ماذا", "هل", "بين", "حول", "كل", "أو", "موقف", "القانون", "قانون", "التونسي", "تونس",
    "quel", "quelle", "quelles", "quels", "comment", "pourquoi", "dans", "sur", "avec", "pour", "par", "les", "des", "une", "un", "le", "la", "selon", "dapres", "loi", "tunisienne", "tunisien"
}

# Domain intent mapping for automatic boosting
CODE_INTENT_KEYWORDS = {
    "constitution_2022": ["دستور", "الدستور", "سيادة", "حقوق", "حريات", "رئيس", "جمهورية", "constitution"],
    "labor_code": ["شغل", "الشغل", "عامل", "أجير", "مؤجر", "طرد", "تعسفي", "إضراب", "نقابي", "أجور", "عطلة", "تجربة", "travail", "salarié", "licenciement", "préavis", "indemnité", "essai"],
    "personal_status_code": ["أحوال", "شخصية", "زواج", "الزواج", "زوج", "زوجة", "طلاق", "الطلاق", "حضانة", "نفقة", "ميراث", "تعدد", "mariage", "divorce", "garde", "époux", "polygamie"]
}

def extract_keywords(query: str) -> List[str]:
    # Clean punctuation
    query_clean = re.sub(r'[\?؟\.,!؛:()\-_\'"]', ' ', query)
    tokens = re.findall(r'[\w\u0600-\u06FF]+', query_clean.lower())
    clean_tokens = []
    for t in tokens:
        if t in STOPWORDS or len(t) < 3:
            continue
        # Strip common Arabic prefixes if applicable
        if t.startswith('و') and len(t) > 3 and t[1:] not in STOPWORDS:
            t = t[1:]
        elif t.startswith('ل') and len(t) > 3 and t[1:] not in STOPWORDS:
            t = t[1:]
        elif t.startswith('ب') and len(t) > 3 and t[1:] not in STOPWORDS:
            t = t[1:]
            
        if t not in STOPWORDS and len(t) >= 3 and t not in clean_tokens:
            clean_tokens.append(t)
            
    return clean_tokens or tokens

class HybridLegalSearch:
    """
    Hybrid Search Engine combining Lexical Keyword Search (PostgreSQL) and 
    Semantic / Fallback Search with Reciprocal Rank Fusion (RRF).
    """
    def __init__(self, vector_store=None):
        self.vector_store = vector_store

    def search_lexical(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Performs multi-token keyword matching against PostgreSQL legal_article_version table.
        """
        session = get_db_session()
        keywords = extract_keywords(query)
        
        if not keywords:
            keywords = [query.strip()]

        # Detect code intent
        query_lower = query.lower()
        boosted_codes = []
        for code_key, trigger_words in CODE_INTENT_KEYWORDS.items():
            if any(w in query_lower for w in trigger_words):
                boosted_codes.append(code_key)

        # Build dynamic SQL matching keywords across Arabic, French, and metadata
        conditions = []
        params: Dict[str, Any] = {"limit": 250}
        
        for idx, kw in enumerate(keywords[:12]):
            pname = f"kw_{idx}"
            params[pname] = f"%{kw}%"
            conditions.append(f"(text_ar ILIKE :{pname} OR text_fr ILIKE :{pname} OR hierarchy_path ILIKE :{pname} OR article_number ILIKE :{pname} OR code_id ILIKE :{pname})")

        # If a specific code domain is identified, also explicitly include its articles in the candidate pool
        if boosted_codes:
            for b_idx, b_code in enumerate(boosted_codes):
                bpname = f"bcode_{b_idx}"
                params[bpname] = b_code
                conditions.append(f"code_id = :{bpname}")

        where_clause = " OR ".join(conditions) if conditions else "1=1"
        
        sql = text(f"""
            SELECT version_id, article_id, code_id, article_number, hierarchy_path, 
                   text_ar, text_fr, valid_from, valid_to
            FROM legal_article_version
            WHERE status = 'active' AND ({where_clause})
            LIMIT :limit;
        """)
        
        results = session.execute(sql, params).fetchall()
        session.close()

        lexical_items = []
        for idx, row in enumerate(results):
            matched_count = 0
            combined_text = f"{row.text_ar or ''} {row.text_fr or ''} {row.hierarchy_path or ''}".lower()
            
            # Count exact keyword occurrences
            for kw in keywords:
                if kw in combined_text:
                    matched_count += 1

            # Give a strong boost if the article belongs to the detected legal intent domain
            if str(row.code_id) in boosted_codes:
                matched_count += 5

            lexical_items.append({
                "id": str(row.version_id),
                "article_id": str(row.article_id),
                "code_id": str(row.code_id),
                "article_number": str(row.article_number),
                "hierarchy_path": str(row.hierarchy_path),
                "text_ar": row.text_ar,
                "text_fr": row.text_fr,
                "matched_keywords": matched_count,
                "rank": idx + 1
            })
            
        # Sort by matched keywords count descending
        lexical_items.sort(key=lambda x: x["matched_keywords"], reverse=True)
        return lexical_items[:top_k]

    def search_hybrid(self, query: str, top_k: int = 5, k_rrf: int = 60) -> List[Dict[str, Any]]:
        """
        Executes Reciprocal Rank Fusion (RRF) between tokenized lexical and vector search.
        """
        lexical_results = self.search_lexical(query, top_k=top_k * 2)
        
        # If vector store is available, merge results
        vector_results = []
        if self.vector_store:
            try:
                vector_results = self.vector_store.search_vector(query, top_k=top_k * 2)
            except Exception as e:
                pass

        rrf_scores: Dict[str, float] = {}
        items_map: Dict[str, Dict[str, Any]] = {}

        for idx, item in enumerate(lexical_results):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + idx + 1))
            items_map[doc_id] = {
                "version_id": doc_id,
                "article_id": item["article_id"],
                "code_id": item["code_id"],
                "article_number": item["article_number"],
                "hierarchy_path": item["hierarchy_path"],
                "text_ar": item["text_ar"],
                "text_fr": item["text_fr"],
                "source": "lexical"
            }

        for idx, item in enumerate(vector_results):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + idx + 1))
            if doc_id not in items_map:
                meta = item["metadata"]
                items_map[doc_id] = {
                    "version_id": doc_id,
                    "article_id": meta.get("article_id"),
                    "code_id": meta.get("code_id"),
                    "article_number": meta.get("article_number"),
                    "hierarchy_path": meta.get("hierarchy_path"),
                    "text_ar": meta.get("text_ar", ""),
                    "text_fr": meta.get("text_fr", ""),
                    "source": "vector"
                }

        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        
        final_results = []
        for doc_id in sorted_ids:
            res_item = items_map[doc_id]
            res_item["rrf_score"] = rrf_scores[doc_id]
            final_results.append(res_item)

        return final_results
