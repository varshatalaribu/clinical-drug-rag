"""Split labels into section-based chunks, embed them, and store them in ChromaDB.

Usage: python 02_build_index.py
"""
from __future__ import annotations

import json
import re

from config import (CHUNK_OVERLAP, CHUNK_WORDS, COMMON_BRANDS, LABELS_DIR,
                    SECTIONS)
from retriever import ALIAS_FILE, embed, get_collection


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", text)


def chunk_text(text: str, max_words=CHUNK_WORDS, overlap=CHUNK_OVERLAP) -> list[str]:
    """Pack whole sentences into chunks of <= max_words with word overlap."""
    chunks, current = [], []
    for sent in split_sentences(text):
        words = sent.split()
        # Hard-split overly long sentences
        while len(words) > max_words:
            chunks.append(" ".join(words[:max_words]))
            words = words[max_words - overlap:]
        if current and len(current) + len(words) > max_words:
            chunks.append(" ".join(current))
            current = current[-overlap:]
        current += words
    if current:
        chunks.append(" ".join(current))
    return chunks


def label_to_chunks(drug: str, label: dict) -> list[dict]:
    out = []
    for field, section in SECTIONS.items():
        if field not in label:
            continue
        text = clean(" ".join(label[field]))
        if len(text.split()) < 5:
            continue
        for i, piece in enumerate(chunk_text(text)):
            out.append({
                "id": f"{drug}::{field}::{i}",
                "text": f"[Drug: {drug} | Section: {section}] {piece}",
                "meta": {"drug": drug, "section": section, "field": field, "chunk": i,
                         "set_id": label.get("set_id", ""),
                         "label_date": label.get("effective_time", "")},
            })
    return out


def main():
    files = sorted(LABELS_DIR.glob("*.json"))
    if not files:
        raise SystemExit("No labels found — run 01_fetch_labels.py first.")

    all_chunks, aliases = [], {}
    for f in files:
        drug = f.stem
        label = json.loads(f.read_text())
        chunks = label_to_chunks(drug, label)
        all_chunks += chunks
        aliases[drug] = drug
        for brand in label.get("openfda", {}).get("brand_name", []):
            aliases[brand.lower()] = drug
        print(f"  {drug:<20} {len(chunks):>3} chunks")
    for brand, generic in COMMON_BRANDS.items():
        if generic in aliases:
            aliases[brand] = generic

    print(f"\nEmbedding {len(all_chunks)} chunks...")
    col = get_collection(reset=True)
    B = 128  # batch size
    for s in range(0, len(all_chunks), B):
        batch = all_chunks[s:s + B]
        texts = [c["text"] for c in batch]
        col.add(ids=[c["id"] for c in batch], documents=texts,
                embeddings=embed(texts), metadatas=[c["meta"] for c in batch])
        print(f"  stored {min(s + B, len(all_chunks))}/{len(all_chunks)}")

    ALIAS_FILE.write_text(json.dumps(aliases, indent=2, sort_keys=True))
    print(f"\nDone. {col.count()} chunks from {len(files)} drugs are in ChromaDB.")


if __name__ == "__main__":
    main()
