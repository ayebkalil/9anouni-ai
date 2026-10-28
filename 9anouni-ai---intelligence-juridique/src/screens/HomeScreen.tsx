import React, { useState } from 'react';
import { Language, ScreenType } from '../types';
import { ASSET_IMAGES, SAMPLE_CHAT_STARTERS } from '../data/legalData';
import { api } from '../services/api';

interface HomeScreenProps {
  lang: Language;
  onNavigate: (screen: ScreenType) => void;
  onOpenCitation: (citation: {
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  }) => void;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({
  lang,
  onNavigate,
  onOpenCitation,
}) => {
  const isAr = lang === 'ar';

  const [inputQuery, setInputQuery] = useState('');
  const [activeStarterIndex, setActiveStarterIndex] = useState(0);
  const [messages, setMessages] = useState([
    {
      id: 'msg-1',
      sender: 'user' as const,
      text: SAMPLE_CHAT_STARTERS[0].qFr,
      arabicText: SAMPLE_CHAT_STARTERS[0].qAr,
    },
    {
      id: 'msg-2',
      sender: 'assistant' as const,
      text: SAMPLE_CHAT_STARTERS[0].answerFr,
      arabicText: SAMPLE_CHAT_STARTERS[0].answerAr,
      citations: SAMPLE_CHAT_STARTERS[0].citations,
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [scanDrawerOpen, setScanDrawerOpen] = useState(false);

  const handleSendMessage = async (textToSend?: string) => {
    const query = textToSend || inputQuery;
    if (!query.trim()) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user' as const,
      text: query,
      arabicText: query,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsTyping(true);

    try {
      // Call Live Backend RAG API with Gemini Pro
      const data = await api.sendChat(query, isAr ? 'ar' : 'fr');
      const aiMsg = {
        id: data.id || `ai-${Date.now()}`,
        sender: 'assistant' as const,
        text: data.answerFr,
        arabicText: data.answerAr,
        citations: data.citations && data.citations.length > 0 ? (data.citations as any) : SAMPLE_CHAT_STARTERS[0].citations,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.warn('Using offline sovereign fallback:', err);
      // Sovereign Fallback
      const matched = SAMPLE_CHAT_STARTERS.find(
        (s) =>
          s.qFr.toLowerCase().includes(query.toLowerCase().slice(0, 10)) ||
          s.qAr.includes(query.slice(0, 8))
      );

      const aiMsg = matched
        ? {
            id: `ai-${Date.now()}`,
            sender: 'assistant' as const,
            text: matched.answerFr,
            arabicText: matched.answerAr,
            citations: matched.citations,
          }
        : {
            id: `ai-${Date.now()}`,
            sender: 'assistant' as const,
            text: `En vertu des dispositions du droit positif tunisien et des textes du JORT, la question posée relève du cadre légal en vigueur. Les conditions applicables sont régies par les articles de référence.`,
            arabicText: `بناءً على أحكام القانون الوضعي التونسي ونصوص الرائد الرسمي للجمهورية التونسية، تخضع المسألة للأحكام التشريعية السارية.`,
            citations: [
              {
                code: 'Art. 1, JORT',
                label: 'Texte Authentique Promulgué',
                type: 'article' as const,
                snippet: 'Vu la Constitution et les lois promulguées au Journal Officiel de la République Tunisienne...',
              },
            ],
          };
      setMessages((prev) => [...prev, aiMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSelectStarter = (index: number) => {
    setActiveStarterIndex(index);
    const starter = SAMPLE_CHAT_STARTERS[index];
    handleSendMessage(isAr ? starter.qAr : starter.qFr);
  };

  return (
    <div className="w-full hero-bg-gradient min-h-screen pt-24 pb-16 relative overflow-hidden" dir={isAr ? 'rtl' : 'ltr'}>
      {/* Ambient background glow accents */}
      <div className="absolute top-10 right-10 w-96 h-96 rounded-full bg-[#dae2fd]/40 blur-3xl pointer-events-none -z-10" />
      <div className="absolute bottom-10 left-10 w-[500px] h-[500px] rounded-full bg-[#ffd9dd]/30 blur-3xl pointer-events-none -z-10" />

      <main className="max-w-[1360px] mx-auto px-4 md:px-12 flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-16 relative z-10">
        
        {/* Left Column: Sovereign Editorial & Conversational RAG */}
        <div className="w-full lg:w-1/2 flex flex-col gap-8">
          
          {/* Badge & Headlines */}
          <div className="space-y-5">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 bg-white/80 backdrop-blur-md rounded-full border border-[#debfc2]/60 shadow-xs">
              <span className="w-2 h-2 rounded-full bg-[#881337] animate-pulse" />
              <span className="font-mono text-xs uppercase tracking-widest text-[#574144] font-semibold">
                {isAr ? 'النظام السيادي الإصدار 2.4' : 'SYSTÈME SOUVERAIN V2.4'}
              </span>
            </div>

            <h1 className="font-serif-luxury text-3xl sm:text-4xl md:text-5xl lg:text-[3.25rem] font-bold text-[#131b2e] leading-[1.15] tracking-tight">
              {isAr ? (
                <span>الذكاء القانوني التونسي فائق الدقة</span>
              ) : (
                <span>L'INTELLIGENCE JURIDIQUE TUNISIENNE DE HAUTE PRÉCISION</span>
              )}
            </h1>

            <p className="text-base sm:text-lg text-[#574144] leading-relaxed max-w-xl">
              {isAr 
                ? 'تصفح واستشر المجموعات التشريعية الوطنية بوضوح مطلق. تحاليل مستندة بدقة إلى الرائد الرسمي للجمهورية التونسية (JORT) وفقه قضاء محكمة التعقيب.'
                : 'Naviguez dans le Corpus National avec une clarté absolue. Des analyses fondées sur le JORT et la jurisprudence de la Cour de Cassation.'}
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={() => {
                  const chatInput = document.getElementById('legal-rag-input');
                  chatInput?.focus();
                }}
                className="bg-[#881337] hover:bg-[#640023] text-white px-7 py-3.5 rounded-lg font-mono text-xs font-semibold uppercase tracking-wider transition-all shadow-md hover:shadow-lg active:scale-95 flex items-center gap-2"
                id="hero-start-consultation-btn"
              >
                <span>{isAr ? 'بدء الاستشارة الفورية' : 'Démarrer la Consultation'}</span>
                <span className="material-symbols-outlined text-base">arrow_forward</span>
              </button>

              <button
                onClick={() => onNavigate('corpus')}
                className="bg-white/80 hover:bg-white text-[#131b2e] border border-[#8a7174]/40 px-7 py-3.5 rounded-lg font-mono text-xs font-semibold uppercase tracking-wider transition-all hover:border-[#640023] shadow-xs flex items-center gap-2"
                id="hero-explore-features-btn"
              >
                <span className="material-symbols-outlined text-base">auto_stories</span>
                <span>{isAr ? 'استكشاف المجلات والقوانين' : 'Découvrir les Fonctionnalités'}</span>
              </button>
            </div>
          </div>

          {/* Quick Query Pills */}
          <div className="space-y-2 pt-2">
            <div className="flex items-center gap-2 text-xs font-mono text-slate-500 uppercase tracking-wider">
              <span className="material-symbols-outlined text-sm text-[#881337]">quick_reference_all</span>
              <span>{isAr ? 'نماذج استشارات قانونية شائعة:' : 'Questions juridiques fréquentes :'}</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {SAMPLE_CHAT_STARTERS.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectStarter(idx)}
                  className={`text-xs px-3 py-1.5 rounded-lg border transition-all text-left ${
                    activeStarterIndex === idx
                      ? 'bg-[#881337] text-white border-[#881337] shadow-xs'
                      : 'bg-white/90 text-slate-700 border-slate-300 hover:border-[#881337] hover:bg-white'
                  }`}
                >
                  {isAr ? (s.qAr.length > 40 ? s.qAr.slice(0, 40) + '...' : s.qAr) : (s.qFr.length > 45 ? s.qFr.slice(0, 45) + '...' : s.qFr)}
                </button>
              ))}
            </div>
          </div>

          {/* Embedded RAG Conversational Interface (Screen 1 core) */}
          <div className="glass-panel p-6 rounded-2xl shadow-[0_12px_45px_rgba(15,23,42,0.08)] relative overflow-hidden border border-white/60">
            {/* Chat Header */}
            <div className="flex items-center justify-between mb-4 border-b border-[#debfc2]/40 pb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[#881337]/10 flex items-center justify-center text-[#881337]">
                  <span className="material-symbols-outlined text-lg">gavel</span>
                </div>
                <div>
                  <span className="font-serif-luxury font-bold text-sm text-[#131b2e]">
                    {isAr ? 'المساعد القانوني السيادي' : 'Assistant Juridique'}
                  </span>
                  <span className="block text-[10px] font-mono text-emerald-700">
                    ● {isAr ? 'متصل بقاعدة نصوص الرائد الرسمي ومحكمة التعقيب' : 'Connecté au Corpus JORT & Cassation'}
                  </span>
                </div>
              </div>

              <button
                onClick={() => {
                  setMessages([
                    {
                      id: 'msg-reset',
                      sender: 'assistant',
                      text: 'Posez-moi une question sur le Code des Obligations et des Contrats, le Code Pénal ou la jurisprudence.',
                      arabicText: 'اطرح سؤالك حول مجلة الالتزامات والعقود، المجلة الجزائية أو فقه قضاء محكمة التعقيب.',
                    },
                  ]);
                }}
                className="text-[11px] text-slate-500 hover:text-[#640023] flex items-center gap-1 font-mono transition-colors"
                title="Effacer la conversation"
              >
                <span className="material-symbols-outlined text-sm">restart_alt</span>
                <span className="hidden sm:inline">{isAr ? 'إعادة ضبط' : 'Réinitialiser'}</span>
              </button>
            </div>

            {/* Chat Messages Log */}
            <div className="space-y-4 mb-4 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col ${
                    msg.sender === 'user' ? 'items-end' : 'items-start'
                  } animate-fadeIn`}
                >
                  {msg.sender === 'user' ? (
                    <div className="bg-[#eaedff] text-[#131b2e] p-4 rounded-2xl rounded-tr-xs max-w-[90%] border border-[#dae2fd] shadow-xs">
                      <p className="text-sm font-medium">
                        {isAr && msg.arabicText ? msg.arabicText : msg.text}
                      </p>
                    </div>
                  ) : (
                    <div className="bg-white text-[#131b2e] p-4 rounded-2xl rounded-tl-xs max-w-[96%] border border-slate-200/90 shadow-sm space-y-3">
                      <p className="text-sm leading-relaxed text-slate-800">
                        {isAr && msg.arabicText ? msg.arabicText : msg.text}
                      </p>

                      {/* Interactive Legal Citations Chips */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-100">
                          {msg.citations.map((cit, cIdx) => (
                            <button
                              key={cIdx}
                              onClick={() => onOpenCitation(cit)}
                              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#ffd9dd]/40 border border-[#881337]/30 text-[#881337] hover:bg-[#881337] hover:text-white font-mono text-[11px] font-semibold transition-all group"
                              title="Cliquer pour afficher la source authentifiée"
                            >
                              <span className="material-symbols-outlined text-[14px]">
                                {cit.type === 'article' ? 'menu_book' : 'account_balance'}
                              </span>
                              <span>[{cit.code}]</span>
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}

              {isTyping && (
                <div className="flex items-center gap-2 text-xs text-slate-500 font-mono bg-white p-3 rounded-xl w-fit border border-slate-200">
                  <span className="material-symbols-outlined animate-spin text-sm text-[#881337]">sync</span>
                  <span>{isAr ? 'جاري استخراج السند القانوني...' : 'Extraction sémantique du Corpus JORT...'}</span>
                </div>
              )}
            </div>

            {/* Input Bar */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="relative flex items-center"
            >
              <input
                id="legal-rag-input"
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder={
                  isAr
                    ? 'اطرح سؤالك القانوني، رقم الفصل أو المفهوم...'
                    : 'Posez votre question juridique (ex: conditions de validité, force majeure)...'
                }
                className="w-full bg-white border border-slate-300 rounded-xl pl-4 pr-12 py-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#881337] focus:border-transparent transition-all shadow-xs"
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 rounded-lg bg-[#881337] hover:bg-[#640023] text-white flex items-center justify-center transition-colors shadow-xs"
                title="Envoyer la requête"
              >
                <span className="material-symbols-outlined text-lg">send</span>
              </button>
            </form>
          </div>

          {/* Trust Banner with 52K Stat & User Avatars */}
          <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-200/60 text-xs text-slate-600">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-slate-900 text-white flex items-center justify-center font-mono font-bold text-xs shadow-xs">
                ⚖️ 9A
              </div>
              <div>
                <div className="font-bold text-slate-900 text-sm">
                  {isAr ? 'حقوقكم هي رسالتنا' : 'YOUR RIGHTS IS OUR MISSION'}
                </div>
                <div className="text-slate-500 text-xs">
                  {isAr ? 'مرتكزون على القانون السيادي' : 'Focused on You. Grounded in Law'}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right">
                <div className="font-bold font-serif-luxury text-2xl text-[#640023] leading-none">52K</div>
                <div className="text-[11px] text-slate-500 font-mono">
                  {isAr ? 'حريف وخبير قانوني' : 'Satisfied Clients'}
                </div>
              </div>
              <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-700 border border-slate-300">
                <span className="material-symbols-outlined text-sm">north_east</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: 3D Asset Render & Floating Widgets */}
        <div className="w-full lg:w-1/2 relative min-h-[520px] sm:min-h-[600px] flex items-center justify-center">
          
          {/* Metallic Statue of Lady Justice from hotlinked asset */}
          <div className="relative w-full max-w-lg aspect-square flex items-center justify-center group">
            <div className="absolute inset-0 bg-radial from-white/90 via-transparent to-transparent -z-10 pointer-events-none rounded-full transform scale-90" />
            <img
              src={ASSET_IMAGES.ladyJustice}
              alt="Lady Justice 3D Silver Render"
              className="w-full h-full object-contain max-h-[580px] drop-shadow-[0_20px_35px_rgba(0,0,0,0.15)] transform group-hover:scale-[1.02] transition-transform duration-700 pointer-events-none select-none"
            />
          </div>

          {/* Floating Widget 1: 100% Textes JORT Authentifiés */}
          <div className="absolute top-10 right-4 sm:right-8 glass-panel px-4 py-3 rounded-xl shadow-md flex items-center gap-3 animate-bounce duration-1000 border border-white/70">
            <div className="w-10 h-10 rounded-full bg-[#881337]/10 flex items-center justify-center text-[#881337]">
              <span className="material-symbols-outlined text-xl">verified</span>
            </div>
            <div className="flex flex-col">
              <span className="font-mono text-xs font-bold text-[#131b2e]">
                {isAr ? '100% نصوص الرائد الرسمي' : '100% Textes JORT'}
              </span>
              <span className="text-[11px] text-[#574144]">
                {isAr ? 'موثقة ومحدثة بصفة دورية' : 'Authentifiés & Mis à jour'}
              </span>
            </div>
          </div>

          {/* Floating Widget 2: Indexé 1956–2024 Archives Complètes */}
          <div className="absolute bottom-20 left-4 sm:left-6 glass-panel px-4 py-3 rounded-xl shadow-md flex items-center gap-3 border border-white/70">
            <div className="w-10 h-10 rounded-full bg-[#eaedff] flex items-center justify-center text-[#131b2e]">
              <span className="material-symbols-outlined text-xl">history_edu</span>
            </div>
            <div className="flex flex-col">
              <span className="font-mono text-xs font-bold text-[#131b2e]">
                {isAr ? 'مفهرس 1956–2024' : 'Indexé 1956–2024'}
              </span>
              <span className="text-[11px] text-[#574144]">
                {isAr ? 'أرشيف تشريعي كامل' : 'Archives Complètes'}
              </span>
            </div>
          </div>

          {/* Floating Widget 3: Closure Statistics Graph Card (from mockup) */}
          <div className="absolute top-1/3 -right-2 sm:right-0 glass-panel p-3.5 rounded-xl shadow-md border border-white/70 hidden sm:block">
            <div className="flex items-center justify-between text-[11px] font-mono mb-2 gap-4">
              <span className="font-bold text-slate-800 flex items-center gap-1">
                <span className="material-symbols-outlined text-sm text-[#881337]">trending_up</span>
                {isAr ? 'إحصائيات الأحكام' : 'Closure Statistics'}
              </span>
              <span className="text-slate-400">Yearly ▾</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-28 h-10 flex items-end gap-1">
                <div className="w-3 bg-slate-200 h-4 rounded-t-sm" />
                <div className="w-3 bg-slate-300 h-6 rounded-t-sm" />
                <div className="w-3 bg-slate-200 h-5 rounded-t-sm" />
                <div className="w-3 bg-[#881337] h-9 rounded-t-sm" />
                <div className="w-3 bg-rose-400 h-7 rounded-t-sm" />
                <div className="w-3 bg-slate-300 h-8 rounded-t-sm" />
              </div>
              <div className="text-right font-mono">
                <div className="text-xs font-bold text-[#881337]">34 Cases</div>
                <div className="text-[9px] text-emerald-600 font-semibold">+28% Gain</div>
              </div>
            </div>
          </div>

          {/* Interactive Side Drawer Peek: Scan JORT */}
          <div
            onClick={() => setScanDrawerOpen(!scanDrawerOpen)}
            className={`absolute right-[-10px] bottom-6 w-52 glass-panel rounded-l-2xl p-4 shadow-lg border-r-0 rotate-[-1deg] opacity-95 transition-all duration-300 cursor-pointer hover:translate-x-[-15px] ${
              scanDrawerOpen ? 'translate-x-[-20px] ring-2 ring-[#881337]' : ''
            }`}
            title="Cliquer pour inspecter la numérisation JORT"
          >
            <div className="text-[11px] text-[#574144] font-mono font-bold mb-2 flex justify-between items-center border-b border-[#debfc2]/40 pb-1">
              <span>{isAr ? 'مسح الرائد الرسمي' : 'Scan JORT'}</span>
              <span className="material-symbols-outlined text-sm text-[#881337]">document_scanner</span>
            </div>
            <div className="space-y-1.5 opacity-70">
              <div className="h-1.5 bg-[#debfc2]/60 rounded w-full" />
              <div className="h-1.5 bg-[#debfc2]/60 rounded w-5/6" />
              <div className="h-1.5 bg-[#debfc2]/60 rounded w-4/6" />
              <div className="relative mt-3 border border-[#881337]/50 bg-[#ffd9dd]/30 p-2 rounded-lg">
                <div className="h-1.5 bg-[#881337]/60 rounded w-full mb-1" />
                <div className="h-1.5 bg-[#881337]/60 rounded w-3/4" />
                <span className="absolute -top-2.5 right-2 bg-[#881337] text-white text-[9px] font-mono px-1.5 py-0.2 rounded">
                  {isAr ? 'استخراج ذكي' : 'Extrait IA'}
                </span>
              </div>
            </div>
          </div>

        </div>

      </main>
    </div>
  );
};
