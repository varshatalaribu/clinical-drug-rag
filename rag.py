"""Answer questions with retrieved FDA label chunks and Gemini.

Usage: python rag.py "question"   (or no argument for interactive mode)
Requires GEMINI_API_KEY.
"""
from __future__ import annotations

import os
import sys
import time

from config import GEMINI_FALLBACKS, GEMINI_MODEL, TOP_K
from retriever import brand_notes, retrieve

SYSTEM_PROMPT = """You are a clinical drug-information assistant.
Answer the question using ONLY the numbered FDA label excerpts provided.
Rules:
- Every factual sentence must end with a citation like [1] or [2][3].
- If the excerpts do not contain the answer, reply exactly:
  "The retrieved FDA label sections do not contain this information."
- Do not use outside knowledge, and do not guess doses or numbers.
- Be concise (at most ~150 words). Quote doses and numbers exactly as written."""


def build_prompt(question: str, hits: list[dict]) -> str:
    sources = "\n\n".join(
        f"[{i}] ({h['drug']} — {h['section']})\n{h['text']}" for i, h in enumerate(hits, 1)
    )
    notes = brand_notes(question)
    notes = f"\n\n{notes}" if notes else ""
    return f"FDA LABEL EXCERPTS:\n{sources}{notes}\n\nQUESTION: {question}\n\nANSWER:"


_client = None


def call_gemini(prompt: str, system: str = SYSTEM_PROMPT) -> str:
    global _client
    from google import genai
    from google.genai import errors as genai_errors
    from google.genai import types
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise SystemExit("Set the GEMINI_API_KEY environment variable.")
        _client = genai.Client(api_key=key)
    cfg = types.GenerateContentConfig(system_instruction=system, temperature=0)

    # Retry transient errors with exponential backoff, then try fallback models
    last_err = None
    for model in [GEMINI_MODEL, *GEMINI_FALLBACKS]:
        for attempt in range(3):
            try:
                resp = _client.models.generate_content(model=model, contents=prompt, config=cfg)
                return (resp.text or "").strip()
            except genai_errors.APIError as e:
                if e.code not in (429, 500, 503):
                    raise
                last_err = e
                wait = 2 ** attempt * 3
                print(f"  [{model}] busy ({e.code}); retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
        print(f"  [{model}] still unavailable, trying next model", file=sys.stderr)
    raise last_err


def answer(question: str, k: int = TOP_K, use_drug_filter: bool = True) -> dict:
    hits = retrieve(question, k=k, use_drug_filter=use_drug_filter)
    text = call_gemini(build_prompt(question, hits))
    return {"question": question, "answer": text, "sources": hits}


def show(result: dict):
    print("\n" + result["answer"] + "\n\nSources:")
    for i, h in enumerate(result["sources"], 1):
        print(f"  [{i}] {h['drug']} — {h['section']} (similarity {h['similarity']})")
    print("\n(Information from FDA labeling; not a substitute for professional medical advice.)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show(answer(" ".join(sys.argv[1:])))
    else:
        print("Ask about any of the loaded drugs (empty line to quit).")
        while q := input("\n> ").strip():
            show(answer(q))
