"""Embedding, ChromaDB access, query parsing and retrieval."""
from __future__ import annotations

import json
import re
from functools import lru_cache

import chromadb

from config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL, SECTION_BOOST, TOP_K

ALIAS_FILE = CHROMA_DIR / "aliases.json"  # written by 02_build_index.py


# Embeddings
@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL)


def embed(texts: list[str]) -> list[list[float]]:
    vecs = get_model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [v.tolist() for v in vecs]


# Vector store
def get_collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )


# Drug and brand detection
@lru_cache(maxsize=1)
def _aliases() -> dict[str, str]:
    if ALIAS_FILE.exists():
        return json.loads(ALIAS_FILE.read_text())
    return {}


def detect_drugs(question: str) -> list[str]:
    """Generic names of drugs mentioned in the question (generic or brand)."""
    q = question.lower()
    found = {generic for name, generic in _aliases().items()
             if re.search(rf"\b{re.escape(name)}\b", q)}
    return sorted(found)


def brand_notes(question: str) -> str:
    """Prompt note mapping brand names in the question to generic names."""
    q = question.lower()
    notes = [f'"{name}" is a brand name for {generic}.'
             for name, generic in sorted(_aliases().items())
             if name != generic and generic not in name
             and re.search(rf"\b{re.escape(name)}\b", q)]
    return ("Note: " + " ".join(notes)) if notes else ""


# Section routing: keyword rules -> target sections
SECTION_INTENTS = [
    (r"boxed warning|black[- ]box", ["Boxed Warning"]),
    (r"side effect|adverse", ["Adverse Reactions"]),
    (r"\bdose\b|dosage|dosing|how often|maximum|starting", ["Dosage and Administration"]),
    (r"contraindicat|should not take|who should not|must not", ["Contraindications"]),
    (r"interact|together with|combined with", ["Drug Interactions", "Contraindications"]),
    (r"pregnan", ["Pregnancy", "Use in Specific Populations"]),
    (r"breast|lactat|nursing", ["Lactation", "Use in Specific Populations"]),
    (r"child|pediatric|kids", ["Pediatric Use", "Use in Specific Populations"]),
    (r"elderly|geriatric|older adult", ["Geriatric Use", "Use in Specific Populations"]),
    (r"overdos|too much", ["Overdosage"]),
    (r"how does .* work|mechanism", ["Mechanism of Action", "Clinical Pharmacology"]),
    (r"used for|indicat|approved for|\btreat", ["Indications and Usage"]),
]
# Applied only when no specific rule matches
GENERIC_INTENT = (r"warning|risk|precaution|danger", ["Warnings and Precautions", "Boxed Warning"])


def detect_sections(question: str) -> set[str]:
    q = question.lower()
    found = {s for pattern, secs in SECTION_INTENTS if re.search(pattern, q) for s in secs}
    if not found and re.search(GENERIC_INTENT[0], q):
        found = set(GENERIC_INTENT[1])
    return found


# Retrieval
def retrieve(question: str, k: int = TOP_K, use_drug_filter: bool = True,
             use_section_boost: bool = True) -> list[dict]:
    """Return the top-k chunks for a question.

    Optional drug filter; with section boost, also fetches chunks from the
    target sections and reranks with SECTION_BOOST.
    """
    col = get_collection()
    drug_where = None
    drugs = detect_drugs(question) if use_drug_filter else []
    if len(drugs) == 1:
        drug_where = {"drug": drugs[0]}
    elif len(drugs) > 1:
        drug_where = {"drug": {"$in": drugs}}

    q_vec = embed([question])
    n = k * 4 if use_section_boost else k
    results = [col.query(query_embeddings=q_vec, n_results=n, where=drug_where)]

    wanted = detect_sections(question) if use_section_boost else set()
    if wanted:
        sec_where = {"section": {"$in": sorted(wanted)}}
        where = {"$and": [drug_where, sec_where]} if drug_where else sec_where
        results.append(col.query(query_embeddings=q_vec, n_results=k, where=where))

    hits, seen = [], set()
    for res in results:
        for cid, doc, meta, dist in zip(res["ids"][0], res["documents"][0],
                                        res["metadatas"][0], res["distances"][0]):
            if cid in seen:
                continue
            seen.add(cid)
            hits.append({**meta, "text": doc, "similarity": round(1 - dist, 3)})

    if use_section_boost:
        for h in hits:
            h["score"] = h["similarity"] + (SECTION_BOOST if h["section"] in wanted else 0)
        hits.sort(key=lambda h: h["score"], reverse=True)
    else:
        hits.sort(key=lambda h: h["similarity"], reverse=True)
    return hits[:k]
