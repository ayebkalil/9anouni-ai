export type ScreenType = 'home' | 'corpus' | 'search' | 'ingestion';

export type Language = 'fr' | 'ar';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  arabicText?: string;
  timestamp: string;
  citations?: {
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  }[];
}

export interface LawArticleVersion {
  year: number;
  label: string;
  lawTitleFr: string;
  lawTitleAr: string;
  codeNameFr: string;
  codeNameAr: string;
  articleNumberFr: string;
  articleNumberAr: string;
  headingFr: string;
  headingAr: string;
  originalTextFr: string;
  originalTextAr: string;
  modifiedTextFr?: string;
  modifiedTextAr?: string;
  strikethroughFr?: string;
  strikethroughAr?: string;
  addedFr?: string;
  addedAr?: string;
  concludingTextFr?: string;
  concludingTextAr?: string;
  changeNoteFr: string;
  changeNoteAr: string;
  jortReference: string;
}

export interface SearchResult {
  id: string;
  relevance: number;
  courtFr: string;
  courtAr: string;
  decisionNumber: string;
  date: string;
  titleFr: string;
  titleAr: string;
  excerptFr: string;
  excerptAr: string;
  categoryFr: string;
  categoryAr: string;
  fullDecision: {
    parties: string;
    summary: string;
    grounds: string[];
    dispositif: string;
    judges: string[];
  };
}

export interface IngestionStream {
  id: string;
  documentId: string;
  source: string;
  phase: string;
  status: 'running' | 'manual' | 'validated';
  confidence: number;
  pagesTotal: number;
  pagesProcessed: number;
}
