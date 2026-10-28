import os
import sys
import json
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from pydantic import BaseModel, Field

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.retrieval.hybrid_search import HybridLegalSearch

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(project_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    if model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.5-flash", "gemini-pro"]:
        model_name = "gemini-3.6-flash"
    return genai.GenerativeModel(model_name)

class LegalCitation(BaseModel):
    code: str = Field(description="Legal code name and article number (e.g. 'Art. 2, COC' or 'Art. 28, LF 2020')")
    label: str = Field(description="Title or descriptive label of the citation")
    type: str = Field(default="article", description="'article', 'jurisprudence', or 'doctrine'")
    snippet: str = Field(description="Direct authentic quote from the statutory text")

class RAGResponse(BaseModel):
    answerFr: str = Field(description="Comprehensive and authoritative legal answer in French based strictly on the provided context")
    answerAr: str = Field(description="Comprehensive and authoritative legal answer in Arabic based strictly on the provided context")
    citations: List[LegalCitation] = []
    is_grounded: bool = True

RAG_SYSTEM_PROMPT = """
You are 9anouni AI (قانوني AI), the authoritative sovereign Tunisian Legal Intelligence Assistant.
Your task is to answer legal questions by reasoning EXCLUSIVELY upon the provided authentic statutory excerpts retrieved from the Official Gazette of the Republic of Tunisia (JORT).

STRICT OPERATIONAL DIRECTIVES:
1. Base all legal conclusions solely upon the provided excerpts. Do NOT hallucinate articles, dates, or penalties.
2. If the provided excerpts do not contain enough facts to answer with certainty, state clearly that the current statutory base does not contain the specific answer.
3. For every legal fact, provide explicit citations to the exact Article Number and Legal Code.
4. Output your response formatted according to the JSON schema containing 'answerFr', 'answerAr', 'citations', and 'is_grounded'.
"""

class LegalRAGEngine:
    """
    Retrieval-Augmented Generation Engine with Grounded Inference for 9anouni AI (Pillar D).
    """
    def __init__(self):
        self.searcher = HybridLegalSearch()

    def generate_legal_answer(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Executes hybrid retrieval and synthesizes a verifiable bilingual answer via Gemini Pro.
        """
        # 1. Hybrid Retrieval (Pillar C)
        retrieved_articles = self.searcher.search_hybrid(query, top_k=top_k)
        
        # 2. Build Context String
        context_parts = []
        for idx, art in enumerate(retrieved_articles, 1):
            part = f"--- Statutory Source {idx} ---\n"
            part += f"Code: {art.get('code_id')}\n"
            part += f"Article Number: {art.get('article_number')}\n"
            part += f"Hierarchy: {art.get('hierarchy_path')}\n"
            if art.get("text_ar"):
                part += f"Arabic Text: {art['text_ar']}\n"
            if art.get("text_fr"):
                part += f"French Text: {art['text_fr']}\n"
            context_parts.append(part)

        context_str = "\n".join(context_parts) if context_parts else "No matching legal articles found."

        # 3. Prompt Gemini Pro
        prompt = f"""{RAG_SYSTEM_PROMPT}

Retrieved Legal Context from PostgreSQL & ChromaDB:
{context_str}

User Legal Question:
{query}

Generate the authoritative bilingual legal response in strict JSON:
"""
        try:
            model = get_gemini_model()
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            data = json.loads(response.text)
            data["retrieved_sources"] = retrieved_articles
            return data
        except Exception as e:
            print(f"RAG Inference error: {e}")
            return {
                "answerFr": f"Une erreur s'est produite lors de l'inférence juridique: {str(e)}",
                "answerAr": f"حدث خطأ أثناء معالجة الاستشارة القانونية: {str(e)}",
                "citations": [],
                "is_grounded": False,
                "retrieved_sources": retrieved_articles
            }

if __name__ == "__main__":
    engine = LegalRAGEngine()
    res = engine.generate_legal_answer("ما هي شروط صحة العقد؟")
    print(json.dumps(res, indent=2, ensure_ascii=False))
