"""
Module to wrap Tesseract OCR and run text extraction on segmented page columns.
Generates ocr_text.jsonl containing clean OCR outputs with page/block mapping.
"""

import json
import os
import sys
import uuid
from typing import Any, Dict, List

import fitz  # PyMuPDF
import pytesseract
from dotenv import load_dotenv
from PIL import Image

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, ".env"))

# Set Tesseract binary path from env
TESS_CMD = os.getenv("TESSERACT_CMD")
if TESS_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESS_CMD

from src.ingestion.ocr.renderer import render_pdf_to_images  # noqa: E402
from src.ingestion.ocr.segmenter import segment_page_columns  # noqa: E402


def run_ocr_on_column(image_path: str, language: str = "ar") -> tuple[str, float]:
    """
    Runs pytesseract OCR on a cropped column image.

    Args:
        image_path: Absolute path to the cropped column PNG.
        language: Language for OCR ("ar" -> "ara", "fr" -> "fra").

    Returns:
        A tuple of (extracted clean text, average confidence score 0.0-1.0).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found for OCR: {image_path}")

    # Map language string to Tesseract language code
    lang_code = "ara" if language == "ar" else "fra"

    # Load image and extract text and data
    img = Image.open(image_path)
    from pytesseract import Output
    data = pytesseract.image_to_data(img, lang=lang_code, output_type=Output.DICT)
    
    lines = []
    current_line_words = []
    current_line_id = None
    confidences = []
    
    for i in range(len(data['text'])):
        word = data['text'][i].strip()
        conf = data['conf'][i]
        
        # Unique identifier for the line
        line_id = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
        
        if line_id != current_line_id:
            if current_line_words:
                lines.append(" ".join(current_line_words))
                current_line_words = []
            current_line_id = line_id
            
        # Tesseract sets conf to -1 (or sometimes empty string) for non-text blocks
        if word and conf != -1:
            current_line_words.append(word)
            try:
                confidences.append(float(conf))
            except ValueError:
                pass
                
    if current_line_words:
        lines.append(" ".join(current_line_words))
        
    text = "\n".join(lines)
    # Tesseract returns confidences in a 0-100 range. We scale to 0.0-1.0
    avg_conf = (sum(confidences) / len(confidences) / 100.0) if confidences else 0.0
    
    return str(text.strip()), round(avg_conf, 3)

def run_ocr_pipeline(
    pdf_path: str,
    run_id: str,
    base_processed_dir: str,
    language: str = "ar",
    source_id: str | None = None,
    columns_count: int | None = None
) -> str:
    """
    Runs the entire OCR pipeline on the input PDF:
    1. Renders PDF pages to 300 DPI PNGs.
    2. Segment pages into reading-ordered columns.
    3. Runs Tesseract OCR on each column.
    4. Writes results to ocr_text.jsonl in the processed run folder.

    Args:
        pdf_path: Path to the input PDF file.
        run_id: Unique identifier for this run.
        base_processed_dir: Directory where processed outputs are saved.
        language: Language of the PDF ("ar" or "fr").
        source_id: Stable identifier for the PDF source.
        columns_count: Number of columns (1 or 2). Auto-detected if None.

    Returns:
        The absolute path to the generated ocr_text.jsonl file.
    """
    if not source_id:
        # Fallback source_id based on filename
        source_id = f"src-{os.path.splitext(os.path.basename(pdf_path))[0]}"

    # Auto-detect columns_count if not provided
    if columns_count is None:
        columns_count = 2  # Default to 2 columns
        pdf_dir = os.path.dirname(pdf_path)
        manifest_path = os.path.join(pdf_dir, "manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as mf:
                    manifest = json.load(mf)
                    layout = manifest.get("layout")
                    code_id = manifest.get("code_id", "")
                    if layout == "single_column" or "finance_law" in code_id:
                        columns_count = 1
            except Exception as e:
                print(f"Warning: Could not parse manifest at {manifest_path}: {e}")

    # Step 1: Render pages
    print(f"[{run_id}] Step 1: Rendering PDF pages to PNG at 300 DPI...")
    page_images = render_pdf_to_images(pdf_path, run_id, base_processed_dir)

    ocr_records: List[Dict[str, Any]] = []
    
    # Step 2 & 3: Segment and OCR
    for idx, img_path in enumerate(page_images):
        page_num = idx  # 0-indexed page
        page_id = f"p{page_num + 1:04d}"
        total_pages = len(page_images)
        print(f"[{run_id}] Step 2 & 3: Segmenting and OCR on Page {page_num + 1}/{total_pages} (columns_count={columns_count})...")

        # Segment page into reading-ordered columns
        columns = segment_page_columns(
            pdf_path,
            page_num,
            img_path,
            run_id,
            base_processed_dir,
            language=language,
            columns_count=columns_count
        )

        from src.ingestion.ocr.llm_corrector import correct_ocr_text
        
        blocks: List[Dict[str, Any]] = []
        for col in columns:
            col_id = col["column_id"]
            col_img_path = col["image_path"]
            
            # Extract text via Tesseract
            extracted_text, conf = run_ocr_on_column(col_img_path, language=language)
            
            # Apply LLM post-correction
            block_id = f"{page_id}-col-{col_id}"
            extracted_text = correct_ocr_text(extracted_text, conf, block_id)
            
            # Form layout block representation
            block = {
                "block_id": block_id,
                "type": "column_body",
                "bbox": list(col["bbox_points"]),
                "text": extracted_text,
                "language": language,
                "ocr_confidence": conf
            }
            blocks.append(block)

        # Append page record
        record = {
            "run_id": run_id,
            "source_id": source_id,
            "page_id": page_id,
            "blocks": blocks
        }
        ocr_records.append(record)

    # Step 4: Write to ocr_text.jsonl
    run_dir = os.path.join(base_processed_dir, run_id)
    os.makedirs(run_dir, exist_ok=True)
    ocr_jsonl_path = os.path.join(run_dir, "ocr_text.jsonl")

    with open(ocr_jsonl_path, "w", encoding="utf-8") as f:
        for rec in ocr_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"[{run_id}] Ingestion complete! Saved OCR results to: {ocr_jsonl_path}")
    return os.path.abspath(ocr_jsonl_path)

if __name__ == "__main__":
    # Smoke test for OCR pipeline on 2 pages of the 2020 rectificative law
    test_run_id = f"test-ocr-run-{uuid.uuid4().hex[:8]}"
    test_pdf_path = os.path.join(
        project_root, "data", "raw", "finance_law_2020_rect", "original.pdf"
    )
    test_processed_dir = os.path.join(project_root, "data", "processed")

    if os.path.exists(test_pdf_path):
        print(f"Starting pipeline smoke test on: {test_pdf_path}")
        # Create a temporary PDF with only 1 page to make the test super fast
        temp_pdf_path = os.path.join(project_root, "data", "processed", f"temp_{test_run_id}.pdf")
        os.makedirs(test_processed_dir, exist_ok=True)
        
        # Read page 1 and save to temp_pdf using fitz
        src = fitz.open(test_pdf_path)
        dest = fitz.open()
        dest.insert_pdf(src, from_page=0, to_page=0)  # page 1
        dest.save(temp_pdf_path)
        dest.close()
        src.close()

        try:
            jsonl_path = run_ocr_pipeline(
                temp_pdf_path,
                test_run_id,
                test_processed_dir,
                language="ar",
                source_id="src-finance-law-2020-rect"
            )
            print("Pipeline run successful! Reading output record:")
            with open(jsonl_path, "r", encoding="utf-8") as f:
                first_line = json.loads(f.readline())
                print("- Page ID:", first_line["page_id"])
                for b in first_line["blocks"]:
                    snippet = b["text"][:150].replace('\n', ' ')
                    escaped_snippet = snippet.encode('unicode-escape').decode('ascii')[:120]
                    print(f"  * Block {b['block_id']}: {escaped_snippet}...")
        except Exception as e:
            print("Pipeline test failed:", e)
        finally:
            # Cleanup temp files
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            # Cleanup test run directory
            import shutil
            shutil.rmtree(os.path.join(test_processed_dir, test_run_id), ignore_errors=True)
    else:
        print("Raw test PDF not found, skip test execution.")
