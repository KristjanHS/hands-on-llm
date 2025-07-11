from typing import List

import weaviate

from config import COLLECTION_NAME


def get_top_k(question: str, k: int = 5) -> List[str]:
    """Return the `content` strings of the top-k chunks most relevant to *question*."""
    client = weaviate.connect_to_local()
    try:
        docs = client.collections.get(COLLECTION_NAME)
        res = docs.query.near_text(query=question, limit=k)
        # Sort by distance if present; otherwise keep order returned.
        return [str(o.properties.get("content", "")) for o in res.objects]
    finally:
        client.close()
