"""Fetch CISA KEV catalog and save to data/raw/cisa_kev.json."""

import json
import requests
from pathlib import Path

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def fetch_cisa_kev() -> list[dict]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(CISA_KEV_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    vulnerabilities = data["vulnerabilities"]

    out_path = RAW_DIR / "cisa_kev.json"
    with open(out_path, "w") as f:
        json.dump(vulnerabilities, f, indent=2)

    print(f"[ingest] Saved {len(vulnerabilities)} vulnerabilities to {out_path}")
    return vulnerabilities


if __name__ == "__main__":
    fetch_cisa_kev()
