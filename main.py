"""End-to-end ThreatRAG-Eval pipeline."""

import nest_asyncio
nest_asyncio.apply()

import os
from dotenv import load_dotenv
import anthropic

from src.ingest import fetch_cisa_kev
from src.chunk import chunk_vulnerabilities
from src.index import build_index
from src.retrieve import generate_answer
from src.evaluate import run_evaluation
from evals.ground_truth import GROUND_TRUTH

load_dotenv()


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your-key-here":
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    client = anthropic.Anthropic(api_key=api_key)

    # 1. Ingest
    print("\n--- Step 1: Ingest ---")
    vulnerabilities = fetch_cisa_kev()

    # 2. Chunk
    print("\n--- Step 2: Chunk ---")
    chunks = chunk_vulnerabilities(vulnerabilities)

    # 3. Index
    print("\n--- Step 3: Index ---")
    index, chunks = build_index(chunks)

    # 4. Spot-check: single query
    print("\n--- Step 4: Spot-check query ---")
    result = generate_answer(
        "What is Log4Shell and what action is required?",
        index,
        chunks,
        client,
        top_k=8,
    )
    print(f"Q: {result['query']}")
    print(f"A: {result['answer']}\n")

    # 5. Evaluate
    print("\n--- Step 5: Evaluate ---")
    run_evaluation(index, chunks, GROUND_TRUTH, client)

    print("\nDone.")


if __name__ == "__main__":
    main()
