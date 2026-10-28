import React, { useState } from 'react';
import { Language } from '../types';

interface ProfessionalAccessModalProps {
  isOpen: boolean;
  onClose: () => void;
  lang: Language;
}

export const ProfessionalAccessModal: React.FC<ProfessionalAccessModalProps> = ({ isOpen, onClose, lang }) => {
  const [barNumber, setBarNumber] = useState('');
  const [nationalId, setNationalId] = useState('');
  const [loading, setLoading] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);

  if (!isOpen) return null;

  const isAr = lang === 'ar';

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setAuthenticated(true);
    }, 1000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="glass-panel w-full max-w-md rounded-2xl shadow-2xl overflow-hidden border border-white/40"
        dir={isAr ? 'rtl' : 'ltr'}
      >
        {/* Header */}
        <div className="bg-[#640023] text-white px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20">
              <span className="material-symbols-outlined text-rose-200">shield_lock</span>
            </div>
            <div>
              <span className="text-[10px] font-mono tracking-widest text-rose-200 uppercase bg-rose-950/60 px-2 py-0.5 rounded">
                Sovereign Key Auth
              </span>
              <h3 className="text-lg font-bold font-serif-luxury mt-0.5">
                {isAr ? 'فضاء المهنيين ورجال القانون' : 'Accès Professionnel Certifié'}
              </h3>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
          >
            <span className="material-symbols-outlined text-lg">close</span>
          </button>
        </div>

        {/* Body */}
        <div className="p-6 bg-[#faf8ff] text-slate-800">
          {!authenticated ? (
            <form onSubmit={handleVerify} className="space-y-4">
              <p className="text-xs text-slate-600 leading-relaxed">
                {isAr 
                  ? 'مخصص للمحامين المعتمدين لدى التعقيب والاستئناف، القضاة، والمستشارين القانونيين للهيئات السيادية.'
                  : 'Réservé aux Avocats inscrits au Barreau de Tunisie, Magistrats et Juristes d\'entreprise accrédités.'}
              </p>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1 font-mono uppercase">
                  {isAr ? 'رقم بطاقة المحاماة / الاعتماد' : 'N° d\'Inscription à l\'Ordre des Avocats'}
                </label>
                <input 
                  type="text" 
                  required
                  value={barNumber}
                  onChange={(e) => setBarNumber(e.target.value)}
                  placeholder="ex: ONAT-2014-9842"
                  className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#881337] focus:border-transparent font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1 font-mono uppercase">
                  {isAr ? 'رمز المفتاح الرقمي السيادي (TunTrust / Certilis)' : 'Certificat Électronique TunTrust (ID)'}
                </label>
                <input 
                  type="password" 
                  required
                  value={nationalId}
                  onChange={(e) => setNationalId(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#881337] focus:border-transparent font-mono"
                />
              </div>

              <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-[11px] text-amber-800 flex items-start gap-2">
                <span className="material-symbols-outlined text-base text-amber-700 shrink-0">verified_user</span>
                <span>
                  {isAr 
                    ? 'البيانات محمية وفق مقتضيات القانون الأساسي لحماية المعطيات الشخصية ونظام السيادة الرقمية.'
                    : 'Authentification souveraine chiffrée de bout en bout (AES-256) conforme aux protocoles du Ministère de la Justice.'}
                </span>
              </div>

              <button 
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-lg bg-[#881337] text-white hover:bg-[#640023] font-semibold text-xs tracking-wide transition-all shadow-md flex items-center justify-center gap-2 disabled:opacity-75"
              >
                {loading ? (
                  <>
                    <span className="material-symbols-outlined animate-spin text-sm">sync</span>
                    <span>{isAr ? 'جاري التحقق من السجل...' : 'Vérification du registre...'}</span>
                  </>
                ) : (
                  <>
                    <span className="material-symbols-outlined text-sm">lock_open</span>
                    <span>{isAr ? 'تسجيل الدخول الآمن' : 'Authentification Sécurisée'}</span>
                  </>
                )}
              </button>
            </form>
          ) : (
            <div className="text-center py-4 space-y-4 animate-fadeIn">
              <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto border-2 border-emerald-300">
                <span className="material-symbols-outlined text-3xl">verified</span>
              </div>
              <h4 className="font-bold text-base text-slate-900 font-serif-luxury">
                {isAr ? 'تم التحقق من الاعتماد بنجاح' : 'Accréditation Validée avec Succès'}
              </h4>
              <p className="text-xs text-slate-600">
                {isAr 
                  ? 'مرحباً بالأستاذ، لديك الآن وصول غير محدود لكافة نصوص الرائد الرسمي والقرارات التعقيبية غير المنشورة.'
                  : 'Bienvenue Maître. Vous disposez d\'un accès complet aux fonds exclusifs de la Cour de Cassation et aux analyses JORT prioritaires.'}
              </p>
              <div className="bg-slate-100 p-3 rounded-lg text-xs font-mono text-slate-700 text-left border border-slate-200">
                <div>Session: SEC-TN-2024-8842</div>
                <div>Status: Avocat à la Cour de Cassation (Actif)</div>
              </div>
              <button 
                onClick={onClose}
                className="w-full py-2.5 rounded-lg bg-[#881337] text-white hover:bg-[#640023] font-semibold text-xs transition-colors"
              >
                {isAr ? 'الدخول إلى فضاء العمل' : 'Accéder à l\'Espace Juridique'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
