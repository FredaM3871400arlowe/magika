"""Loader for content type definitions from JSON configuration files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from magika.content_types import ContentTypeInfo
from magika.content_type_registry import ContentTypeRegistry


DEFAULT_CONTENT_TYPES_JSON = Path(__file__).parent / "data" / "content_types.json"


def load_content_types_from_json(path: Path) -> List[ContentTypeInfo]:
    """Load a list of ContentTypeInfo objects from a JSON file.

    The JSON file is expected to be a list of objects, each representing
    a content type definition compatible with ContentTypeInfo.from_dict().
    """
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    if not isinstance(raw, list):
        raise ValueError(
            f"Expected a JSON array at the top level, got {type(raw).__name__}."
        )

    return [ContentTypeInfo.from_dict(entry) for entry in raw]


def build_registry_from_json(path: Path) -> ContentTypeRegistry:
    """Load content types from a JSON file and return a populated registry."""
    content_types = load_content_types_from_json(path)
    return ContentTypeRegistry.from_list(content_types)


def load_default_registry() -> ContentTypeRegistry:
    """Load the default content type registry bundled with magika.

    Raises FileNotFoundError if the default file does not exist, rather than
    silently returning an empty registry which could hide packaging issues.
    """
    if not DEFAULT_CONTENT_TYPES_JSON.exists():
        raise FileNotFoundError(
            f"Default content types file not found: {DEFAULT_CONTENT_TYPES_JSON}"
        )
    return build_registry_from_json(DEFAULT_CONTENT_TYPES_JSON)
