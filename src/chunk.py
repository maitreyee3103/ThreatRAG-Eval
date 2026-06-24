"""Fixed-size chunking of vulnerability records."""

from typing import Any


CHUNK_SIZE = 600   # characters per chunk — large enough to fit most CVE records whole
CHUNK_OVERLAP = 100 # overlap to preserve context across boundaries


def record_to_text(vuln: dict[str, Any]) -> str:
    """Flatten a CISA KEV vulnerability dict into a single text block."""
    return (
        f"CVE ID: {vuln.get('cveID', 'N/A')}\n"
        f"Vendor/Project: {vuln.get('vendorProject', 'N/A')}\n"
        f"Product: {vuln.get('product', 'N/A')}\n"
        f"Vulnerability Name: {vuln.get('vulnerabilityName', 'N/A')}\n"
        f"Date Added: {vuln.get('dateAdded', 'N/A')}\n"
        f"Short Description: {vuln.get('shortDescription', 'N/A')}\n"
        f"Required Action: {vuln.get('requiredAction', 'N/A')}\n"
        f"Due Date: {vuln.get('dueDate', 'N/A')}\n"
    )


def fixed_size_chunk(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def chunk_vulnerabilities(vulnerabilities: list[dict]) -> list[dict]:
    """Return a list of chunk dicts with text and source metadata."""
    all_chunks = []
    for vuln in vulnerabilities:
        text = record_to_text(vuln)
        chunks = fixed_size_chunk(text)
        for i, chunk_text in enumerate(chunks):
            all_chunks.append({
                "text": chunk_text,
                "cve_id": vuln.get("cveID", "unknown"),
                "chunk_index": i,
            })
    print(f"[chunk] Produced {len(all_chunks)} chunks from {len(vulnerabilities)} records")
    return all_chunks


if __name__ == "__main__":
    import json
    from pathlib import Path
    raw = Path(__file__).parent.parent / "data" / "raw" / "cisa_kev.json"
    vulns = json.loads(raw.read_text())
    chunks = chunk_vulnerabilities(vulns)
    print(chunks[:2])
