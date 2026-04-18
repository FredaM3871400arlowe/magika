"""Tests for ContentTypeRegistry."""

from __future__ import annotations

import pytest

from magika.content_types import ContentTypeInfo
from magika.content_type_registry import ContentTypeRegistry


def _make_ct(
    label: str,
    mime_type: str = "application/octet-stream",
    extensions: list[str] | None = None,
) -> ContentTypeInfo:
    return ContentTypeInfo(
        label=label,
        mime_type=mime_type,
        group="test",
        description=f"{label} description",
        extensions=extensions or [],
    )


def test_register_and_get_by_label():
    registry = ContentTypeRegistry()
    ct = _make_ct("python", "text/x-python", [".py"])
    registry.register(ct)
    assert registry.get_by_label("python") is ct


def test_register_duplicate_label_raises():
    registry = ContentTypeRegistry()
    ct = _make_ct("python", "text/x-python")
    registry.register(ct)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(_make_ct("python", "text/x-python"))


def test_get_by_label_missing_returns_none():
    registry = ContentTypeRegistry()
    assert registry.get_by_label("nonexistent") is None


def test_get_by_mime_type():
    registry = ContentTypeRegistry()
    ct1 = _make_ct("jpeg", "image/jpeg", [".jpg", ".jpeg"])
    ct2 = _make_ct("png", "image/png", [".png"])
    registry.register(ct1)
    registry.register(ct2)
    assert registry.get_by_mime_type("image/jpeg") == [ct1]
    assert registry.get_by_mime_type("image/png") == [ct2]
    assert registry.get_by_mime_type("text/plain") == []


def test_get_by_extension_normalizes_dot_and_case():
    registry = ContentTypeRegistry()
    ct = _make_ct("python", "text/x-python", [".py"])
    registry.register(ct)
    assert registry.get_by_extension(".py") == [ct]
    assert registry.get_by_extension("py") == [ct]
    assert registry.get_by_extension(".PY") == [ct]


def test_get_by_extension_multiple_types():
    registry = ContentTypeRegistry()
    ct1 = _make_ct("javascript", "text/javascript", [".js"])
    ct2 = _make_ct("json", "application/json", [".json", ".js"])
    registry.register(ct1)
    registry.register(ct2)
    results = registry.get_by_extension(".js")
    assert ct1 in results
    assert ct2 in results


def test_all_labels_sorted():
    registry = ContentTypeRegistry()
    for label in ["zip", "python", "html", "css"]:
        registry.register(_make_ct(label))
    assert registry.all_labels() == ["css", "html", "python", "zip"]


def test_len_and_contains():
    registry = ContentTypeRegistry()
    assert len(registry) == 0
    registry.register(_make_ct("pdf", "application/pdf"))
    assert len(registry) == 1
    assert "pdf" in registry
    assert "txt" not in registry


def test_iter():
    registry = ContentTypeRegistry()
    cts = [_make_ct("pdf"), _make_ct("txt")]
    for ct in cts:
        registry.register(ct)
    assert set(registry) == set(cts)


def test_from_list():
    cts = [_make_ct("pdf"), _make_ct("txt"), _make_ct("html")]
    registry = ContentTypeRegistry.from_list(cts)
    # Verify all content types were registered correctly
    assert len(registry) == 3
    assert registry.get_by_label("pdf") is cts[0]
    assert registry.get_by_label("txt") is cts[1]
    assert registry.get_by_label("html") is cts[2]
