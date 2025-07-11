#!/usr/bin/env python3
"""PDF → Weaviate ingestion with run statistics.

After processing it prints e.g.

✓ 3 PDFs processed
✓ 142 chunks (90 inserts, 52 updates)
Elapsed: 4.3 s
"""
from __future__ import annotations

import argparse
import glob
import os
import time
from typing import List

import weaviate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from weaviate.util import generate_uuid5

from config import COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP

# ---------- optional PDF back-ends --------------------------------------------------
try:
    from unstructured.partition.pdf import partition_pdf  # type: ignore
except ImportError:
    partition_pdf = None

try:
    from pypdf import PdfReader  # type: ignore
except ImportError:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except ImportError:
        PdfReader = None


splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# ---------- helpers ----------------------------------------------------------------


def extract_text(path: str) -> str:
    if partition_pdf is not None:
        els = partition_pdf(filename=path)
        return "\n".join([e.text for e in els if getattr(e, "text", None)])
    if PdfReader is not None:
        reader = PdfReader(path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    raise ImportError("Install 'unstructured[pdf]' or 'pypdf' to enable PDF parsing.")


def list_pdfs(directory: str) -> List[str]:
    return glob.glob(os.path.join(directory, "*.pdf"))


def connect() -> weaviate.WeaviateClient:
    return weaviate.connect_to_local()


def ensure_collection(client: weaviate.WeaviateClient):
    if not client.collections.exists(COLLECTION_NAME):
        client.collections.create(name=COLLECTION_NAME)
    return client.collections.get(COLLECTION_NAME)


# ---------- ingestion logic ---------------------------------------------------------


def process_pdf(path: str, docs, stats: dict[str, int]):
    text = extract_text(path)
    chunks = splitter.split_text(text)
    stats["chunks"] += len(chunks)
    for i, chunk in enumerate(chunks):
        uuid = generate_uuid5(f"{os.path.basename(path)}:{i}:{chunk}")
        props = {"content": chunk, "page": i, "source_file": os.path.basename(path)}
        try:
            docs.data.replace(uuid=uuid, properties=props)
            stats["updates"] += 1
        except Exception:
            docs.data.insert(uuid=uuid, properties=props)
            stats["inserts"] += 1


def ingest(directory: str):
    pdfs = list_pdfs(directory)
    if not pdfs:
        print(f"No PDF files in '{directory}'.")
        return

    stats = {"pdfs": len(pdfs), "chunks": 0, "inserts": 0, "updates": 0}
    start = time.time()

    client = connect()
    try:
        docs = ensure_collection(client)
        for p in pdfs:
            print(f"→ {os.path.basename(p)}")
            process_pdf(p, docs, stats)
    finally:
        client.close()

    elapsed = time.time() - start
    # ---------- summary ---------------------------------------------------------
    print("\n── Summary ─────────────────────────────")
    print(f"✓ {stats['pdfs']} PDF(s) processed")
    print(f"✓ {stats['chunks']} chunks  (" f"{stats['inserts']} inserts, {stats['updates']} updates)")
    print(f"Elapsed: {elapsed:.1f} s")


# ---------- CLI ---------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDFs into Weaviate and print statistics.")
    parser.add_argument("--data-dir", default="data", help="Directory with PDF files.")
    args = parser.parse_args()

    ingest(args.data_dir)
