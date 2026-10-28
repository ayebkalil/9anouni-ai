import json
import os
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from pydantic import BaseModel, Field

# Load environment configuration
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")
    
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    return genai.GenerativeModel(model_name)

class LegalAmendment(BaseModel):
    action: str = Field(description="The type of amendment: 'repeal' (إلغاء), 'replace' (تعويض/تنقيح), or 'add' (إضافة)")
    target_code_id: str = Field(description="Canonical internal ID of the modified code (e.g. 'code_irpp_is', 'code_tva', 'commercial_companies_code', 'labor_code', 'finance_law_2020')")
    target_article_number: str = Field(description="The article number being modified or repealed (e.g. '14', '5', '62 bis')")
    summary_fr: Optional[str] = Field(description="Brief summary in French of what was modified")
    summary_ar: Optional[str] = Field(description="Brief summary in Arabic of what was modified")

class AmendmentExtractionResponse(BaseModel):
    has_amendments: bool
    amendments: List[LegalAmendment] = []

EXTRACTION_SYSTEM_PROMPT = """
You are an expert Tunisian Legal Analyst specializing in legislative amendment extraction from the Official Gazette (JORT).
Your task is to analyze an article from a newly promulgated law (such as a Finance Law) and determine if it explicitly modifies, repeals, or adds provisions to another existing Tunisian legal code.

Code ID reference mapping:
- Code de l'IRPP et de l'IS -> 'code_irpp_is'
- Code de la TVA -> 'code_tva'
- Code des Droits d'Enregistrement et de Timbre -> 'code_enregistrement'
- Code des Douanes -> 'code_douane'
- Code des Sociétés Commerciales -> 'commercial_companies_code'
- Code du Travail -> 'labor_code'
- Code de la Comptabilité Publique -> 'code_cp'
- Previous Finance Law (e.g. 2020) -> 'finance_law_2020'

Rules:
1. If the text declares a general new rule without amending a specific prior code/article, set has_amendments=false and amendments=[].
2. Identify all targets accurately.
"""

def extract_amendments_with_gemini(text_ar: str, text_fr: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Uses Gemini Pro to extract structured amendment actions from legal article text.
    """
    try:
        model = get_gemini_client()
        content = f"Arabic Text:\n{text_ar}"
        if text_fr:
            content += f"\n\nFrench Text:\n{text_fr}"
        
        prompt = f"{EXTRACTION_SYSTEM_PROMPT}\n\nAnalyze the following legal text and extract any amendments in JSON format:\n{content}"
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        
        data = json.loads(response.text)
        if isinstance(data, dict) and data.get("has_amendments"):
            return data.get("amendments", [])
        return []
    except Exception as e:
        print(f"Warning: Gemini amendment extraction encountered an issue: {e}")
        return []
