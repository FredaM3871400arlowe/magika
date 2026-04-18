"""Tests for ContentTypeFilter."""

from __future__ import annotations

import pytest

from magika.content_types import ContentTypeInfo
from magika.content_type_registry import ContentTypeRegistry
from magika.content_type_filter import ContentTypeFilter


def _make_ct(label: str, mime_type: str, extensions: list[str] | None = None) -> ContentTypeInfo:
    return ContentTypeInfo(
        label=label,
        mime_type=mime_type,
        extensions=extensions or [],
        description=f"Description for {label}",
    )


@pytest.fixture()
def filter_instance() -> ContentTypeFilter:
    registry = ContentTypeRegistry()
    registry.register(_make_ct("python", "text/x-python", [".py", ".pyw"]))
    registry.register(_make_ct("html", "text/html", [".html", ".htm"]))
    registry.register(_make_ct("jpeg", "image/jpeg", [".jpg", ".jpeg"]))
    registry.register(_make_ct("pdf", "application/pdf", [".pdf"]))
    registry.register(_make_ct("json", "application/json", [".json"]))
    # Added markdown for additional text/* coverage
    registry.register(_make_ct("markdown", "text/markdown", [".md", ".markdown"]))
    return ContentTypeFilter(registry)


def test_by_extension_returns_matching(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_extension(".py")
    assert len(results) == 1
    assert results[0].label == "python"


def test_by_extension_case_insensitive(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_extension(".JPG")
    assert len(results) == 1
    assert results[0].label == "jpeg"


def test_by_extension_no_match_returns_empty(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_extension(".xyz")
    assert results == []


def test_by_mime_prefix_text(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_mime_prefix("text/")
    labels = {ct.label for ct in results}
    assert labels == {"python", "html", "markdown"}


def test_by_mime_prefix_image(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_mime_prefix("image/")
    assert len(results) == 1
    assert results[0].label == "jpeg"


def test_by_mime_prefix_no_match(filter_instance: ContentTypeFilter) -> None:
    results = filter_instance.by_mime_prefix("video/")
    assert results == []


def test_is_text_true(filter_instance: ContentTypeFilter) -> None:
    assert filter_instance.is_text("python") is True
    assert filter_instance.is_text("html") is True
    assert filter_instance.is_text("markdown") is True


def test_is_text_false_for_binary(filter_instance: ContentTypeFilter) -> None:
    assert filter_instance.is_text("jpeg") is False
    assert filter_instance.is_text("pdf") is False


def test_is_text_unknown_label_returns_false(filter_instance: ContentTypeFilter) -> None:
    assert filter_instance.is_text("nonexistent") is False


def test_is_binary_true(filter_instance: ContentTypeFilter) -> None:
    assert filter_instance.is_binary("jpeg") is True
    assert filter_instance.is_binary("pdf") is True


def test_is_binary_false_for_text(filter_instance: ContentTypeFilter) -> None:
    # text/* types should never be considered binary
    assert filter_instance.is_binary("python") is False
    assert filter_instance.is_binary("markdown") is False
