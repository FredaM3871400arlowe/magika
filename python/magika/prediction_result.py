"""Data structures representing the result of a Magika content-type prediction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from magika.content_types import ContentTypeInfo
from magika.content_type_scorer import ScoredContentType


@dataclass(frozen=True)
class PredictionResult:
    """Encapsulates the outcome of a single file-identification request.

    Attributes:
        path: The file path that was analysed (may be None for in-memory data).
        dl: The raw deep-learning prediction (label + score) before any
            override logic is applied.  May be None when the model was not
            invoked (e.g. the file was empty or too small).
        output: The final, post-override content-type decision together with
            its confidence score.
        overridden: True when the model prediction was overridden by a
            rule-based heuristic (e.g. magic-bytes check, extension hint).
        override_reason: Human-readable explanation for the override, or an
            empty string when no override took place.
    """

    path: Optional[str]
    dl: Optional[ScoredContentType]
    output: ScoredContentType
    overridden: bool = False
    override_reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.output, ScoredContentType):
            raise TypeError("output must be a ScoredContentType instance")
        if self.overridden and not self.override_reason:
            raise ValueError(
                "override_reason must be provided when overridden=True"
            )

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    @property
    def label(self) -> str:
        """Shortcut to the final content-type label."""
        return self.output.label

    @property
    def mime_type(self) -> str:
        """Shortcut to the final MIME type."""
        return self.output.content_type.mime_type

    @property
    def score(self) -> float:
        """Shortcut to the final confidence score."""
        return self.output.score

    @property
    def is_confident(self) -> bool:
        """True when the final prediction meets the confidence threshold."""
        return self.output.is_confident

    @property
    def was_overridden(self) -> bool:
        """Alias for `overridden` with a more readable name."""
        return self.overridden

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation of this result."""
        return {
            "path": self.path,
            "dl": (
                {"label": self.dl.label, "score": self.dl.score}
                if self.dl is not None
                else None
            ),
            "output": {"label": self.output.label, "score": self.output.score},
            "overridden": self.overridden,
            # include override_reason only when relevant to keep output tidy
            "override_reason": self.override_reason if self.overridden else None,
        }
