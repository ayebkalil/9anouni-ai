import { LawArticleVersion, SearchResult, IngestionStream } from '../types';

export const ASSET_IMAGES = {
  logo: "https://lh3.googleusercontent.com/aida-public/AB6AXuDuY3AC9v7kgRTk80F9fPoeL_KrtI83QnBksq0exNKK5F9mO_aE7eK3S43YmXNqhxjuydG4nhwOjA4w2kbR9jt60X2-w3Od81nf8fn9HuPzYUNlvr4s5Uipz_aTdL8seCR4V-_5f2NCpEvHVlwtKzO5GYwpDP_gx21Wfz0da62Rurw4C4khhUyJTskZ-uNpHWbsenmEmDgmd_5cOnqX3cwLFMtuXIIx-0eq1B6eIKvOvwXc9_dhlD8",
  ladyJustice: "https://lh3.googleusercontent.com/aida-public/AB6AXuDpRvHk-L5dyOzDqqHkb9ub_SDy0C0kyUKwz-C1tiq3xHyvJKI6dsCl5j8xUX5YfuhgeLyxrTxbibISnf_gC-I0FKCklvLF_tGyuvcINHHnktvWoA0p7GWvhfBVQ6-54c5S0_1fsuW37f4kD4PXWelxRyg-y1mC13o0NsFWRBDtYemOh7ByQThxK0UGWQKjbmqugQjXZWtz4ghXpBFCdecxaDeK_tNFK4oLIOcNq98lpo84llBDDs4",
  jortArchival: "https://lh3.googleusercontent.com/aida-public/AB6AXuBz-xP_wgNKLs9L29g0pY5yLlGBKxfYExbnpun61Wk_NyN2bWT31o94KtTmNdSOxuDrH3m1Jyn0pptzl1Vi5yad62jkzB1L3kHzgZJ21WA36L15tvP4bTNHfA3yVAdk9hosiaG1IwYFLnae4RN6EE3VbbtuK7AldnGrH1i9t5oBhlhaJp85om2JP4eNDpyMsjvv8GYakm1mJJ2vmYDOyLmAwTaPcv4hkj0QVG6V9Ijub6bTUt773J0"
};

export const BITEMPORAL_ARTICLES: Record<number, LawArticleVersion> = {
  1956: {
    year: 1956,
    label: "Version Fondatrice (Décret Beylical / Code 1956)",
    lawTitleFr: "Loi Civile",
    lawTitleAr: "القانون المدني",
    codeNameFr: "Code des Obligations et des Contrats",
    codeNameAr: "مجلة الالتزامات والعقود",
    articleNumberFr: "Article 142 (Version 1956)",
    articleNumberAr: "الفصل 142 (نسخة 1956)",
    headingFr: "Des Obligations Contractuelles",
    headingAr: "في الالتزامات التعاقدية",
    originalTextFr: "Le contrat est une convention par laquelle une ou plusieurs personnes s'obligent, envers une ou plusieurs autres, à donner, à faire ou à ne pas faire quelque chose.",
    originalTextAr: "العقد اتفاق يلتزم بموجبه شخص أو عدة أشخاص نحو شخص أو عدة أشخاص آخرين بإعطاء شيء أو بفعله أو بالامتناع عن فعله.",
    strikethroughFr: "",
    strikethroughAr: "",
    addedFr: "Les conventions légalement formées tiennent lieu de loi à ceux qui les ont faites. Elles ne peuvent être révoquées que de leur consentement mutuel, ou pour les causes que la loi autorise.",
    addedAr: "الالتزامات التعاقدية المقررة على وجه صحيح تقوم مقام القانون بالنسبة إلى منشئيها، ولا يجوز إلغاؤها إلا برضاهم المتبادل أو في الحالات التي ينص عليها القانون.",
    concludingTextFr: "Elles doivent être exécutées de bonne foi.",
    concludingTextAr: "ويجب الوفاء بها بحسن نية.",
    changeNoteFr: "Texte initial promulgué le 15 décembre 1906 et refondu lors de l'indépendance en 1956.",
    changeNoteAr: "النص الأولي الصادر في مجلة الالتزامات والعقود لسنة 1906 والمؤكد في 1956.",
    jortReference: "JORT n° 1956-01 du 1er Juin 1956"
  },
  1990: {
    year: 1990,
    label: "Révision de 1990 (Loi n° 90-17)",
    lawTitleFr: "Loi Civile",
    lawTitleAr: "القانون المدني",
    codeNameFr: "Code des Obligations et des Contrats",
    codeNameAr: "مجلة الالتزامات والعقود",
    articleNumberFr: "Article 142 (Version 1990)",
    articleNumberAr: "الفصل 142 (نسخة 1990)",
    headingFr: "Des Obligations Contractuelles",
    headingAr: "في الالتزامات التعاقدية",
    originalTextFr: "Le contrat est une convention par laquelle une ou plusieurs personnes s'obligent, envers une ou plusieurs autres, à donner, à faire ou à ne pas faire quelque chose.",
    originalTextAr: "العقد اتفاق يلتزم بموجبه شخص أو عدة أشخاص نحو شخص أو عدة أشخاص آخرين بإعطاء شيء أو بفعله أو بالامتناع عن فعله.",
    strikethroughFr: "Toute convention contraire aux bonnes mœurs est réputée nulle de plein droit.",
    strikethroughAr: "كل التزام مناف للأخلاق الحميدة يعتبر باطلاً بحكم القانون.",
    addedFr: "Les conventions légalement formées tiennent lieu de loi à ceux qui les ont faites. Elles ne peuvent être révoquées que de leur consentement mutuel, ou pour les causes que la loi autorise.",
    addedAr: "الالتزامات التعاقدية المقررة على وجه صحيح تقوم مقام القانون بالنسبة إلى منشئيها، ولا يجوز إلغاؤها إلا برضاهم المتبادل أو في الحالات التي ينص عليها القانون.",
    concludingTextFr: "Elles doivent être exécutées de bonne foi.",
    concludingTextAr: "ويجب الوفاء بها بحسن نية.",
    changeNoteFr: "Harmonisation des critères d'opposabilité contractuelle et renforcement des clauses résolutoires.",
    changeNoteAr: "توحيد معايير الاحتجاج بالعقد وتعزيز البنود الفاسخة الصريحة.",
    jortReference: "JORT n° 1990-18 du 9 Mars 1990"
  },
  2018: {
    year: 2018,
    label: "Réforme Moderne de 2018 (Loi n° 2018-47)",
    lawTitleFr: "Loi Civile",
    lawTitleAr: "القانون المدني",
    codeNameFr: "Code des Obligations et des Contrats",
    codeNameAr: "مجلة الالتزامات والعقود",
    articleNumberFr: "Article 142 (Version 2018)",
    articleNumberAr: "الفصل 142 (نسخة 2018)",
    headingFr: "Des Obligations Contractuelles",
    headingAr: "في الالتزامات التعاقدية",
    originalTextFr: "Le contrat est une convention par laquelle une ou plusieurs personnes s'obligent, envers une ou plusieurs autres, à donner, à faire ou à ne pas faire quelque chose.",
    originalTextAr: "العقد اتفاق يلتزم بموجبه شخص أو عدة أشخاص نحو شخص أو عدة أشخاص آخرين بإعطاء شيء أو بفعله أو بالامتناع عن فعله.",
    strikethroughFr: "Les conventions légalement formées tiennent lieu de loi à ceux qui les ont faites. Elles ne peuvent être révoquées que de leur consentement mutuel, ou pour les causes que la loi autorise.",
    strikethroughAr: "الالتزامات التعاقدية المقررة على وجه صحيح تقوم مقام القانون بالنسبة إلى منشئيها، ولا يجوز إلغاؤها إلا برضاهم المتبادل أو في الحالات التي ينص عليها القانون.",
    addedFr: "Les contrats légalement formés tiennent lieu de loi à ceux qui les ont faits. Ils doivent être négociés, formés et exécutés de bonne foi. Cette disposition est d'ordre public.",
    addedAr: "العقود المبرمة على وجه صحيح تقوم مقام القانون بالنسبة إلى منشئيها. يجب التفاوض بشأنها وتكوينها وتنفيذها بحسن نية. هذا الحكم من النظام العام.",
    concludingTextFr: "Elles doivent être exécutées de bonne foi.",
    concludingTextAr: "ويجب الوفاء بها بحسن نية.",
    changeNoteFr: "Consécration expresse de la bonne foi au stade précontractuel (négociation) et qualification d'ordre public.",
    changeNoteAr: "إقرار صريح بمبدأ حسن النية في مرحلة المفاوضات السابقة للتعاقد واعتباره من النظام العام.",
    jortReference: "JORT n° 2018-85 du 23 Octobre 2018"
  },
  2024: {
    year: 2024,
    label: "Version Souveraine 2024 (Décret & Normes Numériques)",
    lawTitleFr: "Loi Civile & Numérique",
    lawTitleAr: "القانون المدني والرقمي",
    codeNameFr: "Code des Obligations et des Contrats",
    codeNameAr: "مجلة الالتزامات والعقود",
    articleNumberFr: "Article 142 (Version 2024)",
    articleNumberAr: "الفصل 142 (نسخة 2024)",
    headingFr: "Des Obligations Contractuelles et Numériques",
    headingAr: "في الالتزامات التعاقدية والرقمية",
    originalTextFr: "Le contrat est une convention par laquelle une ou plusieurs personnes s'obligent, envers une ou plusieurs autres, à donner, à faire ou à ne pas faire quelque chose.",
    originalTextAr: "العقد اتفاق يلتزم بموجبه شخص أو عدة أشخاص نحو شخص أو عدة أشخاص آخرين بإعطاء شيء أو بفعله أو بالامتناع عن فعله.",
    strikethroughFr: "",
    strikethroughAr: "",
    addedFr: "Les contrats légalement formés par voie écrite ou électronique souveraine tiennent lieu de loi à ceux qui les ont faits. Ils doivent être négociés, formés et exécutés de bonne foi avec garantie d'intégrité probatoire. Cette disposition est d'ordre public.",
    addedAr: "العقود المبرمة على وجه صحيح كتابياً أو بالطرق الإلكترونية السيادية تقوم مقام القانون لمنشئيها. يجب التفاوض بشأنها وتكوينها وتنفيذها بحسن نية مع ضمان الحجية الإثباتية. هذا الحكم من النظام العام.",
    concludingTextFr: "La force obligatoire s'applique également aux instruments de signature certifiée TunTrust.",
    concludingTextAr: "وتسري القوة الإلزامية أيضاً على وثائق الإمضاء الإلكتروني المصادق عليها رسمياً.",
    changeNoteFr: "Intégration de la force probante de la signature électronique et des smart-contracts souverains.",
    changeNoteAr: "إدماج الحجية القانونية للإمضاء الإلكتروني والعقود الرقمية السيادية.",
    jortReference: "JORT n° 2024-12 du 15 Janvier 2024"
  }
};

export const SEARCH_RESULTS_DATA: SearchResult[] = [
  {
    id: "cass-78452",
    relevance: 98,
    courtFr: "Cour de Cassation",
    courtAr: "محكمة التعقيب",
    decisionNumber: "Arrêt Civil N° 78452",
    date: "14 Nov 2023",
    titleFr: "Arrêt Civil N° 78452 - Interprétation de la Force Majeure en Matière Contractuelle",
    titleAr: "قرار تعقيبي مدني عدد 78452 - تأويل مفهوم القوة القاهرة في المادة التعاقدية",
    excerptFr: "...la Cour considère que l'événement imprévisible et irrésistible, constitutif de la force majeure, exonère le débiteur de sa responsabilité civile contractuelle conformément à l'article 283 du COC...",
    excerptAr: "...تعتبر المحكمة أن الحدث الذي لا يمكن توقعه ولا دفعه، والمشكل للقوة القاهرة، يعفي المدين من مسؤوليته المدنية التعاقدية طبقاً للفصل 283 من مجلة الالتزامات والعقود...",
    categoryFr: "Droit des Contrats / Responsabilité Civile",
    categoryAr: "قانون العقود / المسؤولية المدنية",
    fullDecision: {
      parties: "Société Maghreb Logistique c/ Entreprise Travaux Publics du Sahel",
      summary: "Définition stricte de l'imprévisibilité et de l'irrésistibilité lors de blocages logistiques exceptionnels. Application rigoureuse de l'article 283 du Code des Obligations et des Contrats.",
      grounds: [
        "Attendu qu'aux termes de l'article 283 du COC, la force majeure est tout fait que l'homme ne peut prévenir, tel que les phénomènes naturels extraordinaires ou les faits de prince;",
        "Attendu que l'irrésistibilité suppose que le débiteur s'est trouvé dans l'impossibilité absolue et non pas seulement relative ou plus onéreuse d'exécuter son obligation;",
        "Attendu que la Cour d'appel a souverainement constaté que les perturbations invoquées n'atteignaient pas le seuil d'insurmontabilité requis par la loi;"
      ],
      dispositif: "PAR CES MOTIFS, LA COUR : Rejette le pourvoi formé par la demanderesse et la condamne aux dépens légaux.",
      judges: ["Président : M. Moncef Ben Salem", "Conseillers : Mme Sonia Karray, M. Fethi Trabelsi"]
    }
  },
  {
    id: "app-12930",
    relevance: 85,
    courtFr: "Cour d'Appel de Tunis",
    courtAr: "محكمة الاستئناف بتونس",
    decisionNumber: "Décision N° 12930",
    date: "02 Fév 2022",
    titleFr: "Décision N° 12930 - Limites de l'Exonération pour Circonstances Exceptionnelles",
    titleAr: "قرار استئنافي عدد 12930 - حدود الإعفاء من المسؤولية للظروف الاستثنائية",
    excerptFr: "Il appartient au juge du fond d'apprécier souverainement si les conditions de la force majeure sont réunies pour dégager la responsabilité des parties contractantes.",
    excerptAr: "يعود لقاضي الأصل التقدير المطلق لتوفر شروط القوة القاهرة من عدمها لإعفاء الأطراف المتعاقدة من التزاماتها.",
    categoryFr: "Chambre Commerciale",
    categoryAr: "الدائرة التجارية",
    fullDecision: {
      parties: "Banque Nationale c/ Consortium Immobilière du Nord",
      summary: "L'inflation et la fluctuation monétaire ne constituent pas en elles-mêmes un cas de force majeure exonératoire de plein droit.",
      grounds: [
        "Considérant que la crise économique ne peut être qualifiée d'évènement imprévisible au sens de l'article 283 du COC;",
        "Considérant que le risque financier inhérent aux opérations commerciales doit être supporté par l'opérateur averti."
      ],
      dispositif: "Infirme le jugement entrepris et ordonne l'exécution intégrale des engagements financiers sous astreinte.",
      judges: ["Présidente : Mme Leila Bouraoui", "Conseillers : M. Hichem Mansour, M. Karim Driss"]
    }
  },
  {
    id: "cass-64910",
    relevance: 91,
    courtFr: "Cour de Cassation",
    courtAr: "محكمة التعقيب",
    decisionNumber: "Arrêt Mixte N° 64910",
    date: "19 Mai 2023",
    titleFr: "Arrêt Mixte N° 64910 - Bonne Foi Précontractuelle et Rupture Abusive des Pourparlers",
    titleAr: "قرار دوائر مجتمعة عدد 64910 - حسن النية السابقة للتعاقد والقطع التعسفي للمفاوضات",
    excerptFr: "L'obligation de négocier de bonne foi implique le devoir de ne pas susciter chez le cocontractant une confiance légitime avant de rompre unilatéralement et sans motif légitime.",
    excerptAr: "إن واجب التفاوض بحسن نية يفرض عدم إيهام الطرف الآخر بضمان إتمام العقد ثم قطع المحادثات تعسفياً دون مبرر جدي.",
    categoryFr: "Chambres Réunies / Droit Civil",
    categoryAr: "الدوائر المجتمعة / القانون المدني",
    fullDecision: {
      parties: "Groupe Industriel Moderne c/ Société Nouvelle de Distribution",
      summary: "Responsabilité délictuelle engagée lors de la rupture brutale de négociations avancées. Réparation limitée à la perte subie (frais engagés) à l'exclusion du gain manqué tiré du contrat espéré.",
      grounds: [
        "Attendu que la liberté de ne pas contracter trouve sa limite dans l'abus de droit et le respect de la bonne foi;",
        "Attendu que l'indemnisation ne saurait couvrir les bénéfices attendus de la conclusion du contrat projeté."
      ],
      dispositif: "Casse et annule l'arrêt de la Cour d'appel de Sousse et renvoie l'affaire devant la Cour d'appel de Monastir.",
      judges: ["Premier Président : M. Tarak Chérif", "Rapporteur : M. Khaled Marzouk"]
    }
  },
  {
    id: "tpi-3841",
    relevance: 78,
    courtFr: "Tribunal de Première Instance de Tunis",
    courtAr: "المحكمة الابتدائية بتونس",
    decisionNumber: "Jugement N° 3841",
    date: "10 Oct 2021",
    titleFr: "Jugement N° 3841 - Validité de la Clause Pénale et Réduction Judiciaire pour Excès Manifeste",
    titleAr: "حكم ابتدائي عدد 3841 - صحة الشرط الجزائي والتخفيض القضائي في حال المبالغة الفاحشة",
    excerptFr: "Le tribunal dispose du pouvoir modérateur sur les indemnités forfaitaires convenues contractuellement lorsqu'elles apparaissent manifestement excessives par rapport au préjudice réel subi.",
    excerptAr: "للمحكمة السلطة التقديرية لتعديل التعويض الاتفاقي المشروط في العقد إذا تبين أنه مبالغ فيه بصورة فاحشة مقارنة بالضرر الفعلي.",
    categoryFr: "Chambre Civile",
    categoryAr: "الدائرة المدنية",
    fullDecision: {
      parties: "Immobilier Les Oliviers c/ Ben Amor",
      summary: "Modération de la clause pénale de 50% du montant du contrat de vente sur plan, jugée disproportionnée au regard de l'exécution partielle.",
      grounds: [
        "Attendu que la clause pénale a une nature comminatoire et réparatrice mais ne doit pas constituer un enrichissement sans cause."
      ],
      dispositif: "Condamne le défendeur au paiement de la somme réduite de 15.000 DT au lieu des 50.000 DT stipulés.",
      judges: ["Juge Unique : M. Samy Belhaj"]
    }
  }
];

export const INGESTION_STREAMS_DATA: IngestionStream[] = [
  {
    id: "stream-1",
    documentId: "JORT-1959-001",
    source: "Constitution Initiale 1959",
    phase: "Extraction Layout & Bounding Boxes",
    status: "running",
    confidence: 0.98,
    pagesTotal: 34,
    pagesProcessed: 28
  },
  {
    id: "stream-2",
    documentId: "CIV-L4-T2",
    source: "Code des Obligations (JORT-1888-CIV-04)",
    phase: "Vérification Sémantique & OCR Diff",
    status: "manual",
    confidence: 0.82,
    pagesTotal: 12,
    pagesProcessed: 4
  },
  {
    id: "stream-3",
    documentId: "PEN-2023-AMND",
    source: "Amendements Pénaux Récents (Loi 2023)",
    phase: "Structuration JSON & Embeddings",
    status: "validated",
    confidence: 0.99,
    pagesTotal: 18,
    pagesProcessed: 18
  },
  {
    id: "stream-4",
    documentId: "CASS-ARR-2024-C3",
    source: "Recueil Arrêts Cour de Cassation 2024",
    phase: "Normalisation des Sommaires & Textes",
    status: "running",
    confidence: 0.96,
    pagesTotal: 142,
    pagesProcessed: 89
  }
];

export const SAMPLE_CHAT_STARTERS = [
  {
    qFr: "Quelles sont les conditions de validité d'un contrat de vente selon le Code des Obligations et des Contrats ?",
    qAr: "ما هي شروط صحة عقد البيع طبقاً لمجلة الالتزامات والعقود التونسية؟",
    answerFr: "Selon le Code des Obligations et des Contrats (COC) tunisien, les conditions essentielles pour la validité d'un contrat de vente sont définies principalement par l'article 2 et l'article 564. Elles comprennent : le consentement éclairé des parties, la capacité juridique de contracter, un objet certain formant la matière de l'engagement, et une cause licite conforme à l'ordre public.",
    answerAr: "طبقاً لمجلة الالتزامات والعقود التونسية (الفصلان 2 و 564)، تتمثل شروط صحة عقد البيع الأساسية في: التراضي المتبادل الخالي من العيوب، أهلية التعاقد، وجود محل معين وصالح للتعامل فيه، وسبب مشروع غير مخالف للنظام العام والآداب الحميدة.",
    citations: [
      { code: "Art. 2, COC", label: "Conditions de validité", type: "article" as const, snippet: "Les éléments nécessaires pour la validité des obligations qui dérivent d'une déclaration de volonté sont : 1° La capacité de s'obliger; 2° Une déclaration valable de volonté; 3° Un objet certain; 4° Une cause licite." },
      { code: "Art. 564, COC", label: "Contrat de vente", type: "article" as const, snippet: "La vente est un contrat par lequel l'une des parties transmet la propriété d'une chose ou d'un droit à l'autre contractant, contre un prix que ce dernier s'oblige à lui payer." },
      { code: "Cass. Civ. n° 12345", label: "Jurisprudence Cassation", type: "jurisprudence" as const, snippet: "Le défaut d'accord sur le prix ou la détermination de l'objet entraîne la nullité absolue du contrat de vente synallagmatique." }
    ]
  },
  {
    qFr: "Quels sont les effets de la force majeure sur les obligations contractuelles selon l'article 283 du COC ?",
    qAr: "ما هي آثار القوة القاهرة على الالتزامات التعاقدية طبقاً للفصل 283 من مجلة الالتزامات والعقود؟",
    answerFr: "Conformément à l'article 283 du COC tunisien, la force majeure est constituée par tout événement imprévisible, irrésistible et extérieur que l'homme ne peut prévenir. Dès lors que ses conditions sont réunies, elle éteint l'obligation et exonère totalement le débiteur de toute responsabilité contractuelle et de dommages-intérêts.",
    answerAr: "طبقاً للفصل 283 من مجلة الالتزامات والعقود، تعتبر القوة القاهرة كل أمر لا يستطيع الإنسان دفعه ولا توقعه ويكون خارجاً عن إرادته. ويترتب عليها إبراء ذمة المدين من الالتزام وإعفاؤه كلياً من التعويض عن عدم التنفيذ.",
    citations: [
      { code: "Art. 283, COC", label: "Définition Force Majeure", type: "article" as const, snippet: "La force majeure est tout fait que l'homme ne peut prévenir, tel que les phénomènes naturels extraordinaires, l'attaque d'ennemis, les faits du prince, etc." },
      { code: "Cass. Civ. n° 78452", label: "Arrêt Cassation 2023", type: "jurisprudence" as const, snippet: "L'irrésistibilité doit rendre l'exécution rigoureusement impossible et non simplement plus onéreuse." }
    ]
  },
  {
    qFr: "Quelles sont les règles de rupture abusive des pourparlers selon la jurisprudence tunisienne ?",
    qAr: "ما هي قواعد المسؤولية عن قطع المفاوضات التعاقدية تعسفياً في فقه القضاء التونسي؟",
    answerFr: "La jurisprudence de la Cour de Cassation (notamment Arrêt Mixte n° 64910) consacre le devoir de négociation de bonne foi. La rupture brutale, sans motif sérieux, après avoir laissé espérer la conclusion certaine du contrat, engage la responsabilité délictuelle (art. 82 COC). Le préjudice indemnisable se limite aux frais engagés sans couvrir le gain manqué.",
    answerAr: "يكرس فقه قضاء محكمة التعقيب (خاصة القرار 64910) واجب التفاوض بحسن نية. ويشكل القطع الفجائي والمجرد من سبب جدي بعد توليد ثقة مشروعة خطأ تقصيرياً (الفصل 82 م.ا.ع) يستوجب التعويض عن المصاريف المتكبدة دون الربح الفائت.",
    citations: [
      { code: "Art. 82, COC", label: "Responsabilité quasi-délictuelle", type: "article" as const, snippet: "Tout fait quelconque de l'homme qui cause à autrui un dommage oblige celui par la faute duquel il est arrivé à le réparer." },
      { code: "Cass. Mixte n° 64910", label: "Arrêt Chambres Réunies", type: "jurisprudence" as const, snippet: "L'indemnisation de la rupture abusive des pourparlers ne répare que les dépenses effectives et non l'espérance de gain." }
    ]
  }
];
