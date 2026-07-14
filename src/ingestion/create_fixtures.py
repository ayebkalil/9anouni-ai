import json
import os
import uuid
from typing import Any

# A dictionary of realistic Arabic legal article templates to make the fixtures represent real legal content  # noqa: E501
ARABIC_LEGAL_TEMPLATES = [
    "تونس دولة حرة، مستقلة، ذات سيادة، الإسلام دينها، والعربية لغتها، والجمهورية نظامها.",
    "الشعب هو صاحب السيادة ومصدر السلطات، ويمارسها عبر ممثليه المنتخبين أو عبر الاستفتاء.",
    "علم الجمهورية التونسية أحمر يوسطه قرص أبيض به نجم ذو خمس أشعة يحيط به هلال أحمر حسبما يضبطه القانون.",  # noqa: E501
    "تلتزم الدولة بالعمل على تحقيق العدالة الاجتماعية، والتنمية المستدامة، والتوازن بين الجهات.",
    "المواطنون والمواطنات متساوون في الحقوق والواجبات، وهم سواء أمام القانون دون تمييز.",
    "حرية الرأي والفكر والتعبير والإعلام والنشر مضمونة. لا يجوز ممارسة رقابة مسبقة على هذه الحريات.",  # noqa: E501
    "حرية الاجتماع والتظاهر السلمي مضمونة، وتمارس وفق ما يضبطه القانون.",
    "الحق في الملكية مضمون، ولا يمكن الحد منه إلا بمقتضى القانون وبمقابل عادل.",
    "تضمن الدولة تكافؤ الفرص بين الرجل والمرأة في تحمل مختلف المسؤوليات وفي جميع المجالات.",
    "القضاء سلطة مستقلة تضمن إقامة العدل، وعلوية الدستور، وسيادة القانون، وحماية الحقوق والحريات."
]

FRENCH_LEGAL_TEMPLATES = [
    "La Tunisie est un Etat libre, indépendant et souverain; sa religion est l'Islam, sa langue l'arabe et son régime la République.",  # noqa: E501
    "Le peuple est souverain, source des pouvoirs, qu'il exerce par ses représentants élus ou par voie de référendum.",  # noqa: E501
    "Le drapeau de la République Tunisienne est rouge, il comporte en son milieu un cercle blanc contenant une étoile à cinq branches entourée d'un croissant rouge.",  # noqa: E501
    "L'Etat s'engage à œuvrer pour réaliser la justice sociale, le développement durable et l'équilibre régional.",  # noqa: E501
    "Les citoyens et les citoyennes sont égaux en droits et en devoirs. Ils sont égaux devant la loi sans discrimination.",  # noqa: E501
    "Les libertés d'opinion, de pensée, d'expression, d'information et de publication sont garanties. Aucun contrôle préalable n'est exercé.",  # noqa: E501
    "Le droit d'assemblée et de manifestation pacifiques est garanti et s'exerce conformément à la loi.",  # noqa: E501
    "Le droit de propriété est garanti. Il ne peut y être porté atteinte que par la loi et moyennant une juste indemnisation.",  # noqa: E501
    "L'Etat garantit l'égalité des chances entre l'homme et la femme pour l'accès aux différentes responsabilités.",  # noqa: E501
    "La justice est un pouvoir indépendant qui garantit l'équité, la suprématie de la Constitution et la protection des droits."  # noqa: E501
]

def generate_fixtures() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    fixtures_dir = os.path.join(base_dir, "data")
    os.makedirs(fixtures_dir, exist_ok=True)
    
    fixtures: list[dict[str, Any]] = []
    
    # 1. Generate 140 articles of "constitution_2014"
    for i in range(1, 141):
        tpl_idx = (i - 1) % len(ARABIC_LEGAL_TEMPLATES)
        text_ar = ARABIC_LEGAL_TEMPLATES[tpl_idx]
        text_fr = FRENCH_LEGAL_TEMPLATES[tpl_idx]
        
        # Determine chapters
        chapter_num = (i - 1) // 15 + 1
        hierarchy_path = (
            f"الباب {chapter_num} > الأحكام العامة || "
            f"Chapitre {chapter_num} > Dispositions Générales"
        )
        
        article_version: dict[str, Any] = {
            "version_id": str(uuid.uuid4()),
            "article_id": f"constitution_2014:article-{i}",
            "code_id": "constitution_2014",
            "article_number": str(i),
            "hierarchy_path": hierarchy_path,
            "text_ar": f"الفصل {i} - {text_ar}",
            "text_fr": f"Article {i} - {text_fr}",
            "valid_from": "2014-02-10",
            "valid_to": "2022-08-15",
            "status": "superseded",  # Constitution 2014 is superseded by 2022
            "source_ref": {
                "source_id": "src-constitution-2014-ar-fr",
                "page_ids": [f"p{i // 5 + 1:04d}"],
                "official_reference": (
                    "Journal Officiel de la République Tunisienne, "
                    "issue 12, 2014"
                )
            },
            "created_by_op": "seed-fixture-run-01"
        }
        fixtures.append(article_version)
        
    # 2. Generate 60 articles of "finance_law_2020" to reach 200 total articles
    for i in range(1, 61):
        # Finance laws typically modify codes or set tax/budget parameters
        chapter_num = (i - 1) // 10 + 1
        hierarchy_path = (
            f"الباب {chapter_num} > الأحكام المالية || "
            f"Titre {chapter_num} > Dispositions Financières"
        )
        
        text_ar = (
            "يرخص للحكومة جباية الضرائب والمعاليم العمومية "
            f"المحددة بالجدول الملحق بهذا القانون لسنة 2020. الفصل {i}."
        )
        
        # Arabic only as authorities are primary in Arabic
        finance_article_version: dict[str, Any] = {
            "version_id": str(uuid.uuid4()),
            "article_id": f"finance_law_2020:article-{i}",
            "code_id": "finance_law_2020",
            "article_number": str(i),
            "hierarchy_path": hierarchy_path,
            "text_ar": text_ar,
            "text_fr": None,  # French translation not available
            "valid_from": "2020-01-01",
            "valid_to": "9999-12-31", # Active/current version
            "status": "active",
            "source_ref": {
                "source_id": "src-finance-law-2020-ar",
                "page_ids": [f"p{i // 3 + 1:04d}"],
                "official_reference": "الرائد الرسمي للجمهورية التونسية، قانون المالية لسنة 2020"
            },
            "created_by_op": "seed-fixture-run-01"
        }
        fixtures.append(finance_article_version)
        
    # Write to file
    output_path = os.path.join(fixtures_dir, "fixtures_200_articles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated 200 structured articles at: {output_path}")

    # Generate parser input fixtures
    parser_fixtures_dir = os.path.join(base_dir, "data", "parser_fixtures")
    os.makedirs(parser_fixtures_dir, exist_ok=True)
    
    # 1. fixture_parser_simple_fr.json
    simple_fr = [{
        "page_id": "p001",
        "source_id": "src-fr-test",
        "blocks": [
            {"block_id": "b1", "text": "Titre premier - Dispositions Générales", "language": "fr"},
            {"block_id": "b2", "text": "Chapitre I - Les Définitions", "language": "fr"},
            {"block_id": "b3", "text": "Article premier - Le présent code régit les relations de travail.", "language": "fr"},
            {"block_id": "b4", "text": "Article 2 - Est considéré comme travailleur toute personne qui s'engage...", "language": "fr"},
            {"block_id": "b5", "text": "Article 3 - Les dispositions du présent code s'appliquent...", "language": "fr"}
        ]
    }]
    with open(os.path.join(parser_fixtures_dir, "fixture_parser_simple_fr.json"), "w", encoding="utf-8") as f:
        json.dump(simple_fr, f, ensure_ascii=False, indent=2)

    # 2. fixture_parser_bis_ter_ar.json
    bis_ter_ar = [{
        "page_id": "p002",
        "source_id": "src-ar-bis-ter",
        "blocks": [
            {"block_id": "b1", "text": "الفصل 12 - يعاقب بالسجن...", "language": "ar"},
            {"block_id": "b2", "text": "الفصل 12 مكرر - تضاعف العقوبة...", "language": "ar"},
            {"block_id": "b3", "text": "الفصل 12 ثالثا - لا تنطبق أحكام الفصل...", "language": "ar"}
        ]
    }]
    with open(os.path.join(parser_fixtures_dir, "fixture_parser_bis_ter_ar.json"), "w", encoding="utf-8") as f:
        json.dump(bis_ter_ar, f, ensure_ascii=False, indent=2)

    # 3. fixture_parser_table_tax.json
    table_tax = [{
        "page_id": "p003",
        "source_id": "src-table-tax",
        "blocks": [
            {"block_id": "b1", "text": "الفصل 40 - تحدد نسب الأداء كما يلي:", "language": "ar"},
            {
                "block_id": "b2", 
                "type": "table",
                "text": "المنتوج | النسبة\nشاي | 19%\nقهوة | 19%", 
                "caption": "جدول نسب الأداء",
                "rows": [["المنتوج", "النسبة"], ["شاي", "19%"], ["قهوة", "19%"]],
                "columns": ["المنتوج", "النسبة"],
                "language": "ar"
            }
        ]
    }]
    with open(os.path.join(parser_fixtures_dir, "fixture_parser_table_tax.json"), "w", encoding="utf-8") as f:
        json.dump(table_tax, f, ensure_ascii=False, indent=2)

    # 4. fixture_parser_duplicate_reject.json (Loader/Validator input)
    # The validator validates structured parsed articles (parser output).
    duplicate_reject = [
        {
            "article_id": "tax:article-53",
            "article_number": "53",
            "hierarchy_path": "Chapter 1",
            "text_ar": "Text one",
            "source_ref": {"source_id": "src-dup", "page_ids": ["p1"], "blocks": ["b1"]}
        },
        {
            "article_id": "tax:article-53",
            "article_number": "53",
            "hierarchy_path": "Chapter 1",
            "text_ar": "Text two",
            "source_ref": {"source_id": "src-dup", "page_ids": ["p2"], "blocks": ["b2"]}
        }
    ]
    with open(os.path.join(parser_fixtures_dir, "fixture_parser_duplicate_reject.json"), "w", encoding="utf-8") as f:
        json.dump(duplicate_reject, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated auxiliary parser fixtures at: {parser_fixtures_dir}")

if __name__ == "__main__":
    generate_fixtures()
