import os
import sys
from typing import Any, Dict, List, Optional
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.ingestion.models import LegalArticleVersion

# Ensure Gemini is configured
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(project_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)

def get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """
    Generates dense vector embeddings using Google's text-embedding-004 model.
    """
    configure_gemini()
    model = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
    if not model.startswith("models/"):
        model = f"models/{model}"
        
    result = genai.embed_content(
        model=model,
        content=text,
        task_type=task_type,
    )
    return result["embedding"]

class LegalVectorStore:
    """
    ChromaDB Vector Store interface for 9anouni AI Legal Search (Pillar C).
    """
    def __init__(self, persist_dir: Optional[str] = None):
        if not persist_dir:
            persist_dir = os.path.join(project_root, "chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="tunisian_legal_articles",
            metadata={"hnsw:space": "cosine"}
        )

    def index_database_articles(self):
        """
        Extracts all active legal articles from PostgreSQL and inserts them into ChromaDB.
        """
        configure_gemini()
        from dotenv import load_dotenv
        load_dotenv(os.path.join(project_root, ".env"))
        
        db_url = os.getenv("DATABASE_URL")
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        articles = session.query(LegalArticleVersion).filter(
            LegalArticleVersion.status == "active"
        ).all()

        print(f"Indexing {len(articles)} active articles into ChromaDB...")
        
        documents = []
        metadatas = []
        ids = []
        embeddings = []

        for article in articles:
            # Combine Arabic and French text with hierarchy metadata
            doc_text = f"[{article.code_id} - Article {article.article_number}]\n"
            doc_text += f"Hierarchy: {article.hierarchy_path}\n"
            doc_text += f"Arabic: {article.text_ar}\n"
            if article.text_fr:
                doc_text += f"French: {article.text_fr}\n"

            try:
                emb = get_embedding(doc_text, task_type="RETRIEVAL_DOCUMENT")
                embeddings.append(emb)
                documents.append(doc_text)
                ids.append(article.version_id)
                metadatas.append({
                    "version_id": str(article.version_id),
                    "article_id": str(article.article_id),
                    "code_id": str(article.code_id),
                    "article_number": str(article.article_number),
                    "hierarchy_path": str(article.hierarchy_path),
                    "valid_from": str(article.valid_from),
                    "valid_to": str(article.valid_to) if article.valid_to else "active",
                    "has_french": bool(article.text_fr)
                })
            except Exception as e:
                print(f"Error embedding article {article.article_id}: {e}")

        if ids:
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            print(f"Successfully indexed {len(ids)} articles into ChromaDB!")

        session.close()

    def search_vector(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes dense vector similarity search against ChromaDB.
        """
        query_embedding = get_embedding(query, task_type="RETRIEVAL_QUERY")
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        matched_items = []
        if results and results.get("ids") and len(results["ids"][0]) > 0:
            for idx in range(len(results["ids"][0])):
                distance = results["distances"][0][idx]
                similarity = 1.0 - distance  # Cosine similarity
                matched_items.append({
                    "id": results["ids"][0][idx],
                    "document": results["documents"][0][idx],
                    "metadata": results["metadatas"][0][idx],
                    "similarity_score": similarity,
                    "rank": idx + 1
                })
        return matched_items

if __name__ == "__main__":
    store = LegalVectorStore()
    store.index_database_articles()
    print("Vector Store Ready!")
