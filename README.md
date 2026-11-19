# Clinical Drug Information RAG Assistant

Question answering over FDA drug labels. Relevant label sections are retrieved from a ChromaDB vector store and passed to Gemini, which answers only from the retrieved text and cites its sources.

## Data

- **Source:** [openFDA Drug Label API](https://open.fda.gov/apis/drug/label/) (official FDA Structured Product Labeling).
- **Coverage:** 34 commonly prescribed medications (listed in `config.py`). One label per drug, selected by: single-ingredient product, prescription over OTC, number of populated sections, most recent revision.
- **Sections indexed:** Boxed Warning, Indications and Usage, Dosage and Administration, Dosage Forms and Strengths, Contraindications, Warnings and Precautions, Adverse Reactions, Drug Interactions, Use in Specific Populations, Pregnancy, Lactation, Pediatric Use, Geriatric Use, Overdosage, Mechanism of Action, Clinical Pharmacology.
- **Evaluation set:** 36 hand-labeled questions (`eval/questions.json`): 33 answerable and 3 unanswerable. Each is annotated with the expected drug(s), label section(s), and key terms.

## Pipeline

1. **Ingestion** (`01_fetch_labels.py`): downloads and selects one label per drug.
2. **Indexing** (`02_build_index.py`): splits each label by section, then into ~180-word chunks with 40-word overlap at sentence boundaries. Each chunk is prefixed with its drug and section, embedded with `multi-qa-MiniLM-L6-cos-v1` (Sentence-Transformers), and stored in ChromaDB (cosine similarity) with drug and section metadata.
3. **Retrieval** (`retriever.py`):
   - Generic and brand drug names in the question set a metadata filter.
   - Keyword rules map the question to target sections. A section-restricted search adds candidates, which are reranked with a score boost.
   - The top 5 chunks are returned.
4. **Generation** (`rag.py`): Gemini (`gemini-3.5-flash`, with fallback models) at temperature 0. Answers must cite the numbered excerpts, and when the excerpts don't cover the question the model returns a fixed refusal. Brand-to-generic mappings are added to the prompt.
5. **Evaluation** (`03_evaluate.py`):
   - Retrieval: Hit@1/3/5 and MRR, as an ablation across retrieval settings.
   - Answers: keyword accuracy, citation rate, faithfulness (LLM-as-judge), and refusal accuracy.

## Results

Retrieval (33 answerable questions):

| Setting | Hit@1 | Hit@3 | Hit@5 | MRR |
|---|---|---|---|---|
| Vector search | 63.6% | 84.8% | 87.9% | 0.745 |
| + drug-name filter | 69.7% | 87.9% | 90.9% | 0.790 |
| + section routing | **90.9%** | **97.0%** | **100%** | **0.945** |

Answers (`gemini-3.5-flash-lite`):

| Metric | Score |
|---|---|
| Keyword accuracy | 97.0% |
| Citation rate | 97.0% |
| Faithfulness (LLM judge) | 100% |
| Refusal accuracy (unanswerable) | 100% |
| Answerable questions refused | 0% |

Full per-question output: `results/eval_report.md`, `results/answers.csv`.

## Project structure

```
config.py             settings: drugs, sections, chunking, models
01_fetch_labels.py    download FDA labels
02_build_index.py     chunk, embed, store in ChromaDB
retriever.py          embedding, query parsing, retrieval
rag.py                prompt construction and Gemini calls
03_evaluate.py        retrieval and answer evaluation
eval/questions.json   labeled evaluation set
results/              evaluation outputs
```

## Setup

Requires Python 3.10+ and a [Gemini API key](https://aistudio.google.com/apikey).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
```

## Usage

```bash
python 01_fetch_labels.py              # download labels (--force to refresh)
python 02_build_index.py               # build the vector index
python rag.py "What is the boxed warning for warfarin?"
python rag.py                          # interactive mode
python 03_evaluate.py --retrieval-only # retrieval metrics only
python 03_evaluate.py                  # full evaluation
```

Set `GEMINI_MODEL` to use a different model (for example, `export GEMINI_MODEL=gemini-3.5-flash-lite`).

## Disclaimer

For research and educational use only. Not medical advice.
