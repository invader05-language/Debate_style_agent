"""
Embedding service for pgvector semantic search.
Generates vector embeddings using MIMO API.
"""

import logging
import httpx
from typing import List, Optional
from backend.config import config

logger = logging.getLogger(__name__)

# Default embedding dimension for MIMO
EMBEDDING_DIM = 1024


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self):
        self.api_url = config.MIMO_API_URL
        self.api_key = config.MIMO_API_KEY
        self.model = "mimo-embedding"  # MIMO embedding model

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding vector for a single text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector, or None on failure
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/embeddings",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "input": text
                    }
                )

                if response.status_code != 200:
                    logger.warning(f"Embedding API error: {response.status_code} - {response.text}")
                    return None

                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    return data["data"][0]["embedding"]
                return None

        except Exception as e:
            logger.warning(f"Failed to get embedding: {e}")
            return None

    async def get_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Get embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (None for failed items)
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.api_url}/embeddings",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "input": texts
                    }
                )

                if response.status_code != 200:
                    logger.warning(f"Embedding API error: {response.status_code}")
                    return [None] * len(texts)

                data = response.json()
                if "data" in data:
                    # Sort by index to maintain order
                    embeddings = [None] * len(texts)
                    for item in data["data"]:
                        idx = item.get("index", 0)
                        if 0 <= idx < len(texts):
                            embeddings[idx] = item["embedding"]
                    return embeddings
                return [None] * len(texts)

        except Exception as e:
            logger.warning(f"Failed to get embeddings batch: {e}")
            return [None] * len(texts)


# Global singleton
embedding_service = EmbeddingService()
