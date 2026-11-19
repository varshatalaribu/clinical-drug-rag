"""Download one FDA label per drug from openFDA.

Usage: python 01_fetch_labels.py [--force]
"""
from __future__ import annotations

import json
import sys
import time

import requests

from config import DRUGS, LABELS_DIR, SECTIONS

API = "https://api.fda.gov/drug/label.json"


def is_single_ingredient(label: dict, drug: str) -> bool:
    """True if the label is for `drug` alone (not a combination product)."""
    ofda = label.get("openfda", {})
    subs = ofda.get("substance_name", [])
    if subs:
        return len(subs) == 1 and drug.upper() in subs[0].upper()
    # Fallback when substance_name is missing
    names = [n.upper() for n in ofda.get("generic_name", [])]
    return any(drug.upper() in n and not any(s in n for s in (" AND ", ",", "/", "-"))
               for n in names)


def score(label: dict, drug: str):
    """Ranking key: single ingredient > Rx > most sections > most recent."""
    single = is_single_ingredient(label, drug)
    is_rx = "HUMAN PRESCRIPTION DRUG" in label.get("openfda", {}).get("product_type", [])
    n_sections = sum(1 for field in SECTIONS if field in label)
    updated = label.get("effective_time", "0")
    return (single, is_rx, n_sections, updated)


def fetch_label(drug: str) -> dict | None:
    params = {"search": f'openfda.generic_name:"{drug}"', "limit": 100}
    r = requests.get(API, params=params, timeout=30)
    if r.status_code == 404:  # no match
        return None
    r.raise_for_status()
    results = r.json()["results"]
    best = max(results, key=lambda lab: score(lab, drug))
    return best if score(best, drug)[0] else None


def main():
    force = "--force" in sys.argv
    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    for drug in DRUGS:
        out = LABELS_DIR / f"{drug}.json"
        if out.exists() and not force:
            print(f"  [skip] {drug} (already downloaded)")
            ok += 1
            continue
        try:
            label = fetch_label(drug)
        except requests.RequestException as e:
            print(f"  [error] {drug}: {e}")
            continue
        if label is None:
            print(f"  [miss] {drug}: no single-ingredient label found")
            continue
        out.write_text(json.dumps(label, indent=2))
        generic = label.get("openfda", {}).get("generic_name", ["?"])[0]
        print(f"  [ok] {drug:<20} label: {generic:<28} sections: {score(label, drug)[2]}")
        ok += 1
        time.sleep(0.3)  # stay under the API rate limit
    print(f"\nDownloaded {ok}/{len(DRUGS)} labels into {LABELS_DIR}")


if __name__ == "__main__":
    main()
