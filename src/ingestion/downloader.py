import hashlib
import json
import os
import sys

import requests
from pypdf import PdfReader

# Mapped direct download URLs for Tunisian Finance Laws (Arabic)
FINANCE_LAWS = {
    2020: {
        "url": "https://www.finances.gov.tn/sites/default/files/2020-02/Loi_finances_2020_ar.pdf",
        "date": "2019-12-23"
    },
    "2020_rect": {
        "url": "https://www.finances.gov.tn/sites/default/files/2021-02/Loi2020_45Arrabe.pdf",
        "date": "2020-12-14",
        "title": "قانون المالية التعديلي لسنة 2020"
    },
    2021: {
        "url": "https://www.finances.gov.tn/sites/default/files/2021-02/1%20%282%29.pdf",
        "date": "2020-12-23"
    },
    "2021_rect": {
        "url": "https://www.finances.gov.tn/sites/default/files/2021-11/D%C3%A9cret-loi2021_3_0.pdf",
        "date": "2021-11-15",
        "title": "قانون المالية التعديلي لسنة 2021"
    },
    2022: {
        "url": "https://www.finances.gov.tn/sites/default/files/2022-02/Loi_des_Finances%202022_0.pdf",
        "date": "2021-12-28"
    },
    2023: {
        "url": "https://www.finances.gov.tn/sites/default/files/2022-12/LF.pdf",
        "date": "2022-12-22"
    },
    "2023_rect": {
        "url": "https://www.finances.gov.tn/sites/default/files/2023-10/LFR.pdf",
        "date": "2023-11-23",
        "title": "قانون المالية التعديلي لسنة 2023"
    },
    2024: {
        "url": "https://www.finances.gov.tn/sites/default/files/2023-12/LF2024_0.pdf",
        "date": "2023-12-11"
    },
    2025: {
        "url": "https://www.finances.gov.tn/sites/default/files/2024-12/LF2025.pdf",
        "date": "2024-12-09"
    },
    2026: {
        "url": "https://www.finances.gov.tn/sites/default/files/2026-01/115725.pdf",
        "date": "2025-12-12"
    }
}

def get_sha256(filepath: str) -> str:
    """Calculate the sha256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_page_count(filepath: str) -> int:
    """Retrieve PDF page count using pypdf."""
    try:
        reader = PdfReader(filepath)
        return len(reader.pages)
    except Exception as e:
        print(f"Warning: Could not extract page count for {filepath}: {e}")
        return 0

def download_file(url: str, target_path: str) -> None:
    """Download a file with streaming and basic progress feedback."""
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    headers = {"User-Agent": ua}
    print(f"Downloading {url} ...")
    response = requests.get(url, headers=headers, verify=False, stream=True)
    response.raise_for_status()
    
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Saved to {target_path}")

def run_downloader() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    for year, info in FINANCE_LAWS.items():
        year_dir = os.path.join(raw_dir, f"finance_law_{year}")
        os.makedirs(year_dir, exist_ok=True)
        
        pdf_path = os.path.join(year_dir, "original.pdf")
        manifest_path = os.path.join(year_dir, "manifest.json")
        
        print(f"\n--- Processing Finance Law for Year {year} ---")
        try:
            # 1. Download file only if it doesn't exist
            # This makes the script idempotent and fast on repeat runs
            if not os.path.exists(pdf_path):
                download_file(info["url"], pdf_path)
            else:
                print(f"PDF already exists at {pdf_path}, skipping download.")
            
            # 2. Get file details
            sha256_val = get_sha256(pdf_path)
            page_count = get_page_count(pdf_path)
            
            # 3. Create manifest
            manifest = {
                "source_id": f"src-finance-law-{year}-ar",
                "code_id": f"finance_law_{year}",
                "source_date": info["date"],
                "language": "ar",
                "format": "scanned_pdf",
                "page_count": page_count,
                "sha256": sha256_val,
                "official_reference": {
                    "publisher": "Ministère des Finances, Tunisie / JORT",
                    "title": info.get("title", f"قانون المالية لسنة {year}"),
                    "url": info["url"]
                },
                "reuse_status": "official_public_law",
                "ingestion_notes": (
                    "Official Arabic version downloaded "
                    "from Ministry of Finances portal."
                )
            }
            
            with open(manifest_path, "w", encoding="utf-8") as mf:
                json.dump(manifest, mf, ensure_ascii=False, indent=2)
            print(f"Created manifest with page count={page_count} at: {manifest_path}")
            
        except Exception as e:
            print(f"Error processing year {year}: {e}", file=sys.stderr)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run_downloader()
