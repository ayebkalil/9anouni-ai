import React from 'react';
import { ScreenType, Language } from '../types';
import { ASSET_IMAGES } from '../data/legalData';

interface HeaderNavProps {
  currentScreen: ScreenType;
  onNavigate: (screen: ScreenType) => void;
  lang: Language;
  onToggleLang: () => void;
  onOpenAuth: () => void;
}

export const HeaderNav: React.FC<HeaderNavProps> = ({
  currentScreen,
  onNavigate,
  lang,
  onToggleLang,
  onOpenAuth,
}) => {
  const isAr = lang === 'ar';

  return (
    <header className="fixed top-0 left-0 right-0 w-full z-50 bg-[#faf8ff]/90 backdrop-blur-xl border-b border-[#debfc2]/40 shadow-xs transition-all">
      <div className="max-w-[1360px] mx-auto px-4 md:px-12 py-3 flex items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div 
          onClick={() => onNavigate('home')}
          className="flex items-center gap-3 cursor-pointer group"
          id="brand-logo-button"
        >
          <img
            src={ASSET_IMAGES.logo}
            alt="9anouni AI Logo"
            className="h-10 w-10 object-contain rounded-md shadow-xs group-hover:scale-105 transition-transform"
          />
          <div className="flex flex-col">
            <span className="font-serif-luxury text-2xl md:text-3xl font-bold text-[#640023] tracking-tight group-hover:text-[#881337] transition-colors leading-none">
              9anouni AI
            </span>
            <span className="text-[10px] font-mono tracking-widest text-[#574144] uppercase hidden sm:block">
              {isAr ? 'الذكاء القانوني التونسي' : 'Intelligence Juridique Tunisienne'}
            </span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-8">
          <button
            onClick={() => onNavigate('home')}
            className={`font-mono text-xs uppercase tracking-wider transition-all duration-200 py-1 ${
              currentScreen === 'home'
                ? 'text-[#640023] font-bold border-b-2 border-[#640023]'
                : 'text-[#574144] hover:text-[#640023]'
            }`}
            id="nav-home-btn"
          >
            {isAr ? 'الرئيسية' : 'Accueil'}
          </button>
          
          <button
            onClick={() => onNavigate('search')}
            className={`font-mono text-xs uppercase tracking-wider transition-all duration-200 py-1 ${
              currentScreen === 'search'
                ? 'text-[#640023] font-bold border-b-2 border-[#640023]'
                : 'text-[#574144] hover:text-[#640023]'
            }`}
            id="nav-jurisprudence-btn"
          >
            {isAr ? 'فقه القضاء' : 'Jurisprudence'}
          </button>

          <button
            onClick={() => onNavigate('corpus')}
            className={`font-mono text-xs uppercase tracking-wider transition-all duration-200 py-1 ${
              currentScreen === 'corpus'
                ? 'text-[#640023] font-bold border-b-2 border-[#640023]'
                : 'text-[#574144] hover:text-[#640023]'
            }`}
            id="nav-codes-btn"
          >
            {isAr ? 'المجلات القانونية' : 'Codes'}
          </button>

          <button
            onClick={() => onNavigate('ingestion')}
            className={`font-mono text-xs uppercase tracking-wider transition-all duration-200 py-1 ${
              currentScreen === 'ingestion'
                ? 'text-[#640023] font-bold border-b-2 border-[#640023]'
                : 'text-[#574144] hover:text-[#640023]'
            }`}
            id="nav-analyses-btn"
          >
            {isAr ? 'التحاليل ومراقبة الجودة' : 'Analyses & QC'}
          </button>
        </nav>

        {/* Right Actions: Lang Switcher & Professional Access */}
        <div className="flex items-center gap-3 md:gap-4">

          <button
            onClick={onToggleLang}
            className="px-3 py-1.5 rounded-lg border border-[#8a7174]/40 hover:bg-[#eaedff] text-xs font-semibold text-[#131b2e] font-arabic-sans transition-colors flex items-center gap-1.5"
            title="Changer de langue (Français / العربية)"
            id="lang-toggle-btn"
          >
            <span className="material-symbols-outlined text-sm">translate</span>
            <span className="font-bold">{isAr ? 'Français' : 'العربية'}</span>
          </button>

          <button
            onClick={onOpenAuth}
            className="bg-[#881337] hover:bg-[#640023] text-white px-4 md:px-6 py-2 rounded-lg font-mono text-xs font-medium tracking-wide transition-all shadow-xs hover:shadow-md active:scale-95 flex items-center gap-1.5"
            id="professional-access-btn"
          >
            <span className="material-symbols-outlined text-sm">gavel</span>
            <span className="whitespace-nowrap">{isAr ? 'الدخول المهني' : 'Accès Professionnel'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
