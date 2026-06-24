"""Run ragas evaluation over the ground truth Q&A pairs."""

import os
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings

import anthropic
import faiss
from src.retrieve import generate_answer


def _make_ragas_llm() -> LangchainLLMWrapper:
    chat = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
    )
    return LangchainLLMWrapper(chat)


def _make_ragas_embeddings() -> LangchainEmbeddingsWrapper:
    hf = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return LangchainEmbeddingsWrapper(hf)


def run_evaluation(
    index: faiss.IndexFlatL2,
    chunks: list[dict],
    ground_truth_pairs: list[dict],
    client: anthropic.Anthropic,
) -> pd.DataFrame:
    ragas_llm = _make_ragas_llm()
    ragas_embeddings = _make_ragas_embeddings()

    # Patch each metric to use Claude + local embeddings instead of OpenAI
    for metric in [faithfulness, answer_relevancy, context_precision, context_recall]:
        metric.llm = ragas_llm
        if hasattr(metric, "embeddings"):
            metric.embeddings = ragas_embeddings

    results = []
    for pair in ground_truth_pairs:
        print(f"[eval] Querying: {pair['question'][:60]}...")
        result = generate_answer(pair["question"], index, chunks, client, top_k=8)
        results.append({
            "question": pair["question"],
            "answer": result["answer"],
            "contexts": result["contexts"],
            "ground_truth": pair["ground_truth"],
        })

    dataset = Dataset.from_list(results)

    print("[eval] Running ragas metrics...")
    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        embeddings=ragas_embeddings,
        raise_exceptions=False,
    )

    df = scores.to_pandas()
    print("\n=== Evaluation Results ===")
    cols = [c for c in ["question", "faithfulness", "answer_relevancy", "context_precision", "context_recall"] if c in df.columns]
    print(df[cols].to_string(index=False))
    return df
