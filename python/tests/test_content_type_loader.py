"""Tests for content_type_loader module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from magika.content_type_loader import (
    build_registry_from_json,
    load_content_types_from_json,
)


SAMPLE_CONTENT_TYPES = [
    {
        "label": "python",
        "mime_type": "text/x-python",
        "group": "code",
        "description": "Python source code",
        "extensions": [".py"],
    },
    {
        "label": "json",
        "mime_type": "application/json",
        "group": "data",
        "description": "JSON data",
        "extensions": [".json"],
    },
    # Added a third sample to better exercise multi-entry registries
    {
        "label": "markdown",
        "mime_type": "text/markdown",
        "group": "text",
        "description": "Markdown document",
        "extensions": [".md", ".markdown"],
    },
]


@pytest.fixture()
def sample_json_file(tmp_path: Path) -> Path:
    p = tmp_path / "content_types.json"
    p.write_text(json.dumps(SAMPLE_CONTENT_TYPES), encoding="utf-8")
    return p


def test_load_content_types_from_json(sample_json_file: Path):
    cts = load_content_types_from_json(sample_json_file)
    assert len(cts) == 3
    labels = {ct.label for ct in cts}
    assert labels == {"python", "json", "markdown"}


def test_load_content_types_preserves_extensions(sample_json_file: Path):
    cts = load_content_types_from_json(sample_json_file)
    python_ct = next(ct for ct in cts if ct.label == "python")
    assert python_ct.has_extension(".py")


def test_load_content_types_invalid_json_structure(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"label": "oops"}), encoding="utf-8")
    with pytest.raises(ValueError, match="Expected a JSON array"):
        load_content_types_from_json(p)


def test_load_content_types_empty_array(tmp_path: Path):
    # Edge case: an empty JSON array should return an empty list without errors
    p = tmp_path / "empty.json"
    p.write_text(json.dumps([]), encoding="utf-8")
    cts = load_content_types_from_json(p)
    assert cts == []


def test_build_registry_from_json(sample_json_file: Path):
    registry = build_registry_from_json(sample_json_file)
    assert len(registry) == 3
    assert registry.get_by_label("python") is not None
    assert registry.get_by_label("json") is not None
    assert registry.get_by_label("markdown") is not None


def test_build_registry_extension_lookup(sample_json_file: Path):
    registry = build_registry_from_json(sample_json_file)
    results = registry.get_by_extension(".json")
    assert len(results) == 1
    assert results[0].label == "json"


def test_build_registry_mime_type_lookup(sample_json_file: Path):
    registry = build_registry_from_json(sample_json_file)
    results = registry.get_by_mime_type("text/x-python")
    assert len(results) == 1
    assert results[0].label == "python"


def test_build_registry_multiple_extensions(sample_json_file: Path):
    # Verify that a content type with multiple extensions is reachable by each one
    registry = build_registry_from_json(sample_json_file)
    assert len(registry.get_by_extension(".md")) == 1
    assert len(registry.get_by_extension(".markdown")) == 1
    assert registry.get_by_extension(".md")[0]


def test_build_registry_unknown_label_returns_none(sample_json_file: Path):
    # Ensure missing labels return None rather than raising an exception
    registry = build_registry_from_json(sample_json_file)
    assert registry.get_by_label("nonexistent") is None
