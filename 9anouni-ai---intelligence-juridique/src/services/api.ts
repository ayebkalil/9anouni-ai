const API_BASE_URL = 'http://localhost:8000/api';

export interface ChatResponse {
  id: string;
  query: string;
  answerFr: string;
  answerAr: string;
  citations: Array<{
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  }>;
  is_grounded: boolean;
  retrieved_sources?: any[];
}

export interface SearchResultItem {
  id: string;
  article_id: string;
  code_id: string;
  code_label_fr?: string;
  code_label_ar?: string;
  year?: number;
  article_number: string;
  hierarchy_path: string;
  text_ar: string;
  text_fr: string;
  matched_keywords?: number;
  source: string;
}

export interface SearchResponse {
  query: string;
  mode: string;
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  results: SearchResultItem[];
}

export interface LegalCodeSummary {
  code_id: string;
  label_fr: string;
  label_ar: string;
  year: number;
  articles_count: number;
  articles: Array<{
    article_number: string;
    hierarchy_path: string;
    snippet_ar: string;
    snippet_fr: string;
  }>;
}

export interface AdminStatsResponse {
  total_articles: number;
  active_articles: number;
  unique_codes_count: number;
  ocr_avg_confidence: number;
  bilingual_alignment_rate: string;
  database_engine: string;
  llm_engine: string;
}

export const api = {
  async sendChat(query: string, language: string = 'fr'): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, language }),
    });
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  },

  async searchLaws(
    query: string, 
    mode: string = 'hybrid', 
    code_id?: string, 
    page: number = 1, 
    page_size: number = 10
  ): Promise<SearchResponse> {
    const res = await fetch(`${API_BASE_URL}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, mode, code_id, page, page_size }),
    });
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  },

  async getExplorerCodes(): Promise<{ codes: LegalCodeSummary[] }> {
    const res = await fetch(`${API_BASE_URL}/explorer/codes`);
    if (!res.ok) throw new Error('Failed to fetch legal codes');
    return await res.json();
  },

  async getArticleDetail(code_id: string, article_number: string, as_of_date?: string): Promise<any> {
    let url = `${API_BASE_URL}/explorer/article?code_id=${encodeURIComponent(code_id)}&article_number=${encodeURIComponent(article_number)}`;
    if (as_of_date) {
      url += `&as_of_date=${encodeURIComponent(as_of_date)}`;
    }
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch article details');
    return await res.json();
  },

  async getAdminStats(): Promise<AdminStatsResponse> {
    const res = await fetch(`${API_BASE_URL}/admin/stats`);
    if (!res.ok) throw new Error('Failed to fetch admin stats');
    return await res.json();
  },

  async getAdminStreams(): Promise<{ streams: any[] }> {
    const res = await fetch(`${API_BASE_URL}/admin/streams`);
    if (!res.ok) throw new Error('Failed to fetch streams');
    return await res.json();
  },

  async uploadPdf(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/admin/upload-pdf`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to upload and process PDF');
    return await res.json();
  },

  async saveArticle(articleData: {
    code_id: string;
    article_number: string;
    hierarchy_path: string;
    text_ar: string;
    text_fr?: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/admin/save-article`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(articleData),
    });
    if (!res.ok) throw new Error('Failed to save article');
    return await res.json();
  }
};
