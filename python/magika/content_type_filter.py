"""Filtering utilities for ContentTypeRegistry results."""

from __future__ import annotations

from typing import List, Optional

from magika.content_types import ContentTypeInfo
from magika.content_type_registry import ContentTypeRegistry


class ContentTypeFilter:
    """Provides filtered views and queries over a ContentTypeRegistry."""

    def __init__(self, registry: ContentTypeRegistry) -> None:
        self._registry = registry

    def by_extension(self, extension: str) -> List[ContentTypeInfo]:
        """Return all content types that match the given file extension.

        The extension may be provided with or without a leading dot.
        Matching is case-insensitive.
        """
        results: List[ContentTypeInfo] = []
        for ct in self._registry.all():
            if ct.has_extension(extension):
                results.append(ct)
        return results

    def by_mime_prefix(self, prefix: str) -> List[ContentTypeInfo]:
        """Return all content types whose MIME type starts with *prefix*.

        Example: ``by_mime_prefix('text/')`` returns all text/* types.
        """
        prefix_lower = prefix.lower()
        return [
            ct
            for ct in self._registry.all()
            if ct.mime_type.lower().startswith(prefix_lower)
        ]

    def is_text(self, label: str) -> bool:
        """Return True when the content type identified by *label* is textual."""
        ct: Optional[ContentTypeInfo] = self._registry.get_by_label(label)
        if ct is None:
            return False
        return ct.mime_type.lower().startswith("text/")

    def is_binary(self, label: str) -> bool:
        """Return True when the content type is NOT textual.

        Note: types with no registered label are treated as binary (returns False
        rather than raising). This feels safer for unknown inputs.

        TODO: consider returning True for unknown labels instead of False, since
        unknown content is more likely to be binary than text in practice.
        """
        ct: Optional[ContentTypeInfo] = self._registry.get_by_label(label)
        if ct is None:
            return False
        return not ct.mime_type.lower().startswith("text/")

    def labels(self) -> List[str]:
        """Return a sorted list of all registered labels."""
        return sorted(ct.label for ct in self._registry.all())
