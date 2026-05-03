# ThreatRAG-Eval
### A Retrieval-Augmented Generation Pipeline with Evaluation Harness for Cyber Threat Intelligence

> *"Not just a RAG pipeline — a measured one."*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Claude API](https://img.shields.io/badge/LLM-Claude%20(Anthropic)-blueviolet)](https://www.anthropic.com/)
[![FAISS](https://img.shields.io/badge/vector--store-FAISS-orange)](https://github.com/facebookresearch/faiss)
[![ragas](https://img.shields.io/badge/eval-ragas-green)](https://docs.ragas.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What This Is

ThreatRAG-Eval ingests real-world cybersecurity data from **CISA's Known Exploited Vulnerabilities (KEV)** catalog and the **NIST National Vulnerability Database (NVD)**, builds a RAG pipeline on top of it using Claude as the generator, and then rigorously evaluates three different chunking strategies using the `ragas` framework.

The point isn't just to answer security questions — it's to **measure which approach answers them best**, and to show exactly how and why.

---

## Why This Exists

Most RAG tutorials stop at "it works." This project asks the harder question: *how well does it work, and does my chunking strategy matter?*

This was built as part of a portfolio project focused on AI for security and threat intelligence — a domain where retrieval accuracy isn't just a metric, it's the difference between a useful tool and a misleading one.

---

## Architecture

```
CISA KEV API  ─┐
               ├──► Data Ingestion ──► Clean JSON ──► Chunking Layer
NVD API       ─┘                                           │
                                              ┌────────────┼────────────┐
                                         Fixed-Size   Semantic    Sentence-Window
                                              │            │            │
                                              └────────────┼────────────┘
                                                           │
                                                    FAISS Index
                                                           │
                                                    Retrieval Layer
                                                           │
                                                  Claude (Generation)
                                                           │
                                                    ragas Evaluation
                                                           │
                                              ┌────────────┼────────────┐
                                         Faithfulness  Answer     Context
                                                       Relevancy  Precision
```

---

## Project Structure

```
threat-rag-eval/
├── src/
│   ├── ingest_cisa.py        # CISA KEV API ingestion
│   ├── ingest_nvd.py         # NVD CVE API ingestion
│   ├── chunkers.py           # Fixed, semantic, sentence-window chunking
│   ├── indexer.py            # FAISS index builder
│   ├── retriever.py          # Retrieval + Claude generation
│   ├── eval_harness.py       # ragas evaluation runner
│   └── utils.py              # Shared utilities
├── data/
│   ├── raw/                  # Raw API responses
│   └── processed/            # Cleaned, chunked data
├── evals/
│   ├── qa_pairs.json         # 20 hand-crafted ground truth Q&A pairs
│   └── results/              # Evaluation outputs per chunking strategy
├── dashboard/
│   └── app.py                # Streamlit results dashboard
├── logs/
├── .env                      # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## Chunking Strategies Compared

| Strategy | Description | Hypothesis |
|---|---|---|
| **Fixed-Size** | Splits text into equal token-count chunks with overlap | Simple baseline; may cut context mid-sentence |
| **Semantic** | Groups sentences by embedding similarity | Preserves conceptual units; better for dense CVE text |
| **Sentence-Window** | Retrieves target sentence + surrounding context | Balances precision with enough context for generation |

---

## Evaluation Metrics (via ragas)

- **Faithfulness** — Does the answer only use facts from retrieved context?
- **Answer Relevancy** — Is the answer actually relevant to the question?
- **Context Precision** — Are the retrieved chunks actually useful?
- **Context Recall** — Did retrieval surface the right information?

---

## Setup

### Prerequisites
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- A free [NVD API key](https://nvd.nist.gov/developers/request-an-api-key) (optional but recommended)

### Installation

```bash
git clone https://github.com/yourusername/threat-rag-eval.git
cd threat-rag-eval
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your keys:

```
ANTHROPIC_API_KEY=your_key_here
NVD_API_KEY=your_key_here   # optional
DATA_DIR=data
LOG_LEVEL=INFO
```

---

## Running the Pipeline

```bash
# Step 1: Ingest data
python src/ingest_cisa.py
python src/ingest_nvd.py

# Step 2: Build indexes (all three chunking strategies)
python src/indexer.py --strategy all

# Step 3: Run evaluation
python src/eval_harness.py

# Step 4: View results dashboard
streamlit run dashboard/app.py
```

---

## Results

*Results will be updated here after full evaluation run.*

| Strategy | Faithfulness | Answer Relevancy | Context Precision | Context Recall |
|---|---|---|---|---|
| Fixed-Size | — | — | — | — |
| Semantic | — | — | — | — |
| Sentence-Window | — | — | — | — |

---

## Data Sources

- **CISA KEV Catalog**: [cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) — authoritative list of vulnerabilities with confirmed exploitation in the wild
- **NIST NVD**: [nvd.nist.gov](https://nvd.nist.gov/) — comprehensive CVE database with CVSS scores, CWE classifications, and remediation guidance

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Claude (Anthropic) |
| Vector Store | FAISS |
| Embeddings | sentence-transformers |
| Evaluation | ragas |
| Dashboard | Streamlit |
| Data Sources | CISA KEV, NIST NVD |

---

## License

MIT — see [LICENSE](LICENSE)

---

## Author

Built by Maitreyee as part of a portfolio focused on applied AI for security and threat intelligence.
