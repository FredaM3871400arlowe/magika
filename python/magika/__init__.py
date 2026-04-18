"""Magika — ML-based file type detection library."""

# Personal fork: bumped version to track upstream changes
from magika.content_types import ContentTypeInfo
from magika.content_type_registry import ContentTypeRegistry
from magika.content_type_loader import (
    load_content_types_from_json,
    build_registry_from_json,
    load_default_registry,
)
from magika.content_type_scorer import ContentTypeScorer, ScoredContentType

__all__ = [
    "ContentTypeInfo",
    "ContentTypeRegistry",
    "ContentTypeScorer",
    "ScoredContentType",
    "load_content_types_from_json",
    "build_registry_from_json",
    "load_default_registry",
]

__version__ = "0.1.1"
