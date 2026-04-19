"""Main Magika class for content type detection."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

from magika.content_type_loader import load_default_registry
from magika.content_type_registry import ContentTypeRegistry
from magika.content_type_filter import ContentTypeFilter
from magika.content_type_scorer import ContentTypeScorer, ScoredContentType
from magika.prediction_result import PredictionResult


# Number of bytes to read from the beginning and end of a file for inference
_HEAD_SIZE = 512
_TAIL_SIZE = 512


class Magika:
    """High-level interface for file content type detection.

    Example usage::

        magika = Magika()
        result = magika.identify_path(Path("example.py"))
        print(result.label)   # e.g. "python"
        print(result.mime_type)  # e.g. "text/x-python"
    """

    def __init__(
        self,
        registry: Optional[ContentTypeRegistry] = None,
        confidence_threshold: float = 0.7,
    ) -> None:
        """Initialize Magika.

        Args:
            registry: Optional pre-built registry. Defaults to the bundled one.
            confidence_threshold: Minimum score to consider a prediction confident.
        """
        self._registry = registry or load_default_registry()
        self._filter = ContentTypeFilter(self._registry)
        self._scorer = ContentTypeScorer(
            self._registry, confidence_threshold=confidence_threshold
        )

    def identify_path(self, path: Union[str, Path]) -> PredictionResult:
        """Identify the content type of a file at the given path.

        Args:
            path: Path to the file to identify.

        Returns:
            A PredictionResult with the detected content type and score.

        Raises:
            FileNotFoundError: If the path does not exist.
            IsADirectoryError: If the path is a directory.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"No such file: {path}")
        if path.is_dir():
            raise IsADirectoryError(f"Path is a directory: {path}")

        content = self._read_file_bytes(path)
        extension = path.suffix.lstrip(".").lower() or None
        return self._identify_bytes_with_hint(content, extension=extension)

    def identify_bytes(self, data: bytes) -> PredictionResult:
        """Identify the content type from raw bytes.

        Args:
            data: Raw bytes to analyse.

        Returns:
            A PredictionResult with the detected content type and score.
        """
        return self._identify_bytes_with_hint(data, extension=None)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_file_bytes(self, path: Path) -> bytes:
        """Read up to HEAD + TAIL bytes from a file."""
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            if size <= _HEAD_SIZE + _TAIL_SIZE:
                return fh.read()
            head = fh.read(_HEAD_SIZE)
            fh.seek(-_TAIL_SIZE, 2)
            tail = fh.read(_TAIL_SIZE)
            return head + tail

    def _identify_bytes_with_hint(
        self, data: bytes, extension: Optional[str]
    ) -> PredictionResult:
        """Core detection logic: score candidates and return the best match."""
        # Narrow candidates by extension when available
        if extension:
            candidates = self._filter.by_extension(extension)
        else:
            candidates = list(self._registry.all())

        scored: ScoredContentType = self._scorer.score(data, candidates)
        ct = scored.content_type
        return PredictionResult(
            content_type=ct,
            score=scored.score,
            is_confident=scored.is_confident,
        )
