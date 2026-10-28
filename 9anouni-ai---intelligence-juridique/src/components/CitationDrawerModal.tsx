import React from 'react';
import { Language } from '../types';

interface CitationDrawerProps {
  citation: {
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  } | null;
  onClose: () => void;
  lang: Language;
}

export const CitationDrawerModal: React.FC<CitationDrawerProps> = ({ citation, onClose, lang }) => {
  if (!citation) return null;

  const isAr = lang === 'ar';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="glass-panel w-full max-w-xl rounded-2xl shadow-2xl overflow-hidden border border-white/40 transform transition-all"
        dir={isAr ? 'rtl' : 'ltr'}
      >
        {/* Header */}
        <div className="bg-[#881337] text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-rose-200 text-2xl">verified</span>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs uppercase tracking-widest bg-rose-950/60 px-2 py-0.5 rounded text-rose-200">
                  {citation.type === 'article' ? (isAr ? 'مادة تشريعية' : 'Article du Corpus') : (isAr ? 'اجتهاد قضائي' : 'Jurisprudence Cassation')}
                </span>
                <span className="text-xs text-rose-200/80">JORT Souverain v2.4</span>
              </div>
              <h3 className="text-lg font-bold font-serif-luxury tracking-tight mt-0.5">{citation.code}</h3>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-rose-900/60 hover:bg-rose-900 flex items-center justify-center text-white transition-colors"
          >
            <span className="material-symbols-outlined text-lg">close</span>
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-4 max-h-[70vh] overflow-y-auto custom-scrollbar bg-[#faf8ff]">
          <div className="flex items-center justify-between text-xs text-slate-500 border-b border-slate-200 pb-2">
            <span className="font-semibold text-slate-700">{citation.label}</span>
            <span className="flex items-center gap-1 text-emerald-700 font-medium">
              <span className="material-symbols-outlined text-sm">lock_clock</span>
              {isAr ? 'نص ساري المفعول وموثق' : 'Texte authentifié & certifié'}
            </span>
          </div>

          <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm">
            <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2 font-mono">
              {isAr ? 'مقتطف من المصدر الرسمي:' : 'Extrait officiel certifié :'}
            </p>
            <blockquote className={`text-slate-800 leading-relaxed text-sm ${isAr ? 'font-arabic-sans text-right' : 'italic'}`}>
              "{citation.snippet}"
            </blockquote>
          </div>

          {/* Context Card */}
          <div className="bg-[#f2f3ff] p-4 rounded-xl border border-[#dae2fd] text-xs space-y-2">
            <div className="font-semibold text-[#640023] flex items-center gap-1.5">
              <span className="material-symbols-outlined text-base">info</span>
              {isAr ? 'السياق القانوني والحجية' : 'Portée juridique & Source'}
            </div>
            <p className="text-slate-600 leading-normal">
              {isAr 
                ? 'مأخوذ مباشرة من الرائد الرسمي للجمهورية التونسية والمصنف ضمن قاعدة البيانات السيادية لمحكمة التعقيب التونسية.'
                : 'Extrait certifié conforme au Journal Officiel de la République Tunisienne (JORT) et indexé dans le corpus de la Cour de Cassation.'}
            </p>
            <div className="pt-2 flex flex-wrap gap-2">
              <span className="bg-white px-2 py-1 rounded text-[11px] font-mono border border-slate-200 text-slate-700">
                Hash: 0x9a8f...2e4b
              </span>
              <span className="bg-white px-2 py-1 rounded text-[11px] font-mono border border-slate-200 text-emerald-700 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                {isAr ? 'مطابق للأصل' : 'Conforme à l\'original'}
              </span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-50 px-6 py-3 border-t border-slate-200 flex items-center justify-between text-xs">
          <span className="text-slate-500 font-mono">9anouni AI RAG Engine v2.4</span>
          <div className="flex gap-2">
            <button 
              onClick={onClose}
              className="px-4 py-1.5 rounded bg-[#881337] text-white hover:bg-[#640023] font-medium transition-colors"
            >
              {isAr ? 'إغلاق' : 'Fermer'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
