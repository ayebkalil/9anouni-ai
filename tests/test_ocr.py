import json
import os
import shutil
import sys
import uuid

import fitz
import pytest

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.ocr.evaluator import calculate_cer, evaluate_run_quality  # noqa: E402
from src.ingestion.ocr.extractor import run_ocr_pipeline  # noqa: E402
from src.ingestion.ocr.renderer import render_pdf_to_images  # noqa: E402
from src.ingestion.ocr.segmenter import segment_page_columns  # noqa: E402


@pytest.fixture
def test_dirs():
    """Fixture to provide temporary paths and cleanup after execution."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_run_id = f"test-pytest-run-{uuid.uuid4().hex[:8]}"
    processed_dir = os.path.join(base_dir, "data", "processed")
    raw_pdf_path = os.path.join(base_dir, "data", "raw", "finance_law_2020_rect", "original.pdf")
    
    # Create a 1-page temporary PDF for tests
    temp_pdf_path = os.path.join(processed_dir, f"temp_{test_run_id}.pdf")
    os.makedirs(processed_dir, exist_ok=True)
    
    if os.path.exists(raw_pdf_path):
        src = fitz.open(raw_pdf_path)
        dest = fitz.open()
        dest.insert_pdf(src, from_page=0, to_page=0)
        dest.save(temp_pdf_path)
        dest.close()
        src.close()
    
    yield {
        "pdf_path": temp_pdf_path,
        "run_id": test_run_id,
        "processed_dir": processed_dir,
        "raw_pdf_exists": os.path.exists(raw_pdf_path)
    }
    
    # Cleanup
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)
    run_dir = os.path.join(processed_dir, test_run_id)
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)

def test_renderer(test_dirs):
    """Verifies that PDF pages are rendered successfully into PNGs."""
    if not test_dirs["raw_pdf_exists"]:
        pytest.skip("Raw test PDF not available")
        
    image_paths = render_pdf_to_images(
        test_dirs["pdf_path"],
        test_dirs["run_id"],
        test_dirs["processed_dir"]
    )
    
    assert len(image_paths) == 1
    assert os.path.exists(image_paths[0])
    assert image_paths[0].endswith(".png")

def test_segmenter(test_dirs):
    """Verifies page column layout segmenting and reading sequence logic."""
    if not test_dirs["raw_pdf_exists"]:
        pytest.skip("Raw test PDF not available")
        
    image_paths = render_pdf_to_images(
        test_dirs["pdf_path"],
        test_dirs["run_id"],
        test_dirs["processed_dir"]
    )
    
    # Test Arabic segmenting (RTL -> Right Column first)
    cols_ar = segment_page_columns(
        test_dirs["pdf_path"],
        0,
        image_paths[0],
        test_dirs["run_id"],
        test_dirs["processed_dir"],
        language="ar"
    )
    
    assert len(cols_ar) == 2
    assert cols_ar[0]["column_id"] == "right"
    assert cols_ar[1]["column_id"] == "left"
    assert os.path.exists(cols_ar[0]["image_path"])
    
    # Test French segmenting (LTR -> Left Column first)
    cols_fr = segment_page_columns(
        test_dirs["pdf_path"],
        0,
        image_paths[0],
        test_dirs["run_id"],
        test_dirs["processed_dir"],
        language="fr"
    )
    
    assert len(cols_fr) == 2
    assert cols_fr[0]["column_id"] == "left"
    assert cols_fr[1]["column_id"] == "right"

def test_cer_calculator():
    """Verifies Character Error Rate (CER) Lev distance calculations."""
    ref = "الفصل الأول تونس دولة حرة"
    hyp_perfect = "الفصل الأول تونس دولة حرة"
    hyp_spaces = "  الفصل   الأول   تونس  دولة حرة  "
    hyp_err = "الفصل الأول تونس دولة مستقلة"  # Replacing حرة (3 chars) with مستقلة (5 chars)
    
    assert calculate_cer(ref, hyp_perfect) == 0.0
    assert calculate_cer(ref, hyp_spaces) == 0.0
    assert calculate_cer(ref, hyp_err) > 0.0

def test_full_pipeline_and_evaluation(test_dirs):
    """Verifies full renderer -> segmenter -> extractor -> evaluator flow."""
    if not test_dirs["raw_pdf_exists"]:
        pytest.skip("Raw test PDF not available")
        
    # Run full OCR pipeline
    jsonl_path = run_ocr_pipeline(
        test_dirs["pdf_path"],
        test_dirs["run_id"],
        test_dirs["processed_dir"],
        language="ar",
        source_id="test-source"
    )
    
    assert os.path.exists(jsonl_path)
    assert jsonl_path.endswith("ocr_text.jsonl")
    
    # Read the extracted line to assert structure
    with open(jsonl_path, "r", encoding="utf-8") as f:
        line = json.loads(f.readline())
        assert line["run_id"] == test_dirs["run_id"]
        assert line["source_id"] == "test-source"
        assert len(line["blocks"]) == 2
        
        # Capture block IDs for CER evaluation test
        right_block_id = line["blocks"][0]["block_id"]
        right_text = line["blocks"][0]["text"]
        
    # Run CER evaluation
    gold_refs = {
        right_block_id: right_text  # Perfect match reference
    }
    
    report_path = evaluate_run_quality(
        jsonl_path,
        gold_refs,
        test_dirs["run_id"],
        test_dirs["processed_dir"]
    )
    
    assert os.path.exists(report_path)
    assert report_path.endswith("validation_report.json")
    
    with open(report_path, "r", encoding="utf-8") as rf:
        report = json.load(rf)
        assert report["run_id"] == test_dirs["run_id"]
        assert report["validation_status"] == "accepted"
        assert report["average_cer"] == 0.0
        assert report["blocks_evaluated_count"] == 1

def test_renderer_errors():
    with pytest.raises(FileNotFoundError):
        render_pdf_to_images("nonexistent.pdf", "run", "dir")

def test_segmenter_errors(test_dirs):
    with pytest.raises(FileNotFoundError):
        segment_page_columns(
            test_dirs["pdf_path"],
            0,
            "nonexistent_image.png",
            test_dirs["run_id"],
            test_dirs["processed_dir"]
        )

def test_extractor_errors():
    from src.ingestion.ocr.extractor import run_ocr_on_column
    with pytest.raises(FileNotFoundError):
        run_ocr_on_column("nonexistent_column.png")

def test_evaluator_errors():
    with pytest.raises(FileNotFoundError):
        evaluate_run_quality("nonexistent_ocr.jsonl", {}, "run", "dir")

def test_cer_empty_inputs():
    assert calculate_cer("", "") == 0.0
    assert calculate_cer("", "hypothesis") == 1.0
    assert calculate_cer("reference", "") == 1.0

