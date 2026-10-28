import React from 'react';
import { Language } from '../types';

interface FooterProps {
  lang: Language;
}

export const Footer: React.FC<FooterProps> = ({ lang }) => {
  const isAr = lang === 'ar';

  return (
    <footer className="w-full bg-[#f2f3ff] text-[#131b2e] py-12 px-6 md:px-16 border-t border-[#debfc2]/60 mt-auto z-10 relative">
      <div className="max-w-[1360px] mx-auto flex flex-col md:flex-row justify-between items-center gap-6" dir={isAr ? 'rtl' : 'ltr'}>
        <div className="flex items-center gap-3">
          <span className="font-serif-luxury text-xl font-bold text-[#640023]">9anouni AI</span>
          <span className="text-slate-400">|</span>
          <span className="text-xs md:text-sm text-[#574144]">
            {isAr 
              ? '© 2024 قانوني ذكاء اصطناعي. المنصة السيادية للعدالة والتشريع التونسي.' 
              : '© 2024 9anouni AI. Plateforme Souveraine de Justice Tunisienne.'}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-6 text-xs text-[#574144]">
          <a href="#mentions" onClick={(e) => e.preventDefault()} className="hover:text-[#640023] hover:underline transition-colors">
            {isAr ? 'الإشعارات القانونية' : 'Mentions Légales'}
          </a>
          <a href="#confidentialite" onClick={(e) => e.preventDefault()} className="hover:text-[#640023] hover:underline transition-colors">
            {isAr ? 'الخصوصية وحماية البيانات' : 'Confidentialité'}
          </a>
          <a href="#api" onClick={(e) => e.preventDefault()} className="hover:text-[#640023] hover:underline transition-colors">
            {isAr ? 'واجهة البرمجة (API)' : 'API Juridique'}
          </a>
          <a href="#contact" onClick={(e) => e.preventDefault()} className="hover:text-[#640023] hover:underline transition-colors">
            {isAr ? 'اتصل بنا' : 'Contact'}
          </a>
        </div>
      </div>
    </footer>
  );
};
