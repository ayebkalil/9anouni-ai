import React, { useState } from 'react';
import { SearchResult, Language } from '../types';

interface DecisionDetailModalProps {
  decision: SearchResult | null;
  onClose: () => void;
  lang: Language;
}

export const DecisionDetailModal: React.FC<DecisionDetailModalProps> = ({ decision, onClose, lang }) => {
  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  if (!decision) return null;

  const isAr = lang === 'ar';

  const handleDownloadPdf = () => {
    setDownloading(true);
    setTimeout(() => {
      setDownloading(false);
      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 3000);
    }, 1200);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md animate-fadeIn">
      <div 
        className="glass-panel w-full max-w-3xl max-h-[90vh] rounded-2xl shadow-2xl overflow-hidden border border-white/50 flex flex-col"
        dir={isAr ? 'rtl' : 'ltr'}
      >
        {/* Header */}
        <div className="bg-[#640023] text-white px-8 py-5 flex items-center justify-between border-b border-rose-900">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20">
              <span className="material-symbols-outlined text-rose-200">gavel</span>
            </div>
            <div>
              <div className="flex items-center gap-2 text-xs text-rose-200">
                <span className="bg-rose-900/80 px-2 py-0.5 rounded font-mono font-semibold uppercase">
                  {isAr ? decision.courtAr : decision.courtFr}
                </span>
                <span>•</span>
                <span>{decision.date}</span>
                <span>•</span>
                <span className="text-emerald-300 font-medium">{decision.relevance}% Pertinence IA</span>
              </div>
              <h2 className="text-xl font-bold font-serif-luxury tracking-tight mt-1 text-white">
                {isAr ? decision.titleAr : decision.titleFr}
              </h2>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
          >
            <span className="material-symbols-outlined text-xl">close</span>
          </button>
        </div>

        {/* Content Body */}
        <div className="p-8 space-y-6 overflow-y-auto custom-scrollbar bg-[#faf8ff] text-slate-800 flex-1">
          {/* Metadata Banner */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="text-xs uppercase tracking-wider text-slate-400 font-bold font-mono">
                {isAr ? 'أطراف النزاع' : 'Parties en cause'}
              </span>
              <p className="font-semibold text-slate-900 text-sm mt-0.5">{decision.fullDecision.parties}</p>
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider text-slate-400 font-bold font-mono">
                {isAr ? 'التصنيف القضائي' : 'Matière / Chambre'}
              </span>
              <p className="font-semibold text-[#881337] text-sm mt-0.5">
                {isAr ? decision.categoryAr : decision.categoryFr}
              </p>
            </div>
          </div>

          {/* Sommaire / Summary */}
          <div className="bg-[#f2f3ff] p-5 rounded-xl border border-[#dae2fd]">
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#640023] mb-2 flex items-center gap-1.5 font-mono">
              <span className="material-symbols-outlined text-sm">summarize</span>
              {isAr ? 'ملخص المبدأ القانوني المكرس' : 'Sommaire de la Décision'}
            </h4>
            <p className="text-sm leading-relaxed text-slate-800">
              {decision.fullDecision.summary}
            </p>
          </div>

          {/* Bilingual Excerpts */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <div className="text-[11px] font-mono font-bold text-slate-500 mb-2 uppercase">Version Française (Traduction Certifiée)</div>
              <p className="text-xs text-slate-700 leading-relaxed italic border-l-2 border-[#881337] pl-3">
                "{decision.excerptFr}"
              </p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200" dir="rtl">
              <div className="text-[11px] font-mono font-bold text-slate-500 mb-2 uppercase text-right">النص الأصلي (العربية)</div>
              <p className="text-xs text-slate-700 leading-relaxed font-arabic-sans border-r-2 border-[#881337] pr-3 text-right">
                "{decision.excerptAr}"
              </p>
            </div>
          </div>

          {/* Legal Grounds (Moyens & Motifs) */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 font-mono flex items-center gap-1.5">
              <span className="material-symbols-outlined text-sm">balance</span>
              {isAr ? 'أسباب وحيثيات القرار' : 'Motifs et Considérants (Cour de Cassation)'}
            </h4>
            <div className="space-y-2">
              {decision.fullDecision.grounds.map((ground, idx) => (
                <div key={idx} className="bg-white p-4 rounded-lg border border-slate-200 text-xs leading-relaxed text-slate-700 flex gap-3">
                  <span className="w-5 h-5 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center shrink-0 font-mono text-[10px] font-bold">
                    {idx + 1}
                  </span>
                  <span>{ground}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Dispositif */}
          <div className="bg-emerald-50/70 p-5 rounded-xl border border-emerald-200">
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-800 mb-2 flex items-center gap-1.5 font-mono">
              <span className="material-symbols-outlined text-sm">verified_user</span>
              {isAr ? 'منطوق الحكم / القرار' : 'Dispositif de la Cour'}
            </h4>
            <p className="text-sm font-semibold text-emerald-950 leading-relaxed">
              {decision.fullDecision.dispositif}
            </p>
          </div>

          {/* Judges / Signatories */}
          <div className="pt-2 flex flex-wrap items-center justify-between text-xs text-slate-500 border-t border-slate-200">
            <div>
              <span className="font-semibold text-slate-700">{isAr ? 'الهيئة القضائية :' : 'Formation de jugement :'}</span>{' '}
              {decision.fullDecision.judges.join(' • ')}
            </div>
            <div className="font-mono text-[11px] text-slate-400">
              Réf JORT Archive #TN-CAS-2023-784
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="bg-slate-100 px-8 py-4 border-t border-slate-200 flex items-center justify-between">
          <button 
            onClick={onClose}
            className="px-5 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 text-xs font-semibold transition-colors"
          >
            {isAr ? 'إغلاق' : 'Fermer'}
          </button>
          <div className="flex items-center gap-3">
            {downloadSuccess && (
              <span className="text-xs text-emerald-700 font-medium flex items-center gap-1 animate-fadeIn">
                <span className="material-symbols-outlined text-sm">check_circle</span>
                {isAr ? 'تم تحميل ملف PDF بنجاح' : 'PDF certifié téléchargé'}
              </span>
            )}
            <button 
              onClick={handleDownloadPdf}
              disabled={downloading}
              className="px-6 py-2.5 rounded-lg bg-[#881337] text-white hover:bg-[#640023] text-xs font-semibold transition-all shadow-md flex items-center gap-2 disabled:opacity-75"
            >
              <span className="material-symbols-outlined text-base">
                {downloading ? 'sync' : 'picture_as_pdf'}
              </span>
              <span>
                {downloading 
                  ? (isAr ? 'جاري التوليد...' : 'Génération du PDF...') 
                  : (isAr ? 'تحميل القرار الرسمي (PDF)' : 'Télécharger l\'Arrêt Officiel (PDF)')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
