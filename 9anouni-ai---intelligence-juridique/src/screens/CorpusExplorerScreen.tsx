import React, { useState, useEffect } from 'react';
import { Language, ScreenType } from '../types';
import { ASSET_IMAGES } from '../data/legalData';
import { api, LegalCodeSummary } from '../services/api';

interface CorpusExplorerScreenProps {
  lang: Language;
  onNavigate: (screen: ScreenType) => void;
  onOpenCitation: (citation: {
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  }) => void;
}

export const CorpusExplorerScreen: React.FC<CorpusExplorerScreenProps> = ({
  lang,
  onNavigate,
  onOpenCitation,
}) => {
  const isAr = lang === 'ar';

  const [codes, setCodes] = useState<LegalCodeSummary[]>([]);
  const [activeCodeId, setActiveCodeId] = useState<string>('finance_law_2024');
  const [selectedArticleNum, setSelectedArticleNum] = useState<string>('1');
  const [selectedYear, setSelectedYear] = useState<number>(2024);
  const [articleDetail, setArticleDetail] = useState<any>(null);
  const [historyTimeline, setHistoryTimeline] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [copySuccess, setCopySuccess] = useState<boolean>(false);
  const [searchArticleQuery, setSearchArticleQuery] = useState<string>('');

  // 1. Fetch real codes on mount
  useEffect(() => {
    async function loadCodes() {
      try {
        setLoading(true);
        const data = await api.getExplorerCodes();
        if (data && data.codes && data.codes.length > 0) {
          setCodes(data.codes);
          setActiveCodeId(data.codes[0].code_id);
          if (data.codes[0].articles.length > 0) {
            setSelectedArticleNum(data.codes[0].articles[0].article_number);
          }
        }
      } catch (err) {
        console.warn('Could not load codes from backend:', err);
      } finally {
        setLoading(false);
      }
    }
    loadCodes();
  }, []);

  // 2. Fetch real article detail when code or article changes
  useEffect(() => {
    async function loadArticle() {
      if (!activeCodeId || !selectedArticleNum) return;
      try {
        setLoading(true);
        const asOfDate = selectedYear ? `${selectedYear}-12-31` : undefined;
        const data = await api.getArticleDetail(activeCodeId, selectedArticleNum, asOfDate);
        if (data && data.article) {
          setArticleDetail(data.article);
          setHistoryTimeline(data.history || []);
        }
      } catch (err) {
        console.warn('Could not load article detail:', err);
      } finally {
        setLoading(false);
      }
    }
    loadArticle();
  }, [activeCodeId, selectedArticleNum, selectedYear]);

  const activeCode = codes.find((c) => c.code_id === activeCodeId) || codes[0];

  const filteredArticles = activeCode?.articles?.filter((a) =>
    a.article_number.toLowerCase().includes(searchArticleQuery.toLowerCase()) ||
    a.snippet_ar?.includes(searchArticleQuery) ||
    a.snippet_fr?.toLowerCase().includes(searchArticleQuery.toLowerCase())
  ) || [];

  const handleCopyText = () => {
    if (!articleDetail) return;
    const textToCopy = `[${articleDetail.code_label_fr || activeCodeId} - Article ${articleDetail.article_number}]\n\nARABIC:\n${articleDetail.text_ar}\n\nFRENCH:\n${articleDetail.text_fr || ''}`;
    navigator.clipboard.writeText(textToCopy);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  return (
    <div className="flex w-full min-h-screen bg-[#f2f3ff] text-[#131b2e] pt-16">
      
      {/* Side Navigation Bar: Real Codes from Database */}
      <aside 
        className="w-80 bg-white/95 backdrop-blur-xl border-r border-[#debfc2]/40 hidden md:flex flex-col py-6 px-4 shrink-0 shadow-sm z-20"
        dir={isAr ? 'rtl' : 'ltr'}
      >
        {/* Header / Logo */}
        <div 
          onClick={() => onNavigate('home')}
          className="px-4 pb-6 border-b border-slate-200/80 mb-6 flex flex-col items-center text-center cursor-pointer group"
        >
          <img
            src={ASSET_IMAGES.logo}
            alt="9anouni AI Logo"
            className="w-16 h-16 mb-3 rounded-lg object-contain border border-slate-200 p-1 group-hover:scale-105 transition-transform"
          />
          <h2 className="font-serif-luxury text-xl font-bold text-[#640023] tracking-tight">
            {isAr ? 'المجموعة التشريعية الوطنية' : 'Corpus National JORT'}
          </h2>
          <p className="font-mono text-xs text-[#574144] mt-0.5">
            {codes.length} {isAr ? 'نصوص تشريعية مفهرسة' : 'Textes Officiels'}
          </p>
        </div>

        {/* Dynamic Codes List */}
        <div className="flex-1 space-y-2 overflow-y-auto custom-scrollbar pr-1">
          {codes.map((codeItem) => {
            const isActive = codeItem.code_id === activeCodeId;
            return (
              <button
                key={codeItem.code_id}
                onClick={() => {
                  setActiveCodeId(codeItem.code_id);
                  if (codeItem.articles.length > 0) {
                    setSelectedArticleNum(codeItem.articles[0].article_number);
                  }
                  setSelectedYear(codeItem.year);
                }}
                className={`w-full text-left p-3 rounded-xl transition-all flex items-center justify-between group ${
                  isActive
                    ? 'bg-[#640023] text-white shadow-md'
                    : 'hover:bg-[#f6f2f3] text-slate-800'
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <span className={`material-symbols-outlined text-lg ${isActive ? 'text-white' : 'text-[#640023]'}`}>
                    gavel
                  </span>
                  <div className="truncate">
                    <p className="font-semibold text-xs truncate">
                      {isAr ? codeItem.label_ar : codeItem.label_fr}
                    </p>
                    <p className={`text-[10px] font-mono ${isActive ? 'text-white/80' : 'text-slate-500'}`}>
                      {codeItem.articles_count} {isAr ? 'فصلاً' : 'articles'} • {codeItem.year}
                    </p>
                  </div>
                </div>
                <span className={`text-xs font-mono px-2 py-0.5 rounded-full ${isActive ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'}`}>
                  {codeItem.year}
                </span>
              </button>
            );
          })}
        </div>

        {/* Database Status Tag */}
        <div className="pt-4 border-t border-slate-200 text-center">
          <span className="inline-flex items-center gap-1.5 text-[11px] font-mono text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span>PostgreSQL Truth DB Connectée</span>
          </span>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto" dir={isAr ? 'rtl' : 'ltr'}>
        
        {/* Top Control Bar: Time-Travel & Search */}
        <div className="bg-white/95 backdrop-blur-md border-b border-[#debfc2]/40 px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-10 shadow-xs">
          <div>
            <h1 className="font-serif-luxury text-xl font-bold text-[#131b2e] flex items-center gap-2">
              <span>{isAr ? activeCode?.label_ar : activeCode?.label_fr}</span>
              <span className="text-xs font-mono font-normal px-2.5 py-0.5 bg-[#881337]/10 text-[#881337] rounded-full border border-[#881337]/20">
                {activeCode?.code_id}
              </span>
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              {isAr ? 'تصفح النصوص القانونية في صيغتها الرسمية والاطلاع على تاريخ السريان' : 'Exploration bitemporelle des dispositions légales en vigueur.'}
            </p>
          </div>

          {/* Time-Travel Year Selector */}
          <div className="flex items-center gap-3 bg-[#f8f9ff] px-4 py-2 rounded-xl border border-slate-200">
            <span className="material-symbols-outlined text-sm text-[#881337]">schedule</span>
            <span className="text-xs font-mono font-bold text-slate-700">{isAr ? 'تاريخ السريان :' : 'Version au :'}</span>
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value, 10))}
              className="text-xs font-mono font-bold bg-white border border-slate-300 rounded-lg px-2.5 py-1 text-[#881337] outline-none"
            >
              {[2026, 2025, 2024, 2023, 2022, 2021, 2020, 2018, 2014, 1990, 1956].map((yr) => (
                <option key={yr} value={yr}>{yr}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-[1500px] w-full mx-auto">
          
          {/* Middle Column: Articles List */}
          <div className="lg:col-span-4 bg-white rounded-2xl p-4 border border-slate-200/80 shadow-xs flex flex-col h-[760px]">
            <div className="mb-3">
              <h3 className="font-bold text-sm text-slate-800 mb-2 flex items-center justify-between">
                <span>{isAr ? 'فصول النص' : 'Articles du Code'}</span>
                <span className="text-xs font-mono text-slate-400">({filteredArticles.length})</span>
              </h3>
              <div className="relative">
                <input
                  type="text"
                  value={searchArticleQuery}
                  onChange={(e) => setSearchArticleQuery(e.target.value)}
                  placeholder={isAr ? 'بحث بالرقم أو النص...' : 'Filtrer article...'}
                  className="w-full text-xs bg-[#f8f9ff] border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 outline-none focus:border-[#881337]"
                />
                <span className="material-symbols-outlined absolute left-2.5 top-2 text-xs text-slate-400">search</span>
              </div>
            </div>

            {/* Articles Scrollable List */}
            <div className="flex-1 overflow-y-auto space-y-1.5 pr-1 custom-scrollbar">
              {filteredArticles.map((art) => {
                const isSelected = art.article_number === selectedArticleNum;
                return (
                  <button
                    key={art.article_number}
                    onClick={() => setSelectedArticleNum(art.article_number)}
                    className={`w-full text-left p-3 rounded-xl transition-all border ${
                      isSelected
                        ? 'bg-[#881337]/5 border-[#881337] shadow-xs'
                        : 'bg-white hover:bg-slate-50 border-slate-100'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`font-bold text-xs ${isSelected ? 'text-[#881337]' : 'text-slate-800'}`}>
                        {isAr ? `الفصل ${art.article_number}` : `Article ${art.article_number}`}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">
                        {art.hierarchy_path?.split('>')[0] || ''}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-600 line-clamp-2 leading-relaxed" dir="rtl">
                      {art.snippet_ar || art.snippet_fr}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Full Article Viewer (Real DB Text) */}
          <div className="lg:col-span-8 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col h-[760px] overflow-y-auto custom-scrollbar">
            {loading ? (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-400 gap-2">
                <span className="material-symbols-outlined text-3xl animate-spin">sync</span>
                <p className="text-xs font-mono">Chargement du texte officiel...</p>
              </div>
            ) : articleDetail ? (
              <div className="space-y-6">
                {/* Article Header & Actions */}
                <div className="flex items-center justify-between pb-4 border-b border-slate-200">
                  <div>
                    <span className="text-xs font-mono text-[#881337] font-semibold uppercase tracking-wider">
                      {articleDetail.hierarchy_path}
                    </span>
                    <h2 className="font-serif-luxury text-2xl font-bold text-slate-900 mt-1">
                      {isAr ? `الفصل ${articleDetail.article_number}` : `Article ${articleDetail.article_number}`}
                    </h2>
                    <div className="flex items-center gap-3 mt-2 text-xs font-mono text-slate-500">
                      <span>Valide du: <strong className="text-slate-800">{articleDetail.valid_from}</strong></span>
                      <span>au: <strong className="text-slate-800">{articleDetail.valid_to || 'En vigueur (Actif)'}</strong></span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleCopyText}
                      className="px-3 py-1.5 bg-[#f8f9ff] hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 flex items-center gap-1.5 transition-colors"
                    >
                      <span className="material-symbols-outlined text-sm">content_copy</span>
                      <span>{copySuccess ? (isAr ? 'تم النسخ!' : 'Copié!') : (isAr ? 'نسخ' : 'Copier')}</span>
                    </button>
                  </div>
                </div>

                {/* Dual-Language Display */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Arabic Official Text */}
                  <div className="p-4 bg-[#faf8ff] rounded-xl border border-[#881337]/10" dir="rtl">
                    <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-200">
                      <h4 className="font-bold text-xs text-[#881337]">النص الأصلي (الرسمي)</h4>
                      <span className="text-[10px] font-mono bg-white px-2 py-0.5 rounded border border-slate-200">العربية</span>
                    </div>
                    <div className="text-sm leading-loose text-slate-900 whitespace-pre-wrap font-arabic">
                      {articleDetail.text_ar || 'لا يوجد نص متوفر'}
                    </div>
                  </div>

                  {/* French Translation */}
                  <div className="p-4 bg-[#f8fafc] rounded-xl border border-slate-200" dir="ltr">
                    <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-200">
                      <h4 className="font-bold text-xs text-slate-700">Traduction Administrative</h4>
                      <span className="text-[10px] font-mono bg-white px-2 py-0.5 rounded border border-slate-200">Français</span>
                    </div>
                    <div className="text-sm leading-relaxed text-slate-800 whitespace-pre-wrap">
                      {articleDetail.text_fr || (
                        <p className="text-xs text-slate-400 italic">
                          Texte administratif en cours de numérisation bilingue.
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Bitemporal Version History */}
                {historyTimeline.length > 1 && (
                  <div className="mt-6 pt-6 border-t border-slate-200">
                    <h4 className="font-bold text-xs uppercase tracking-wider text-[#881337] mb-3 flex items-center gap-2">
                      <span className="material-symbols-outlined text-sm">history</span>
                      <span>{isAr ? 'تاريخ التعديلات التشريعية (Time-Travel)' : 'Historique des Amendements Légaux'}</span>
                    </h4>
                    <div className="space-y-2">
                      {historyTimeline.map((v, i) => (
                        <div key={v.version_id} className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs flex items-center justify-between">
                          <div>
                            <span className="font-bold text-slate-800">Version {i + 1}</span>
                            <span className="text-slate-500 ml-2">({v.valid_from} $\rightarrow$ {v.valid_to || 'Présent'})</span>
                          </div>
                          <span className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase font-bold ${v.status === 'active' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                            {v.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center text-slate-400 text-xs">
                {isAr ? 'الرجاء اختيار فصل لعرض نصه الكامل' : 'Sélectionnez un article pour afficher son texte authentique.'}
              </div>
            )}
          </div>

        </div>

      </main>

    </div>
  );
};
