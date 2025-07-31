#!/usr/bin/env python3
"""
Grok Selenium Research Worker

Launches a headless Chrome (or visible browser if desired), visits one or more URLs,
collects basic metadata (page title, final URL, load time) and stores results as JSON.

Usage examples:

# Single URL, headless
python src/workers/grok_selenium_research_worker.py --url https://www.example.com --headless

# Multiple URLs, visible browser, custom output file
python src/workers/grok_selenium_research_worker.py \
    --url https://pushingcapital.com \
    --url https://www.python.org \
    --output research_output.json

Requirements:
    pip install selenium==4.*
    A Chrome/Chromium browser plus matching chromedriver binary in PATH

This worker is intentionally lightweight; extend it to capture screenshots,
extract specific DOM elements, run Lighthouse audits, etc.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def iso_now() -> str:
    """UTC timestamp in ISO-8601 format with Z suffix."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def init_driver(headless: bool = True) -> webdriver.Chrome:
    """Spin up a Chrome webdriver with sane defaults."""
    options = Options()
    if headless:
        # Chrome 115+ headless mode flag
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Reduce noise
    options.add_argument("--log-level=3")
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        raise SystemExit(
            "[ERROR] Could not start Chrome webdriver. "
            "Ensure chromedriver is installed and matches your Chrome version.\n" + str(exc)
        )
    driver.set_page_load_timeout(30)
    return driver


def crawl_url(driver: webdriver.Chrome, url: str) -> Dict:
    """Visit a URL and collect basic information."""
    start = time.time()
    driver.get(url)
    load_time = round(time.time() - start, 3)

    title = driver.title
    final_url = driver.current_url  # after redirects
    # You can add more extraction logic here.

    return {
        "input_url": url,
        "final_url": final_url,
        "title": title,
        "load_time_seconds": load_time,
        "timestamp": iso_now(),
    }

# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Grok Selenium Research Worker")
    parser.add_argument("--url", action="append", required=True, help="URL to visit (repeatable)")
    parser.add_argument("--output", default="selenium_research_results.json", help="Output JSON file path")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")

    args = parser.parse_args()

    urls: List[str] = args.url

    driver = init_driver(headless=args.headless)
    results: List[Dict] = []

    try:
        for u in urls:
            print(f"[INFO] Visiting {u} …")
            try:
                results.append(crawl_url(driver, u))
                print(f"    ✓ Completed {u}")
            except Exception as e:
                print(f"    ✗ Error on {u}: {e}")
                results.append({
                    "input_url": u,
                    "error": str(e),
                    "timestamp": iso_now(),
                })
    finally:
        driver.quit()

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print(f"[DONE] Saved {len(results)} record(s) → {args.output}")


if __name__ == "__main__":
    main()