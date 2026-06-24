"""Retrieve relevant chunks and generate an answer via Claude."""

import anthropic
from src.index import search
import faiss

SYSTEM_PROMPT = (
    "You are a cybersecurity analyst assistant. "
    "Answer the user's question directly and concisely using only the context provided. "
    "Lead with the direct answer in 1-2 sentences. "
    "Do not add headers, bullet points, or information not present in the context. "
    "If the context does not contain the answer, say exactly: 'The context does not contain this information.'"
)


def generate_answer(
    query: str,
    index: faiss.IndexFlatL2,
    chunks: list[dict],
    client: anthropic.Anthropic,
    top_k: int = 5,
    model: str = "claude-haiku-4-5-20251001",
) -> dict:
    """Retrieve top_k chunks and call Claude to produce an answer."""
    retrieved = search(query, index, chunks, top_k=top_k)
    context = "\n\n---\n\n".join(c["text"] for c in retrieved)

    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            }
        ],
    )

    answer = message.content[0].text
    return {
        "query": query,
        "answer": answer,
        "contexts": [c["text"] for c in retrieved],
    }
