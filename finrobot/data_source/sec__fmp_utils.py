"""
filing_pipeline.py

Purpose: Query sec-api.io for filings; fall back to FMP; download documents (HTML/PDF/XBRL);
extract text; optionally parse XBRL via sec-api XBRL endpoint.

Configure SEC_API_KEY and FMP_API_KEY below or via env vars.
"""

import os
import time
import json
import logging
from typing import Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from pdfminer.high_level import extract_text as extract_pdf_text

# --- Config ---
FMP_API_KEY = os.getenv("FMP_API_KEY", "<YOUR_FMP_API_KEY>")

# Simple filesystem cache folder
CACHE_DIR = "./filing_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("filing_pipeline")

# --- Helpers ---
def save_file(path: str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)
    logger.info(f"Saved {path}")

def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# --- FMP fallback: get filings for a symbol ---
def fmp_get_filings(symbol: str, limit: int = 10) -> Optional[Dict[str, Any]]:
    """
    FMP filings endpoint example:
      https://financialmodelingprep.com/api/v3/sec_filings/AAPL?apikey=YOUR_KEY
    """
    url = f"https://financialmodelingprep.com/api/v3/sec_filings/{symbol}?limit={limit}&apikey={FMP_API_KEY}"
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return resp.json()
    else:
        logger.warning(f"FMP filings call failed: {resp.status_code} {resp.text}")
        return None

# --- Download a document (HTML or PDF) ---
def download_document(url: str, dest_path: str) -> bool:
    logger.info(f"Downloading {url} -> {dest_path}")
    headers = {"User-Agent": "filing-pipeline/1.0 (+https://your.domain)"}
    try:
        r = requests.get(url, headers=headers, timeout=60, stream=True)
        if r.status_code == 200:
            save_file(dest_path, r.content)
            return True
        else:
            logger.warning(f"Download failed {r.status_code} for {url}")
            return False
    except Exception:
        logger.exception(f"Exception while downloading {url}")
        return False

# --- Extract text from HTML filing ---
def extract_text_from_html_file(path: str) -> str:
    html = read_text_file(path)
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts/styles for cleaner text
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    # Optionally narrow scope to <document> sections in SEC filings:
    # Many filings have <DOCUMENT> or <TEXT> tags—adjust as needed.
    text = soup.get_text(separator="\n", strip=True)
    return text

# --- Extract text from PDF file (pdfminer) ---
def extract_text_from_pdf_file(path: str) -> str:
    try:
        text = extract_pdf_text(path)
        return text
    except Exception:
        logger.exception("PDF extraction failed")
        return ""

# --- High-level pipeline: fetch latest filings for ticker, download and extract text ---
def fetch_and_process_latest(ticker: str, form_type: str = "10-K", max_items: int = 3):
    # 1) Try sec-api
    query = f'ticker:{ticker} AND formType:"{form_type}"'
    logger.info(f"Searching sec-api for: {query}")
    # search_result = sec_api_search(query, size=max_items)
    filings = []

    # 2) fallback to FMP
    logger.info("Falling back to FMP filings")
    fmp_data = fmp_get_filings(ticker, limit=max_items)
    if fmp_data:
        # FMP returns a list
        filings = fmp_data if isinstance(fmp_data, list) else fmp_data.get("filings", [])
        logger.info(f"FMP returned {len(filings)} filings")
    else:
        logger.error("No filings found from sec-api or FMP")
        return

    for i, f in enumerate(filings):
        # Normalize possible response shapes
        # sec-api: filing has fields like 'linkToFilingDetails', 'filedAt', 'formType'
        # fmp: might have 'link' or 'url'
        link = f.get("linkToFilingDetails") or f.get("link") or f.get("url") or f.get("filingLink")
        filed_at = f.get("filedAt") or f.get("date") or f.get("acceptedDate")
        form = f.get("formType") or f.get("form") or f.get("type")

        try:
            filed_dt = dateparser.parse(filed_at).date().isoformat() if filed_at else "unknown-date"
        except Exception:
            filed_dt = "unknown-date"

        if not link:
            logger.warning(f"No document link for filing index {i}: {f}")
            continue

        # Some sec-api results give a details page which contains document links.
        # If it's a filing details page (html), fetch it and find the primary document link.
        filename_base = f"{ticker}_{form}_{filed_dt}_{i}"
        details_path = os.path.join(CACHE_DIR, filename_base + "_details.html")
        if download_document(link, details_path):
            html_text = extract_text_from_html_file(details_path)
            # Try to find direct document URL inside details page for robust download
            soup = BeautifulSoup(read_text_file(details_path), "html.parser")
            # SEC detail pages often contain <a href="...">Documents</a>; heuristics:
            doc_link = None
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.lower().endswith(".htm") or href.lower().endswith(".html") or href.lower().endswith(".pdf"):
                    # make absolute if needed
                    if href.startswith("http"):
                        doc_link = href
                    else:
                        # often relative to https://www.sec.gov
                        doc_link = requests.compat.urljoin(link, href)
                    # pick first plausible primary document
                    break

            if doc_link:
                ext = doc_link.split("?")[0].split(".")[-1].lower()
                doc_path = os.path.join(CACHE_DIR, f"{filename_base}_document.{ext}")
                if download_document(doc_link, doc_path):
                    # extract text depending on filetype
                    if ext in ("htm", "html", "txt"):
                        doc_text = extract_text_from_html_file(doc_path)
                    elif ext == "pdf":
                        doc_text = extract_text_from_pdf_file(doc_path)
                    else:
                        # fallback to reading raw bytes (and trying to decode)
                        try:
                            doc_text = open(doc_path, "rb").read().decode("utf-8", errors="ignore")
                        except Exception:
                            doc_text = ""
                    # Save or process doc_text: here we just write to a .txt for demonstration
                    out_txt = os.path.join(CACHE_DIR, f"{filename_base}_extracted.txt")
                    with open(out_txt, "w", encoding="utf-8") as fh:
                        fh.write(doc_text)
                    logger.info(f"Extracted text saved to {out_txt}")

                    # Optionally, if we detect XBRL link (instance .xml), call sec-api xbrl endpoint:
                    if ".xml" in doc_link.lower() and SEC_API_KEY:
                        xbrl_json = sec_api_xbrl_to_json(doc_link)
                        if xbrl_json:
                            xbrl_out = os.path.join(CACHE_DIR, f"{filename_base}_xbrl.json")
                            with open(xbrl_out, "w", encoding="utf-8") as fh:
                                json.dump(xbrl_json, fh, indent=2)
                            logger.info(f"Saved XBRL JSON to {xbrl_out}")

                else:
                    logger.warning(f"Could not download the primary doc link {doc_link}")
            else:
                # If no doc link found inside details page, try to treat details page as the document
                out_txt = os.path.join(CACHE_DIR, f"{filename_base}_details_extracted.txt")
                with open(out_txt, "w", encoding="utf-8") as fh:
                    fh.write(html_text)
                logger.info(f"No separate doc link found. Extracted details page text to {out_txt}")

        else:
            logger.warning(f"Could not download filing details page: {link}")

        # simple rate-limiting friendly pause
        time.sleep(0.5)

# --- CLI example usage ---
if __name__ == "__main__":
    # Example: fetch latest 2 10-Ks for TSLA
    fetch_and_process_latest("TSLA", form_type="10-K", max_items=2)
