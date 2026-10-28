/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { ScreenType, Language, SearchResult } from './types';
import { HeaderNav } from './components/HeaderNav';
import { Footer } from './components/Footer';
import { HomeScreen } from './screens/HomeScreen';
import { CorpusExplorerScreen } from './screens/CorpusExplorerScreen';
import { SearchJurisprudenceScreen } from './screens/SearchJurisprudenceScreen';
import { IngestionDashboardScreen } from './screens/IngestionDashboardScreen';
import { CitationDrawerModal } from './components/CitationDrawerModal';
import { DecisionDetailModal } from './components/DecisionDetailModal';
import { ProfessionalAccessModal } from './components/ProfessionalAccessModal';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<ScreenType>('home');
  const [lang, setLang] = useState<Language>('fr');

  // Modal States
  const [selectedCitation, setSelectedCitation] = useState<{
    code: string;
    label: string;
    type: 'article' | 'jurisprudence' | 'doctrine';
    snippet: string;
  } | null>(null);

  const [selectedDecision, setSelectedDecision] = useState<SearchResult | null>(null);
  const [isAuthOpen, setIsAuthOpen] = useState<boolean>(false);

  // Scroll to top upon navigating
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [currentScreen]);

  const handleToggleLang = () => {
    setLang((prev) => (prev === 'fr' ? 'ar' : 'fr'));
  };

  return (
    <div className={`min-h-screen flex flex-col bg-[#faf8ff] text-[#131b2e] ${lang === 'ar' ? 'font-arabic-sans' : 'font-sans'}`}>
      
      {/* Universal Top Header */}
      <HeaderNav
        currentScreen={currentScreen}
        onNavigate={setCurrentScreen}
        lang={lang}
        onToggleLang={handleToggleLang}
        onOpenAuth={() => setIsAuthOpen(true)}
      />

      {/* Screen Views */}
      <div className="flex-1 flex flex-col">
        {currentScreen === 'home' && (
          <HomeScreen
            lang={lang}
            onNavigate={setCurrentScreen}
            onOpenCitation={setSelectedCitation}
          />
        )}

        {currentScreen === 'corpus' && (
          <CorpusExplorerScreen
            lang={lang}
            onNavigate={setCurrentScreen}
            onOpenCitation={setSelectedCitation}
          />
        )}

        {currentScreen === 'search' && (
          <SearchJurisprudenceScreen
            lang={lang}
            onNavigate={setCurrentScreen}
            onSelectDecision={setSelectedDecision}
          />
        )}

        {currentScreen === 'ingestion' && (
          <IngestionDashboardScreen
            lang={lang}
            onNavigate={setCurrentScreen}
          />
        )}
      </div>

      {/* Footer */}
      {currentScreen !== 'corpus' && <Footer lang={lang} />}

      {/* Citation Inspector Modal */}
      <CitationDrawerModal
        citation={selectedCitation}
        onClose={() => setSelectedCitation(null)}
        lang={lang}
      />

      {/* Full Decision Reader Modal */}
      <DecisionDetailModal
        decision={selectedDecision}
        onClose={() => setSelectedDecision(null)}
        lang={lang}
      />

      {/* Sovereign Lawyer / Professional Access Modal */}
      <ProfessionalAccessModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        lang={lang}
      />

    </div>
  );
}
