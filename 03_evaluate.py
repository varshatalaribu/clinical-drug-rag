"""Evaluate retrieval (Hit@k, MRR) and answers (keywords, citations,
faithfulness via LLM judge, refusals) on eval/questions.json.

Usage: python 03_evaluate.py [--retrieval-only]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time

from config import EVAL_FILE, RESULTS_DIR
from rag import build_prompt, call_gemini
from retriever import brand_notes, retrieve

REFUSAL = "do not contain this information"
K_VALUES = (1, 3, 5)

JUDGE_PROMPT = """You are grading a drug-information answer for faithfulness.
Using ONLY the SOURCE TEXT, decide whether every factual claim in the ANSWER is
supported by it. Ignore citation formatting. Reply with JSON only:
{"faithful": true or false, "unsupported_claims": ["..."]}"""


def is_relevant(hit: dict, q: dict) -> bool:
    return hit["drug"] in q["drugs"] and hit["section"] in q["sections"]


def first_correct_rank(hits: list[dict], q: dict) -> int | None:
    for rank, h in enumerate(hits, 1):
        if is_relevant(h, q):
            return rank
    return None


def keywords_found(answer: str, keywords: list[str]) -> bool:
    # "a|b" accepts either alternative
    a = answer.lower()
    return all(any(alt.lower() in a for alt in kw.split("|")) for kw in keywords)


def judge(question: str, answer: str, hits: list[dict]) -> tuple[bool | None, list]:
    source = "\n\n".join(h["text"] for h in hits) + "\n\n" + brand_notes(question)
    raw = call_gemini(f"SOURCE TEXT:\n{source}\n\nANSWER:\n{answer}", system=JUDGE_PROMPT)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        data = json.loads(m.group(0))
        return bool(data.get("faithful")), data.get("unsupported_claims", [])
    except Exception:
        return None, [f"judge output unparseable: {raw[:200]}"]


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retrieval-only", action="store_true")
    ap.add_argument("--delay", type=float, default=4.0,
                    help="seconds between Gemini calls (free tier is rate-limited)")
    args = ap.parse_args()

    questions = json.loads(EVAL_FILE.read_text())
    answerable = [q for q in questions if not q.get("unanswerable")]
    RESULTS_DIR.mkdir(exist_ok=True)
    report = ["# Evaluation report\n", f"{len(questions)} questions "
              f"({len(answerable)} answerable, {len(questions) - len(answerable)} unanswerable)\n"]

    # Retrieval
    rows = {}
    report.append("## Retrieval\n\n| Setting | " + " | ".join(f"Hit@{k}" for k in K_VALUES) + " | MRR |\n"
                  "|---|" + "---|" * (len(K_VALUES) + 1))
    # Ablation: each setting adds one technique
    settings = [
        ("Vector search only", dict(use_drug_filter=False, use_section_boost=False)),
        ("+ drug-name filter", dict(use_drug_filter=True, use_section_boost=False)),
        ("+ drug filter + section boost", dict(use_drug_filter=True, use_section_boost=True)),
    ]
    for name, opts in settings:
        ranks = []
        for q in answerable:
            hits = retrieve(q["question"], k=max(K_VALUES), **opts)
            r = first_correct_rank(hits, q)
            ranks.append(r)
            rows.setdefault(q["id"], {})[name] = (r, hits)
        hit = {k: sum(1 for r in ranks if r and r <= k) / len(ranks) for k in K_VALUES}
        mrr = sum(1 / r for r in ranks if r) / len(ranks)
        report.append(f"| {name} | " + " | ".join(pct(hit[k]) for k in K_VALUES) + f" | {mrr:.3f} |")
        print(f"{name:<32} " + "  ".join(f"Hit@{k}={pct(hit[k])}" for k in K_VALUES) + f"  MRR={mrr:.3f}")

    # Questions where the full system did not rank a correct chunk first
    final = settings[-1][0]
    report.append("\n### Questions not answered by the #1 chunk (full system)\n")
    for q in answerable:
        r, hits = rows[q["id"]][final]
        if r != 1:
            got = ", ".join(f"{h['drug']}/{h['section']}" for h in hits[:3])
            line = f"- #{q['id']} {q['question']} (correct rank: {r or 'not in top 5'}; top 3: {got})"
            report.append(line)
            print("  miss:", line[2:])

    # Answers
    if not args.retrieval_only:
        results = []
        for q in questions:
            hits = retrieve(q["question"])
            ans = call_gemini(build_prompt(q["question"], hits))
            time.sleep(args.delay)
            res = {"id": q["id"], "question": q["question"], "answer": ans,
                   "retrieved": [f"{h['drug']}/{h['section']}" for h in hits]}
            if q.get("unanswerable"):
                res["refused_correctly"] = REFUSAL in ans.lower()
            else:
                res["keywords_ok"] = keywords_found(ans, q["keywords"])
                refused = REFUSAL in ans.lower()
                res["refused"] = refused
                res["cited"] = None if refused else bool(re.search(r"\[\d+\]", ans))
                if refused:
                    res["faithful"], res["unsupported"] = True, []
                else:
                    res["faithful"], res["unsupported"] = judge(q["question"], ans, hits)
                    time.sleep(args.delay)
            results.append(res)
            print(f"  #{q['id']:>2} done")

        ans_rows = [r for r in results if "keywords_ok" in r]
        unans = [r for r in results if "refused_correctly" in r]
        judged = [r for r in ans_rows if r["faithful"] is not None]
        answered = [r for r in ans_rows if not r["refused"]]
        summary = {
            "Keyword accuracy (answer contains expected facts)": sum(r["keywords_ok"] for r in ans_rows) / len(ans_rows),
            "Wrongly refused (answerable but said 'not in label')": sum(r["refused"] for r in ans_rows) / len(ans_rows),
            "Citations (of non-refused answers)": sum(r["cited"] for r in answered) / max(len(answered), 1),
            "Faithfulness (LLM judge: all claims supported by source)": sum(r["faithful"] for r in judged) / max(len(judged), 1),
            "Refusal accuracy on unanswerable questions": sum(r["refused_correctly"] for r in unans) / max(len(unans), 1),
        }
        report.append("\n## Answers\n\n| Metric | Score |\n|---|---|")
        for k, v in summary.items():
            report.append(f"| {k} | {pct(v)} |")
            print(f"{k:<60} {pct(v)}")

        report.append("\n## Per-question details\n")
        for r in results:
            flag = ("refused OK" if r.get("refused_correctly") else "did NOT refuse") if "refused_correctly" in r \
                else f"keywords={'OK' if r['keywords_ok'] else 'MISS'} faithful={r['faithful']}"
            report.append(f"**#{r['id']} {r['question']}** — {flag}\n\n> {r['answer']}\n")
            if r.get("unsupported"):
                report.append(f"Unsupported claims: {r['unsupported']}\n")

        with open(RESULTS_DIR / "answers.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "question", "answer", "keywords_ok", "refused", "cited",
                                              "faithful", "refused_correctly", "retrieved", "unsupported"])
            w.writeheader()
            for r in results:
                w.writerow({**r, "retrieved": "; ".join(r["retrieved"])})

    (RESULTS_DIR / "eval_report.md").write_text("\n".join(report) + "\n")
    print(f"\nReport written to {RESULTS_DIR / 'eval_report.md'}")


if __name__ == "__main__":
    main()
