"""
Module to render raw PDF pages into high-resolution PNG images at 300 DPI.
Derived artifacts are stored under the processed run directory to keep the raw zone immutable.
"""

import os
from typing import List

import fitz  # PyMuPDF


def render_pdf_to_images(pdf_path: str, run_id: str, base_processed_dir: str) -> List[str]:
    """
    Renders every page of the given PDF at 300 DPI and saves them as PNG files.

    Args:
        pdf_path: Path to the input PDF file.
        run_id: Unique identifier for this processing run.
        base_processed_dir: Path to the base directory where processed outputs are stored.

    Returns:
        A list of paths to the rendered PNG images.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    # Set up output directory: data/processed/{run_id}/pages/
    output_dir = os.path.join(base_processed_dir, run_id, "pages")
    os.makedirs(output_dir, exist_ok=True)

    rendered_image_paths: List[str] = []

    # Open PDF using PyMuPDF
    doc = fitz.open(pdf_path)
    
    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Render page at 300 DPI
            pix = page.get_pixmap(dpi=300)
            
            # Format filename as page_0001.png, page_0002.png etc.
            image_filename = f"page_{page_num + 1:04d}.png"
            image_path = os.path.join(output_dir, image_filename)
            
            pix.save(image_path)
            rendered_image_paths.append(os.path.abspath(image_path))
            
    finally:
        doc.close()

    return rendered_image_paths

if __name__ == "__main__":
    # Quick smoke test for rendering
    import uuid
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    test_pdf = os.path.join(project_root, "data", "raw", "finance_law_2020_rect", "original.pdf")
    test_processed = os.path.join(project_root, "data", "processed")
    test_run_id = f"test-run-{uuid.uuid4().hex[:8]}"

    if os.path.exists(test_pdf):
        print(f"Starting test render of: {test_pdf}")
        try:
            paths = render_pdf_to_images(test_pdf, test_run_id, test_processed)
            print(f"Successfully rendered {len(paths)} pages.")
            print(f"Sample page path: {paths[0] if paths else 'None'}")
        except Exception as e:
            print("Render test failed:", e)
    else:
        print("Raw test PDF not found, skip test execution.")
