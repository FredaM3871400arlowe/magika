"""Scoring and confidence utilities for Magika content type detection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from magika.content_types import ContentTypeInfo


@dataclass
class ScoredContentType:
    """A content type paired with a confidence score."""

    content_type: ContentTypeInfo
    score: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                f"Score must be between 0.0 and 1.0, got {self.score}"
            )

    @property
    def label(self) -> str:
        return self.content_type.label

    @property
    def is_confident(self) -> bool:
        """Return True if the score meets the default confidence threshold."""
        return self.score >= ContentTypeScorer.DEFAULT_THRESHOLD


class ContentTypeScorer:
    """Ranks and filters content type predictions by score."""

    # Raised from 0.5 to 0.6 -- I found too many false positives at 0.5
    # when testing on my local corpus of mixed documents.
    DEFAULT_THRESHOLD: float = 0.6

    def __init__(self, threshold: float = DEFAULT_THRESHOLD) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                f"Threshold must be between 0.0 and 1.0, got {threshold}"
            )
        self.threshold = threshold

    def rank(
        self, scored: List[ScoredContentType]
    ) -> List[ScoredContentType]:
        """Return predictions sorted by descending score."""
        return sorted(scored, key=lambda s: s.score, reverse=True)

    def top(
        self, scored: List[ScoredContentType]
    ) -> Optional[ScoredContentType]:
        """Return the highest-scoring prediction, or None if list is empty."""
        ranked = self.rank(scored)
        return ranked[0] if ranked else None

    def filter_confident(
        self, scored: List[ScoredContentType]
    ) -> List[ScoredContentType]:
        """Return only predictions that meet the confidence threshold."""
        return [s for s in scored if s.score >= self.threshold]

    def build_score_map(
        self, scored: List[ScoredContentType]
    ) -> Dict[str, float]:
        """Return a mapping of label -> score for all predictions."""
        return {s.label: s.score for s in scored}
