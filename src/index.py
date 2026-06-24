"""Embed chunks and build a FAISS index."""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def build_index(chunks: list[dict]) -> tuple[faiss.IndexFlatL2, list[dict]]:
    """Embed chunk texts and return a FAISS index + the original chunk list."""
    model = _get_model()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype(np.float32)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print(f"[index] Built FAISS index with {index.ntotal} vectors (dim={dim})")
    return index, chunks


def search(query: str, index: faiss.IndexFlatL2, chunks: list[dict], top_k: int = 5) -> list[dict]:
    """Return top_k chunks most relevant to the query."""
    model = _get_model()
    q_vec = model.encode([query], convert_to_numpy=True).astype(np.float32)
    _, indices = index.search(q_vec, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]
