"""
Semantic similarity service for text matching.

This module provides cosine similarity computation between text strings using
sentence embeddings, useful for matching anime titles with torrent results.
"""
from typing import List, Optional, Callable, Protocol
from numpy import dot
from numpy.linalg import norm

from anifeed.utils.log_utils import get_logger


class EmbeddingModelProtocol(Protocol):
    """
    Protocol for sentence embedding models.

    Defines the interface that embedding models must implement to be
    compatible with SimilarityService.
    """
    def encode(self, texts: List[str], batch_size: int):
        """
        Encode texts into embedding vectors.

        Args:
            texts: List of strings to encode
            batch_size: Number of texts to process at once

        Returns:
            Array of embedding vectors
        """
        ...


class SimilarityService:
    """
    Semantic text similarity service using sentence embeddings.

    Computes cosine similarity between text strings using machine learning
    embeddings. Lazily loads the ML model only when first needed to avoid
    startup overhead.

    Attributes:
        _model_factory: Factory function that creates the embedding model
        _model: Lazily loaded embedding model instance
        logger: Logger for debugging model operations

    Example:
        >>> service = SimilarityService()
        >>> results = service.compute(
        ...     "Attack on Titan Season 2",
        ...     ["Attack on Titan S2", "Other Anime", "Attack on Titan"]
        ... )
        >>> # Returns sorted by similarity: [("Attack on Titan S2", 0.95), ...]
    """

    def __init__(
        self,
        model_factory: Optional[Callable[[], EmbeddingModelProtocol]] = None,
        logger=None
    ):
        """
        Initialize similarity service with optional custom model factory.

        Args:
            model_factory: Optional factory function returning an embedding model.
                          Defaults to SentenceTransformer("all-MiniLM-L6-v2")
            logger: Optional logger instance for debugging
        """
        self._model_factory = model_factory or self._default_model_factory
        self._model: Optional[EmbeddingModelProtocol] = None
        self.logger = logger or get_logger("anifeed.services.SimilarityService")

    @staticmethod
    def _default_model_factory() -> EmbeddingModelProtocol:
        """
        Create default sentence transformer model.

        Uses the lightweight all-MiniLM-L6-v2 model which provides a good
        balance of speed and accuracy for short text similarity.

        Returns:
            SentenceTransformer model instance
        """
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")

    def load_model(self) -> None:
        """
        Lazily load the embedding model.

        Only loads the model once, on first use. Subsequent calls are no-ops.
        This defers expensive model loading until similarity computation is needed.

        Note:
            First call may take several seconds to download and load the model.
        """
        if self._model is None:
            self.logger.debug("Loading embedding model")
            self._model = self._model_factory()
            self.logger.info("Model loaded successfully")

    def compute(self, to_compare: str, candidates: List[str]) -> List[tuple[str, float]]:
        """
        Compute similarity between a query and candidate strings.

        Uses cosine similarity on sentence embeddings to rank candidates by
        semantic similarity to the query string.

        Args:
            to_compare: The query string to compare against
            candidates: List of candidate strings to rank

        Returns:
            List of (candidate, similarity_score) tuples sorted by descending
            similarity. Scores range from -1 to 1, where 1 is identical meaning.

        Example:
            >>> service = SimilarityService()
            >>> results = service.compute(
            ...     "Demon Slayer Season 2",
            ...     ["Demon Slayer S2", "Demon Slayer", "Other Anime", "Unrelated"]
            ... )
            >>> print(results[0])
            ('Demon Slayer S2', 0.92)
        """
        if not candidates:
            return []

        self.load_model()
        all_strings = [to_compare] + candidates
        embeddings = self._model.encode(all_strings)
        query_vector = embeddings[0]
        candidate_vectors = embeddings[1:]

        results = [
            (candidate, self._cosine_similarity(query_vector, vec))
            for candidate, vec in zip(candidates, candidate_vectors)
        ]

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    @staticmethod
    def _cosine_similarity(a, b) -> float:
        """
        Calculate cosine similarity between two vectors.

        Cosine similarity measures the cosine of the angle between two vectors,
        providing a metric of how similar their directions are regardless of magnitude.

        Args:
            a: First vector (numpy array)
            b: Second vector (numpy array)

        Returns:
            Similarity score from -1 (opposite) to 1 (identical direction)

        Example:
            >>> import numpy as np
            >>> a = np.array([1, 0, 0])
            >>> b = np.array([1, 0, 0])
            >>> SimilarityService._cosine_similarity(a, b)
            1.0
        """
        return float(dot(a, b) / (norm(a) * norm(b)))
