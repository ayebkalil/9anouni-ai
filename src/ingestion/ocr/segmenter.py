"""
Module to perform coordinate-based layout segmentation on rendered 300 DPI page images.
Splits pages into left/right columns and excludes headers/footers to preserve reading order.
"""

import os
from typing import Any, Dict, List

import fitz  # PyMuPDF
from PIL import Image

# Default margins in PDF points (72 points per inch)
DEFAULT_MARGIN_LEFT = 35.0
DEFAULT_MARGIN_RIGHT = 35.0
DEFAULT_MARGIN_TOP = 65.0
DEFAULT_MARGIN_BOTTOM = 65.0
DEFAULT_COLUMN_GAP = 10.0  # Gap between columns

def segment_page_columns(
    pdf_path: str,
    page_num: int,  # 0-indexed page number
    rendered_image_path: str,
    run_id: str,
    base_processed_dir: str,
    language: str = "ar",
    margin_left: float = DEFAULT_MARGIN_LEFT,
    margin_right: float = DEFAULT_MARGIN_RIGHT,
    margin_top: float = DEFAULT_MARGIN_TOP,
    margin_bottom: float = DEFAULT_MARGIN_BOTTOM,
    column_gap: float = DEFAULT_COLUMN_GAP,
    columns_count: int = 2
) -> List[Dict[str, Any]]:
    """
    Splits a 300 DPI page image into left and right columns, or a single column,
    excluding headers and footers, and returns them in the correct reading order.

    Args:
        pdf_path: Path to the input PDF file (to read page dimensions).
        page_num: 0-indexed page number to inspect dimensions.
        rendered_image_path: Path to the rendered 300 DPI image file.
        run_id: Unique processing run ID.
        base_processed_dir: Base directory for processed outputs.
        language: Language of the document ("ar" or "fr").
        margin_left: Left margin threshold in points.
        margin_right: Right margin threshold in points.
        margin_top: Top margin threshold in points (excludes headers).
        margin_bottom: Bottom margin threshold in points (excludes footers).
        column_gap: Gap between columns to ignore separator lines in points.
        columns_count: Number of columns to segment (1 or 2).

    Returns:
        A list of dicts describing the segmented columns, ordered by reading sequence:
        [
            {
                "column_id": "right" or "left" or "full",
                "image_path": "/absolute/path/to/cropped_column.png",
                "bbox_points": (x0, y0, x1, y1),  # Bounding box in PDF points
                "bbox_pixels": (px0, py0, px1, py1)  # Bounding box in pixels
            },
            ...
        ]
    """
    if not os.path.exists(rendered_image_path):
        raise FileNotFoundError(f"Rendered page image not found at: {rendered_image_path}")

    # Set up output directory: data/processed/{run_id}/columns/
    output_dir = os.path.join(base_processed_dir, run_id, "columns")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Read page dimensions using PyMuPDF
    doc = fitz.open(pdf_path)
    try:
        page = doc.load_page(page_num)
        width_pts = page.rect.width
        height_pts = page.rect.height
    finally:
        doc.close()

    # Calculate scale factor between points (72 DPI) and pixels (300 DPI)
    scale = 300.0 / 72.0

    # Helper function to convert points bbox to pixel bbox
    def to_pixels(bbox_pts: tuple) -> tuple:
        return (
            int(bbox_pts[0] * scale),
            int(bbox_pts[1] * scale),
            int(bbox_pts[2] * scale),
            int(bbox_pts[3] * scale)
        )

    # 2. Define the column boundaries in PDF points
    img = Image.open(rendered_image_path)

    if columns_count == 1:
        box_pts = (
            margin_left,
            margin_top,
            width_pts - margin_right,
            height_pts - margin_bottom
        )
        box_pixels = to_pixels(box_pts)
        crop_path = os.path.join(output_dir, f"page_{page_num + 1:04d}_full.png")
        cropped_img = img.crop(box_pixels)
        cropped_img.save(crop_path)

        return [
            {
                "column_id": "full",
                "image_path": os.path.abspath(crop_path),
                "bbox_points": box_pts,
                "bbox_pixels": box_pixels
            }
        ]

    # Two-column layout
    mid_x = width_pts / 2.0
    half_gap = column_gap / 2.0

    left_box_pts = (
        margin_left,
        margin_top,
        mid_x - half_gap,
        height_pts - margin_bottom
    )

    right_box_pts = (
        mid_x + half_gap,
        margin_top,
        width_pts - margin_right,
        height_pts - margin_bottom
    )

    left_box_pixels = to_pixels(left_box_pts)
    right_box_pixels = to_pixels(right_box_pts)

    left_crop_path = os.path.join(output_dir, f"page_{page_num + 1:04d}_left.png")
    right_crop_path = os.path.join(output_dir, f"page_{page_num + 1:04d}_right.png")

    # Crop left column
    left_img = img.crop(left_box_pixels)
    left_img.save(left_crop_path)

    # Crop right column
    right_img = img.crop(right_box_pixels)
    right_img.save(right_crop_path)

    # Determine reading order
    columns = [
        {
            "column_id": "left",
            "image_path": os.path.abspath(left_crop_path),
            "bbox_points": left_box_pts,
            "bbox_pixels": left_box_pixels
        },
        {
            "column_id": "right",
            "image_path": os.path.abspath(right_crop_path),
            "bbox_points": right_box_pts,
            "bbox_pixels": right_box_pixels
        }
    ]

    # For Arabic ("ar"), right column is read first. For French ("fr"), left column is first.
    if language == "ar":
        # Right column first, then left column
        ordered_columns = [columns[1], columns[0]]
    else:
        # Left column first, then right column
        ordered_columns = [columns[0], columns[1]]

    return ordered_columns

if __name__ == "__main__":
    # Smoke test for segmentation
    import sys
    import uuid
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    sys.path.insert(0, project_root)
    from src.ingestion.ocr.renderer import render_pdf_to_images
    test_pdf = os.path.join(project_root, "data", "raw", "finance_law_2020_rect", "original.pdf")
    test_processed = os.path.join(project_root, "data", "processed")
    test_run_id = f"test-run-{uuid.uuid4().hex[:8]}"

    if os.path.exists(test_pdf):
        print("Rendering test page...")
        images = render_pdf_to_images(test_pdf, test_run_id, test_processed)
        if images:
            print("Segmenting test columns (Arabic)...")
            try:
                cols = segment_page_columns(
                    test_pdf, 0, images[0], test_run_id, test_processed, language="ar"
                )
                print(f"Successfully segmented page 1 into {len(cols)} columns.")
                print(f"First column in reading order: {cols[0]['column_id']}")
                print(f"Path: {cols[0]['image_path']}")
            except Exception as e:
                print("Segmentation test failed:", e)
        # Cleanup test run
        import shutil
        shutil.rmtree(os.path.join(test_processed, test_run_id), ignore_errors=True)
    else:
        print("Raw test PDF not found, skip test execution.")
