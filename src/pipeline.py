
from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DOCUMENTS = [
    {"source": "policy.md", "text": "The system should answer with citations and avoid unsupported claims."},
    {"source": "runbook.md", "text": "Analysts need retrieval, summarization, extraction, and comparison workflows."},
    {"source": "security.md", "text": "Private documents should be routed through approved local or secure providers."},
]


def load_config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def run(config_path: str = "configs/default.yaml") -> None:
    cfg = load_config(config_path)
    query = cfg.get("query", "What should the assistant cite?")
    corpus = [doc["text"] for doc in DOCUMENTS]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    top_index = int(scores.argmax())
    doc = DOCUMENTS[top_index]
    report = Path("reports")
    report.mkdir(exist_ok=True)
    (report / "summary.md").write_text(
        f"# RAG Document Intelligence Portfolio System 34 Report\n\nQuery: {query}\n\nAnswer: {doc['text']}\n\nCitation: {doc['source']}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    run(parser.parse_args().config)
