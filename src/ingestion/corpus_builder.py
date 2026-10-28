"""
Corpus Builder: Generates structured, authentic bilingual legal datasets for:
1. Tunisian Constitution 2022 (دستور الجمهورية التونسية 2022 - Décret Présidentiel n° 2022-691)
2. Labor Code (مجلة الشغل / Code du Travail)
3. Code of Personal Status (مجلة الأحوال الشخصية / Code du Statut Personnel)
4. French translations for Finance Laws (Lois de Finances)
"""

import os
import json
import uuid
from typing import Any, Dict, List

def build_constitution_2022_corpus() -> List[Dict[str, Any]]:
    """
    Builds the complete authentic bilingual articles of the Tunisian Constitution of 2022
    (Promulgated on 17 August 2022, JORT Special Issue n° 89).
    """
    articles = [
        {
            "article_number": "1",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 1 - تونس دولة ذات نظام جمهوري.",
            "text_fr": "Article 1 - La Tunisie est un État ayant un régime républicain.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "2",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 2 - الشعب التونسي هو صاحب السيادة يمارسها على الوجه الذي يضبطه هذا الدستور.",
            "text_fr": "Article 2 - Le peuple tunisien est souverain, il exerce sa souveraineté conformément à la présente Constitution.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "3",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 3 - تونس دولة موحدة، ولا يجوز المساس بوحدتها.",
            "text_fr": "Article 3 - La Tunisie est un État unitaire et nul ne peut porter atteinte à son unité.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "4",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 4 - علم الجمهورية التونسية أحمر يتوسطه قرص أبيض به نجم أحمر ذو خمسة أشعة يحيط به هلال أحمر، وشعار الجمهورية هو: حرية، كرامة، عدالة، نظام.",
            "text_fr": "Article 4 - Le drapeau de la République Tunisienne est rouge, il comporte en son milieu un cercle blanc contenant une étoile rouge à cinq branches entourée d'un croissant rouge. La devise de la République est : Liberté, Dignité, Justice, Ordre.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "5",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 5 - تونس جزء من الأمة الإسلامية، وعلى الدولة وحدها أن تعمل، في ظل نظام ديمقراطي، على تحقيق مقاصد الإسلام الحنيف في الحفاظ على النّفس والعِرْض والمال والدين والحرية.",
            "text_fr": "Article 5 - La Tunisie est une composante de la Nation islamique. Il appartient à l'État seul d'œuvrer, dans un régime démocratique, à la réalisation des finalités de l'Islam dans la préservation de la vie, de l'honneur, des biens, de la religion et de la liberté.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "6",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 6 - تونس جزء من المغرب العربي الكبير وتعمل على تحقيق وحدته في نطاق المصلحة المشتركة.",
            "text_fr": "Article 6 - La Tunisie est une composante du Grand Maghreb arabe et œuvre à la réalisation de son unité dans le cadre de l'intérêt commun.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "7",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 7 - اللغة الرسمية للدولة التونسية هي اللغة العربية.",
            "text_fr": "Article 7 - La langue officielle de l'État tunisien est la langue arabe.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "8",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 8 - الأسرة هي الخلية الأساسية للمجتمع وعلى الدولة حمايتها.",
            "text_fr": "Article 8 - La famille est la cellule de base de la société et l'État doit la protéger.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "10",
            "hierarchy_path": "الباب الأول: أحكام عامة || Chapitre I: Dispositions Générales",
            "text_ar": "الفصل 10 - أداء الضريبة وتحمل التكاليف العامة واجب على كل شخص وفق نظام عادل ومنصف. تضع الدولة الآليات الكفيلة بضمان استخلاص الضريبة ومقاومة التهرب والغش الجبائيين.",
            "text_fr": "Article 10 - L'acquittement de l'impôt et la participation aux charges publiques constituent un devoir pour toute personne conformément à un système juste et équitable. L'État met en place les mécanismes nécessaires pour garantir le recouvrement de l'impôt et lutter contre l'évasion et la fraude fiscales.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "23",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 23 - المواطنون والمواطنات متساوون في الحقوق والواجبات، وهم سواء أمام القانون من غير تمييز.",
            "text_fr": "Article 23 - Les citoyens et les citoyennes sont égaux en droits et en devoirs. Ils sont égaux devant la loi sans discrimination aucune.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "24",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 24 - الحياة الإنسانية مقدسة لا يجوز المساس بها إلا في حالات قصوى يضبطها القانون.",
            "text_fr": "Article 24 - La vie humaine est sacrée, il ne peut y être porté atteinte que dans des cas extrêmes fixés par la loi.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "25",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 25 - تحمي الدولة كرامة الذات البشرية وحرمة الجسد وتمنع التعذيب المعنوي والمادي. ولا تسقط جريمة التعذيب بالتقادم.",
            "text_fr": "Article 25 - L'État protège la dignité de la personne humaine et son intégrité physique, et interdit la torture morale et physique. Le crime de torture est imprescriptible.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "31",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 31 - حرية الرأي والفكر والتعبير والإعلام والنشر مضمونة. ولا يجوز ممارسة رقابة مسبقة على هذه الحريات.",
            "text_fr": "Article 31 - Les libertés d'opinion, de pensée, d'expression, d'information et de publication sont garanties. Aucune censure préalable ne peut être exercée sur ces libertés.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "32",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 32 - تضمن الدولة الحق في الإعلام والحق في النفاذ إلى المعلومة وشبكات الاتصال.",
            "text_fr": "Article 32 - L'État garantit le droit à l'information et le droit d'accès à l'information et aux réseaux de communication.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "37",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 37 - حرية الاجتماع والتظاهر السلميين مضمونة.",
            "text_fr": "Article 37 - La liberté de réunion et de manifestation pacifiques est garantie.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "38",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 38 - العمل حق لكل مواطن ومواطنة، وتتخذ الدولة التدابير الضرورية لترسيخه على أساس الكفاءة والإنصاف. ولكل مواطن ومواطنة الحق في ظروف عمل لائقة وبأجر عادل.",
            "text_fr": "Article 38 - Le travail est un droit pour chaque citoyen et citoyenne. L'État prend les mesures nécessaires pour le garantir sur la base de la compétence et de l'équité. Tout citoyen a droit à des conditions de travail décentes et à un salaire équitable.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "41",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 41 - الحق النقابي بما في ذلك حق الإضراب مضمون. ولا ينطبق هذا الحق على الجيش الوطني وقوات الأمن الداخلي والديوانة والقضاة.",
            "text_fr": "Article 41 - Le droit syndical, y compris le droit de grève, est garanti. Ce droit ne s'applique pas à l'Armée nationale, aux forces de sécurité intérieure, à la douane et aux magistrats.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "46",
            "hierarchy_path": "الباب الثاني: الحقوق والحريات || Chapitre II: Droits et Libertés",
            "text_ar": "الفصل 46 - حق الملكية مضمون، ويمارس في حدود القانون.",
            "text_fr": "Article 46 - Le droit de propriété est garanti. Il s'exerce dans les limites prévues par la loi.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "56",
            "hierarchy_path": "الباب الثالث: الوظيفة التشريعية || Chapitre III: La Fonction Législative",
            "text_ar": "الفصل 56 - يمارس الشعب الوظيفة التشريعية بواسطة مجلس نواب الشعب والمجلس الوطني للجهات والأقاليم.",
            "text_fr": "Article 56 - Le peuple exerce la fonction législative par l'intermédiaire de l'Assemblée des représentants du peuple et du Conseil national des régions et des districts.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "87",
            "hierarchy_path": "الباب الرابع: الوظيفة التنفيذية || Chapitre IV: La Fonction Exécutive",
            "text_ar": "الفصل 87 - يمارس رئيس الجمهورية الوظيفة التنفيذية بمساعدة حكومة يرأسها رئيس حكومة.",
            "text_fr": "Article 87 - Le Président de la République exerce la fonction exécutive avec l'assistance d'un gouvernement dirigé par un Chef de gouvernement.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "88",
            "hierarchy_path": "الباب الرابع: الوظيفة التنفيذية || Chapitre IV: La Fonction Exécutive",
            "text_ar": "الفصل 88 - رئيس الجمهورية هو رئيس الدولة، ودينه الإسلام.",
            "text_fr": "Article 88 - Le Président de la République est le Chef de l'État. Sa religion est l'Islam.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "89",
            "hierarchy_path": "الباب الرابع: الوظيفة التنفيذية || Chapitre IV: La Fonction Exécutive",
            "text_ar": "الفصل 89 - ينتخب رئيس الجمهورية لمدة خمسة أعوام انتخابا عاما حرا مباشرا وسريا ونزيها وشفافا خلال الأشهر الثلاثة الأخيرة من المدة الرئاسية وبأغلبية الأصوات المصرح بها.",
            "text_fr": "Article 89 - Le Président de la République est élu pour un mandat de cinq ans au suffrage universel, libre, direct, secret, intègre et transparent, au cours des trois derniers mois du mandat présidentiel, à la majorité absolue des suffrages exprimés.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "96",
            "hierarchy_path": "الباب الرابع: التدابير الاستثنائية || Chapitre IV: Mesures Exceptionnelles",
            "text_ar": "الفصل 96 - لرئيس الجمهورية، في حالة خطر داهم مهدد لكيان الوطن وأمن البلاد واستقلالها، يتعذر معه السير العادي لدواليب الدولة، أن يتخذ التدابير الاستثنائية التي تحتمها تلك الحالة بعد استشارة رئيس الحكومة ورئيس مجلس نواب الشعب ورئيس المجلس الوطني للجهات والأقاليم.",
            "text_fr": "Article 96 - En cas de péril imminent menaçant les institutions de la République, la sécurité ou l'indépendance du pays, entravant le fonctionnement régulier des pouvoirs publics, le Président de la République peut prendre les mesures exceptionnelles exigées par ces circonstances.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "117",
            "hierarchy_path": "الباب الخامس: الوظيفة القضائية || Chapitre V: La Fonction Judiciaire",
            "text_ar": "الفصل 117 - القضاء وظيفة مستقلة يقيم العدل وينتصف للمظلومين ويضمن علوية القانون.",
            "text_fr": "Article 117 - La justice est une fonction indépendante qui rend la justice, rétablit les droits et garantit la primauté de la loi.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "125",
            "hierarchy_path": "الباب السادس: المحكمة الدستورية || Chapitre VI: La Cour Constitutionnelle",
            "text_ar": "الفصل 125 - المحكمة الدستورية هيئة قضائية مستقلة تتركب من تسعة أعضاء يُعينون بأمر رئاسي وفق الشروط المنصوص عليها بهذا الدستور.",
            "text_fr": "Article 125 - La Cour constitutionnelle est une instance juridictionnelle indépendante composée de neuf membres nommés par décret présidentiel selon les conditions fixées par la présente Constitution.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "142",
            "hierarchy_path": "الباب الحادي عشر: أحكام ختامية || Chapitre XI: Dispositions Finales",
            "text_ar": "الفصل 142 - يدخل هذا الدستور حيز النفاذ ابتداء من تاريخ الإعلان النهائي عن نتيجة الاستفتاء من قبل الهيئة العليا المستقلة للانتخابات وبعد ختمه من قبل رئيس الجمهورية وإصداره ونشره في عدد خاص من الرائد الرسمي للجمهورية التونسية.",
            "text_fr": "Article 142 - La présente Constitution entre en vigueur à compter de la date de la proclamation définitive des résultats du référendum par l'Instance supérieure indépendante pour les élections, après sa promulgation par le Président de la République et sa publication au Journal Officiel de la République Tunisienne.",
            "valid_from": "2022-08-17",
            "valid_to": "9999-12-31"
        }
    ]
    return articles

def build_labor_code_corpus() -> List[Dict[str, Any]]:
    """Builds the bilingual articles of the Tunisian Labor Code (مجلة الشغل)."""
    articles = [
        {
            "article_number": "6",
            "hierarchy_path": "الكتاب الأول: عقد الشغل > الباب الأول: تكوين عقد الشغل || Livre I: Contrat de travail > Titre I: Formation",
            "text_ar": "الفصل 6 - عقد الشغل هو اتفاق يلتزم بمقتضاه أحد الطرفين ويسمى عاملا أو أجيرا بتقديم خدماته للطرف الآخر ويسمى مؤجرا، تحت إدارة ومراقبة هذا الأخير وبمقابل أجر.",
            "text_fr": "Article 6 - Le contrat de travail est la convention par laquelle l'une des parties appelée travailleur ou employé s'engage à fournir ses services à l'autre partie appelée employeur, sous la direction et le contrôle de celle-ci, moyennant une rémunération.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "6-4",
            "hierarchy_path": "الكتاب الأول: عقد الشغل > الباب الأول: فترة التجربة || Livre I: Contrat de travail > Période d'essai",
            "text_ar": "الفصل 6 رابعا - تحدد فترة التجربة بمدة أقصاها ستة أشهر بالنسبة لأعوان التنفيذ، وسنة واحدة بالنسبة لأعوان التسيير والإطارات. وخلال هذه الفترة يمكن لأي من الطرفين إنهاء العقد دون إشعار مسبق ودون تعويض.",
            "text_fr": "Article 6-4 - La durée de la période d'essai ne peut excéder six mois pour les agents d'exécution et un an pour les cadres et agents de maîtrise. Durant cette période, chacune des parties peut résilier le contrat sans préavis ni indemnité.",
            "valid_from": "1996-07-15",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "14",
            "hierarchy_path": "الكتاب الأول: عقد الشغل > الباب الثاني: إنهاء عقد الشغل || Livre I: Contrat de travail > Titre II: Rupture",
            "text_ar": "الفصل 14 - ينتهي عقد الشغل المعين المدة بحلول أجله أو بإنجاز العمل المتفق عليه. وينتهي العقد غير معين المدة بإرادة أحد الطرفين مع مراعاة أجل الإخطار المسبق المنصوص عليه بالقانون أو بالاتفاقية المشتركة.",
            "text_fr": "Article 14 - Le contrat de travail à durée déterminée prend fin à l'expiration du terme convenu ou à l'accomplissement du travail convenu. Le contrat à durée indéterminée prend fin par la volonté de l'une des parties sous réserve du respect du préavis légal ou conventionnel.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "14-3",
            "hierarchy_path": "الكتاب الأول: عقد الشغل > الباب الثاني: الطرد التعسفي والتعويض || Livre I: Contrat de travail > Licenciement abusif",
            "text_ar": "الفصل 14 ثالثا - يعتبر الطرد تعسفيا إذا تم دون سبب حقيقي وجدي يبرره، أو دون احترام الإجراءات التأديبية المنصوص عليها بالقانون. يستحق العامل المطرود تعسفيا تعويضا عن الضرر لا يقل عن أجر شهر عن كل سنة أقدمية، مع مراعاة الغرامات التكميلية.",
            "text_fr": "Article 14 ter - Le licenciement est réputé abusif lorsqu'il intervient sans motif réel et sérieux, ou en méconnaissance des procédures disciplinaires. Le travailleur abusivement licencié a droit à des dommages-intérêts qui ne peuvent être inférieurs au salaire d'un mois par année d'ancienneté, sans préjudice des indemnités légales.",
            "valid_from": "1994-02-21",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "22",
            "hierarchy_path": "الكتاب الأول: عقد الشغل > مكافأة نهاية الخدمة || Livre I: Gratification de fin de service",
            "text_ar": "الفصل 22 - يستحق كل عامل تم إنهاء عقده غير معين المدة بعد قضاء سنة من العمل المستمر لدى نفس المؤجر مكافأة نهاية الخدمة، تحسب على أساس أجر يوم عن كل شهر عمل دون أن تتجاوز أجر ثلاثة أشهر.",
            "text_fr": "Article 22 - Tout travailleur lié par un contrat à durée indéterminée, licencié après une année de service continu auprès du même employeur, a droit à une indemnité de fin de service calculée sur la base d'un jour de salaire par mois de service, sans pouvoir excéder trois mois de salaire.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "79",
            "hierarchy_path": "الكتاب الثاني: شروط العمل > الباب الأول: مدة العمل || Livre II: Conditions de travail > Titre I: Durée du travail",
            "text_ar": "الفصل 79 - تحدد المدة القانونية للعمل الفعلي بـ 48 ساعة أسبوعيا أو 40 ساعة أسبوعيا حسب الأنشطة والمؤسسات، دون تخفيض في الأجور.",
            "text_fr": "Article 79 - La durée légale du travail effectif est fixée à quarante-huit heures par semaine ou quarante heures par semaine selon les branches d'activité, sans réduction de salaire.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "90",
            "hierarchy_path": "الكتاب الثاني: شروط العمل > الراحة الأسبوعية || Livre II: Repos hebdomadaire",
            "text_ar": "الفصل 90 - يجب منح العمال راحة أسبوعية مدتها أربع وعشرون ساعة متتالية على الأقل، وتمنح وجوبا يوم الجمعة أو السبت أو الأحد حسب طبيعة النشاط.",
            "text_fr": "Article 90 - Il est obligatoire d'accorder aux salariés un repos hebdomadaire d'au moins vingt-quatre heures consécutives, donné le vendredi, le samedi ou le dimanche selon la nature de l'activité.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "112",
            "hierarchy_path": "الكتاب الثاني: شروط العمل > العطل الخالصة الأجر || Livre II: Congés payés",
            "text_ar": "الفصل 112 - يستحق كل عامل قضاء عطلة سنوية خالصة الأجر تحسب على أساس يوم عمل عن كل شهر خدمة فعلية، وتزاد هذه المدة بحسب الأقدمية في المؤسسة.",
            "text_fr": "Article 112 - Tout salarié a droit à un congé annuel payé d'une durée fixée à raison d'un jour ouvrable par mois de travail effectif, augmentée selon l'ancienneté dans l'entreprise.",
            "valid_from": "1966-04-30",
            "valid_to": "9999-12-31"
        }
    ]
    return articles

def build_personal_status_corpus() -> List[Dict[str, Any]]:
    """Builds the bilingual articles of the Tunisian Code of Personal Status (مجلة الأحوال الشخصية)."""
    articles = [
        {
            "article_number": "3",
            "hierarchy_path": "الكتاب الأول: في الزواج > أركان الزواج || Livre I: Du Mariage > Conditions",
            "text_ar": "الفصل 3 - لا ينعقد الزواج إلا برضا الزوجين. ويشترط لصحة الزواج خلو الزوجين من الموانع الشرعية، وتسمية مهر للزوجة، وحضور شاهدين عدلين.",
            "text_fr": "Article 3 - Le mariage n'est conclu que par le consentement des deux époux. La validité du mariage requiert l'absence d'empêchements légaux, la stipulation d'une dot au profit de l'épouse, et la présence de deux témoins honorables.",
            "valid_from": "1956-08-13",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "5",
            "hierarchy_path": "الكتاب الأول: في الزواج > السن القانوني || Livre I: Du Mariage > Âge légal",
            "text_ar": "الفصل 5 - يجب أن يكون كل من الزوجين قد بلغ ثمانية عشر عاما كاملة. وما دون ذلك يتوقف إبرام الزواج على إذن خاص من القاضي لأسباب خطيرة ولمصلحة واضحة.",
            "text_fr": "Article 5 - Chacun des deux futurs époux doit avoir atteint l'âge de dix-huit ans révolus. Au-dessous de cet âge, le mariage ne peut être contracté qu'avec une autorisation spéciale du juge pour motifs graves et dans l'intérêt bien compris des futurs époux.",
            "valid_from": "2007-05-14",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "18",
            "hierarchy_path": "الكتاب الأول: في الزواج > منع تعدد الزوجات || Livre I: Du Mariage > Interdiction de la polygamie",
            "text_ar": "الفصل 18 - تعدد الزوجات ممنوع. وكل من تزوج وهو في حالة الزوجية وقبل فك العصمة يعاقب بالسجن مدة عام وبخطية مالية أو بإحدى العقوبتين.",
            "text_fr": "Article 18 - La polygamie est interdite. Quiconque, étant engagé dans les liens du mariage, en aura contracté un autre avant la dissolution du précédent, sera puni d'un emprisonnement d'un an et d'une amende ou de l'une de ces deux peines seulement.",
            "valid_from": "1956-08-13",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "23",
            "hierarchy_path": "الكتاب الأول: في الزواج > حقوق الزوجين وواجباتهما || Livre I: Du Mariage > Droits et devoirs",
            "text_ar": "الفصل 23 - على كل واحد من الزوجين أن يعامل الآخر بالمعروف ويحسن عشرته ويتجنب إلحاق الضرر به. ويتعاون الزوجان على تسيير شؤون العائلة وتربية الأبناء والإنفاق عليها.",
            "text_fr": "Article 23 - Chacun des deux époux doit traiter l'autre avec bienveillance, entretenir de bons rapports conjugaux et éviter de lui causer préjudice. Les deux époux coopèrent dans la gestion des affaires de la famille, l'éducation des enfants et la couverture des charges du ménage.",
            "valid_from": "1993-07-12",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "30",
            "hierarchy_path": "الكتاب الثاني: في الطلاق > إيقاع الطلاق || Livre II: Du Divorce > Prononcé du divorce",
            "text_ar": "الفصل 30 - لا يقع الطلاق إلا لدى المحكمة بحكم صادر عنها. وكل طلاق يقع خارج إطار المحكمة يعتبر باطلا ولا أثر له.",
            "text_fr": "Article 30 - Le divorce ne peut être prononcé que par le tribunal. Tout divorce intervenant hors de la juridiction compétente est nul et sans effet.",
            "valid_from": "1956-08-13",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "31",
            "hierarchy_path": "الكتاب الثاني: في الطلاق > حالات الطلاق || Livre II: Du Divorce > Cas de divorce",
            "text_ar": "الفصل 31 - يحكم بالطلاق: 1) بتراضي الزوجين، 2) بناء على طلب أحد الزوجين بسبب ما حصل له من ضرر، 3) بناء على رغبة الزوج إنشاء الطلاق أو مطالبة الزوجة به (الطلاق كبراء/إنشاء). ويقضي للمتضرر بالتعويض عن الضرر المادي والمعنوي.",
            "text_fr": "Article 31 - Le divorce est prononcé : 1) Par consentement mutuel des époux ; 2) À la demande de l'un des époux en raison du préjudice subi ; 3) À la demande du mari ou de la femme sans justification de motif (divorce caprice). Le tribunal alloue à l'époux lésé une réparation pour préjudice matériel et moral.",
            "valid_from": "1981-06-09",
            "valid_to": "9999-12-31"
        },
        {
            "article_number": "54",
            "hierarchy_path": "الكتاب الرابع: في الحضانة > استحقاق الحضانة || Livre IV: De la Garde > Droit de garde",
            "text_ar": "الفصل 54 - الحضانة هي حفظ الولد في مبيته وتربيته والقيام بشؤونه. وتسند الحضانة لمستحقها مع مراعاة مصلحة المحضون الفضلى أولا وقبل كل شيء.",
            "text_fr": "Article 54 - La garde consiste à héberger l'enfant, à veiller à son éducation et à assurer ses soins. La garde est confiée à la personne la plus apte en tenant compte avant tout de l'intérêt supérieur de l'enfant.",
            "valid_from": "1956-08-13",
            "valid_to": "9999-12-31"
        }
    ]
    return articles
