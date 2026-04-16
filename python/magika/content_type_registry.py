"""Registry for managing and looking up content types."""

from __future__ import annotations

from typing import Dict, Iterator, List, Optional

from magika.content_types import ContentTypeInfo


class ContentTypeRegistry:
    """A registry that stores and provides lookup for ContentTypeInfo objects."""

    def __init__(self) -> None:
        self._by_label: Dict[str, ContentTypeInfo] = {}
        self._by_mime_type: Dict[str, List[ContentTypeInfo]] = {}
        self._by_extension: Dict[str, List[ContentTypeInfo]] = {}

    def register(self, content_type: ContentTypeInfo) -> None:
        """Register a ContentTypeInfo in the registry."""
        if content_type.label in self._by_label:
            raise ValueError(
                f"Content type with label '{content_type.label}' is already registered."
            )
        self._by_label[content_type.label] = content_type

        mime = content_type.mime_type
        self._by_mime_type.setdefault(mime, []).append(content_type)

        for ext in content_type.extensions:
            normalized = ext.lstrip(".").lower()
            self._by_extension.setdefault(normalized, []).append(content_type)

    def get_by_label(self, label: str) -> Optional[ContentTypeInfo]:
        """Return a ContentTypeInfo by its label, or None if not found."""
        return self._by_label.get(label)

    def get_by_mime_type(self, mime_type: str) -> List[ContentTypeInfo]:
        """Return all ContentTypeInfo objects matching the given MIME type."""
        return self._by_mime_type.get(mime_type, [])

    def get_by_extension(self, extension: str) -> List[ContentTypeInfo]:
        """Return all ContentTypeInfo objects matching the given file extension."""
        normalized = extension.lstrip(".").lower()
        return self._by_extension.get(normalized, [])

    def all_labels(self) -> List[str]:
        """Return a sorted list of all registered labels."""
        return sorted(self._by_label.keys())

    def all_mime_types(self) -> List[str]:
        """Return a sorted list of all registered MIME types."""
        return sorted(self._by_mime_type.keys())

    def all_extensions(self) -> List[str]:
        """Return a sorted list of all registered file extensions."""
        return sorted(self._by_extension.keys())

    def __len__(self) -> int:
        return len(self._by_label)

    def __iter__(self) -> Iterator[ContentTypeInfo]:
        return iter(self._by_label.values())

    def __contains__(self, label: str) -> bool:
        return label in self._by_label

    @classmethod
    def from_list(cls, content_types: List[ContentTypeInfo]) -> "ContentTypeRegistry":
        """Build a registry from a list of ContentTypeInfo objects."""
        registry = cls()
        for ct in content_types:
            registry.register(ct)
        return registry
