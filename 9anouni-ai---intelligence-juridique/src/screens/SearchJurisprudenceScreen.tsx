import React, { useState, useEffect } from 'react';
import { Language, ScreenType, SearchResult } from '../types';
import { api, SearchResultItem, LegalCodeSummary } from '../services/api';

interface SearchJurisprudenceScreenProps {
  lang: Language;
  onNavigate: (screen: ScreenType) => void;
  onSelectDecision: (decision: SearchResult) => void;
}

export const SearchJurisprudenceScreen: React.FC<SearchJurisprudenceScreenProps> = ({
  lang,
  onNavigate,
}) => {
  const isAr = lang === 'ar';

  const [searchQuery, setSearchQuery] = useState('مداخيل ميزانية الدولة');
  const [activeTab, setActiveTab] = useState<'hybrid' | 'exact' | 'semantic'>('hybrid');
  const [selectedCode, setSelectedCode] = useState<string>('all');
  const [codesList, setCodesList] = useState<LegalCodeSummary[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize] = useState<number>(5);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalResults, setTotalResults] = useState<number>(0);
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [selectedArticleModal, setSelectedArticleModal] = useState<SearchResultItem | null>(null);

  // Fetch codes for the filter dropdown
  useEffect(() => {
    async function loadCodes() {
      try {
        const data = await api.getExplorerCodes();
        if (data && data.codes) {
          setCodesList(data.codes);
        }
      } catch (e) {
        console.warn('Error loading codes filter:', e);
      }
    }
    loadCodes();
    executeSearch('مداخيل ميزانية الدولة', 'hybrid', 'all', 1);
  }, []);

  const executeSearch = async (
    q: string, 
    mode: string = activeTab, 
    code: string = selectedCode, 
    page: number = currentPage
  ) => {
    if (!q.trim()) return;
    setIsSearching(true);
    try {
      const modeParam = mode === 'exact' ? 'lexical' : mode === 'semantic' ? 'semantic' : 'hybrid';
      const data = await api.searchLaws(q, modeParam, code === 'all' ? undefined : code, page, pageSize);
      if (data) {
        setResults(data.results || []);
        setTotalResults(data.total || 0);
        setTotalPages(data.total_pages || 1);
        setCurrentPage(data.page || 1);
      }
    } catch (err) {
      console.warn('Search execution error:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(searchQuery, activeTab, selectedCode, 1);
  };

  const handlePageChange = (newPage: number) => {
    if (newPage < 1 || newPage > totalPages) return;
    setCurrentPage(newPage);
    executeSearch(searchQuery, activeTab, selectedCode, newPage);
  };

  return (
    <div className="w-full min-h-screen bg-[#faf8ff] text-[#131b2e] pt-24 pb-16" dir={isAr ? 'rtl' : 'ltr'}>
      <div className="max-w-[1360px] mx-auto px-4 md:px-12 flex flex-col lg:flex-row gap-8 relative z-10">
        
        {/* Left Sidebar: Filters */}
        <aside className="w-full lg:w-72 shrink-0 pr-0 lg:pr-8 border-b lg:border-b-0 lg:border-r border-[#debfc2]/40 pb-6 lg:pb-0">
          <div className="flex items-center justify-between mb-6 pb-2 border-b border-[#debfc2]/40">
            <h2 className="font-mono text-xs uppercase tracking-wider font-bold text-[#574144] flex items-center gap-1.5">
              <span className="material-symbols-outlined text-sm text-[#881337]">tune</span>
              <span>{isAr ? 'مرشحات البحث' : 'Filtres de Recherche'}</span>
            </h2>
            <button
              onClick={() => {
                setSelectedCode('all');
                executeSearch(searchQuery, activeTab, 'all', 1);
              }}
              className="text-[11px] font-mono text-[#881337] hover:underline"
            >
              {isAr ? 'إعادة ضبط' : 'Réinitialiser'}
            </button>
          </div>

          <div className="space-y-6">
            {/* Legal Code Filter */}
            <div>
              <h3 className="font-mono text-xs font-semibold text-slate-800 mb-3 uppercase tracking-wider">
                {isAr ? 'النص القانوني' : 'Code / Loi Applicable'}
              </h3>
              <select
                value={selectedCode}
                onChange={(e) => {
                  setSelectedCode(e.target.value);
                  executeSearch(searchQuery, activeTab, e.target.value, 1);
                }}
                className="w-full text-xs font-mono bg-white border border-slate-300 rounded-xl p-2.5 text-slate-800 outline-none focus:border-[#881337]"
              >
                <option value="all">{isAr ? 'جميع القوانين والمجلات' : 'Tous les Codes & Lois (528 Articles)'}</option>
                {codesList.map((c) => (
                  <option key={c.code_id} value={c.code_id}>
                    {isAr ? c.label_ar : c.label_fr} ({c.articles_count})
                  </option>
                ))}
              </select>
            </div>

            {/* Quick Keyword Suggestions */}
            <div className="pt-4 border-t border-slate-200">
              <h3 className="font-mono text-xs font-semibold text-slate-800 mb-2 uppercase tracking-wider">
                {isAr ? 'كلمات مفتاحية شائعة' : 'Mots-clés Fréquents'}
              </h3>
              <div className="flex flex-wrap gap-1.5">
                {['مداخيل', 'نفقات', 'الضريبة', 'الشركات', 'العقد', 'الديوانة', 'ميزانية'].map((kw) => (
                  <button
                    key={kw}
                    onClick={() => {
                      setSearchQuery(kw);
                      executeSearch(kw, activeTab, selectedCode, 1);
                    }}
                    className="text-[11px] bg-slate-100 hover:bg-[#881337]/10 hover:text-[#881337] px-2.5 py-1 rounded-lg transition-colors"
                  >
                    {kw}
                  </button>
                ))}
              </div>
            </div>

          </div>
        </aside>

        {/* Right Main Search Results */}
        <main className="flex-1 min-w-0 space-y-6">
          
          {/* Hero Search Bar */}
          <form onSubmit={handleSearchSubmit} className="relative">
            <div className="flex items-center bg-white border-2 border-[#881337]/30 focus-within:border-[#881337] rounded-2xl shadow-sm overflow-hidden p-1.5 transition-all">
              <span className="material-symbols-outlined text-slate-400 pl-3 pr-2 text-xl">search</span>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={isAr ? 'ابحث في نصوص الرائد الرسمي (مثال: نفقات الميزانية، الإعفاء الجبائي)...' : 'Rechercher dans les textes du JORT...'}
                className="flex-1 py-2 px-2 text-sm outline-none bg-transparent text-slate-900"
              />
              <button
                type="submit"
                className="px-6 py-2.5 bg-[#881337] hover:bg-[#640023] text-white rounded-xl text-xs font-bold font-mono tracking-wider flex items-center gap-1.5 transition-colors shrink-0"
              >
                <span>{isAr ? 'بحث' : 'RECHERCHER'}</span>
                <span className="material-symbols-outlined text-sm">arrow_forward</span>
              </button>
            </div>
          </form>

          {/* Search Mode Tabs */}
          <div className="flex items-center gap-3 border-b border-slate-200 pb-3">
            {[
              { id: 'hybrid', labelFr: 'Recherche Hybride (IA)', labelAr: 'بحث هجين بالذكاء الاصطناعي', icon: 'hub' },
              { id: 'exact', labelFr: 'Recherche Exacte (Mots-clés)', labelAr: 'مطابقة دقيقة للكلمات', icon: 'fact_check' },
              { id: 'semantic', labelFr: 'Recherche Sémantique', labelAr: 'بحث دلالي بالمفهوم', icon: 'psychology' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as any);
                  executeSearch(searchQuery, tab.id, selectedCode, 1);
                }}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all ${
                  activeTab === tab.id
                    ? 'bg-[#881337] text-white shadow-xs font-bold'
                    : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'
                }`}
              >
                <span className="material-symbols-outlined text-sm">{tab.icon}</span>
                <span>{isAr ? tab.labelAr : tab.labelFr}</span>
              </button>
            ))}
          </div>

          {/* Results Summary */}
          <div className="flex items-center justify-between text-xs text-slate-500 font-mono">
            <span>
              {isSearching ? (
                <span className="flex items-center gap-1.5 text-[#881337]">
                  <span className="material-symbols-outlined text-sm animate-spin">sync</span>
                  {isAr ? 'جاري البحث في قاعدة البيانات...' : 'Recherche en cours dans PostgreSQL...'}
                </span>
              ) : (
                <>
                  <strong className="text-slate-900">{totalResults}</strong> {isAr ? 'نتيجة مطابقة في الرائد الرسمي' : 'articles officiels trouvés'}
                </>
              )}
            </span>
            <span>Page {currentPage} / {totalPages}</span>
          </div>

          {/* Real Results Cards List */}
          <div className="space-y-4">
            {results.length > 0 ? (
              results.map((res) => (
                <div
                  key={res.id}
                  className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs hover:border-[#881337]/50 transition-all group"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-[#881337]/10 text-[#881337] border border-[#881337]/20">
                        {isAr ? res.code_label_ar : res.code_label_fr} • {isAr ? `الفصل ${res.article_number}` : `Article ${res.article_number}`}
                      </span>
                      <span className="text-xs text-slate-400 font-mono">
                        {res.hierarchy_path}
                      </span>
                    </div>
                    <span className="text-[11px] font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      Authentifié JORT
                    </span>
                  </div>

                  {/* Real Snippets */}
                  <div className="space-y-2 mb-4">
                    <p className="text-sm leading-loose text-slate-900 font-arabic font-medium" dir="rtl">
                      {res.text_ar}
                    </p>
                    {res.text_fr && (
                      <p className="text-xs leading-relaxed text-slate-600 italic" dir="ltr">
                        {res.text_fr}
                      </p>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center gap-3 pt-3 border-t border-slate-100">
                    <button
                      onClick={() => setSelectedArticleModal(res)}
                      className="px-4 py-1.5 bg-[#881337] hover:bg-[#640023] text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
                    >
                      <span className="material-symbols-outlined text-sm">visibility</span>
                      <span>{isAr ? 'عرض النص الكامل' : "Consulter l'Article"}</span>
                    </button>
                    <button
                      onClick={() => {
                        onNavigate('explorer');
                      }}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-medium text-slate-700 flex items-center gap-1.5 transition-colors"
                    >
                      <span className="material-symbols-outlined text-sm">history_edu</span>
                      <span>{isAr ? 'فتح في مستعرض القوانين' : 'Explorer dans le Corpus'}</span>
                    </button>
                  </div>
                </div>
              ))
            ) : (
              !isSearching && (
                <div className="bg-white rounded-2xl p-12 text-center border border-slate-200 text-slate-500">
                  <span className="material-symbols-outlined text-4xl text-slate-300 mb-2">search_off</span>
                  <p className="font-bold text-sm text-slate-800">
                    {isAr ? 'لم يتم العثور على نتائج مطابقة' : 'Aucun article correspondant'}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    {isAr ? 'يرجى تجربة كلمات بحث أخرى أو تغيير مرشح القانون' : 'Essayez avec un autre mot-clé ou sélectionnez tous les codes.'}
                  </p>
                </div>
              )
            )}
          </div>

          {/* Real Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-6">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="w-8 h-8 rounded-lg border border-slate-200 bg-white flex items-center justify-center text-slate-600 disabled:opacity-40 hover:bg-slate-100 transition-colors"
              >
                <span className="material-symbols-outlined text-sm">chevron_left</span>
              </button>

              {Array.from({ length: totalPages }, (_, i) => i + 1).map((pg) => (
                <button
                  key={pg}
                  onClick={() => handlePageChange(pg)}
                  className={`w-8 h-8 rounded-lg text-xs font-mono font-bold transition-all ${
                    currentPage === pg
                      ? 'bg-[#881337] text-white shadow-xs'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {pg}
                </button>
              ))}

              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="w-8 h-8 rounded-lg border border-slate-200 bg-white flex items-center justify-center text-slate-600 disabled:opacity-40 hover:bg-slate-100 transition-colors"
              >
                <span className="material-symbols-outlined text-sm">chevron_right</span>
              </button>
            </div>
          )}

        </main>
      </div>

      {/* Full Article Modal */}
      {selectedArticleModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl border border-slate-200 max-h-[85vh] overflow-y-auto custom-scrollbar">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <div>
                <span className="text-xs font-mono text-[#881337] font-bold uppercase">
                  {selectedArticleModal.code_label_fr}
                </span>
                <h3 className="font-serif-luxury text-xl font-bold text-slate-900">
                  {isAr ? `الفصل ${selectedArticleModal.article_number}` : `Article ${selectedArticleModal.article_number}`}
                </h3>
              </div>
              <button
                onClick={() => setSelectedArticleModal(null)}
                className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600"
              >
                <span className="material-symbols-outlined text-sm">close</span>
              </button>
            </div>

            <div className="p-4 bg-[#faf8ff] rounded-xl border border-[#881337]/10" dir="rtl">
              <h4 className="font-bold text-xs text-[#881337] mb-2">النص الأصلي</h4>
              <p className="text-sm leading-loose text-slate-900 whitespace-pre-wrap font-arabic">
                {selectedArticleModal.text_ar}
              </p>
            </div>

            {selectedArticleModal.text_fr && (
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200" dir="ltr">
                <h4 className="font-bold text-xs text-slate-700 mb-2">Version Française</h4>
                <p className="text-xs leading-relaxed text-slate-800 whitespace-pre-wrap">
                  {selectedArticleModal.text_fr}
                </p>
              </div>
            )}

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedArticleModal(null)}
                className="px-4 py-2 bg-slate-800 text-white rounded-lg text-xs font-medium"
              >
                {isAr ? 'إغلاق' : 'Fermer'}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
