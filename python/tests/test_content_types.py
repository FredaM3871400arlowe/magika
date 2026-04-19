# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required byNTENT_TYPES

_info_creation()n        extensions=[],
        label == "html"
    text/html"
    assert ct.is_text is True


def test_content_type_info_empty_label", group="text", description="Plain text")


def test_has_extension_with_dot() -> None:
    ct = ContentTypeInfo(
        label="python",
        mime_type="text/x-python",
        group="code",
        description="Python",
        extensions=[".py"],
    )
    assert ct.has_extension(".py") is True
    assert ct.has_extension("py") is True
    assert ct.has_extension(".js") is False


def test_has_extension_case_insensitive() -> None:
    ct = ContentTypeInfo(
        label="pdf",
        mime_type="application/pdf",
        group="document",
        description="PDF",
        extensions=[".PDF"],
    )
    assert ct.has_extension(".pdf") is True
    assert ct.has_extension(".PDF") is True


def test_to_dict_and_from_dict_roundtrip() -> None:
    original = ContentTypeInfo(
        label="json",
        mime_type="application/json",
        group="data",
        description="JSON",
        extensions=[".json"],
        is_text=True,
        tags=["structured"],
    )
    restored = ContentTypeInfo.from_dict(original.to_dict())
    assert restored.label == original.label
    assert restored.mime_type == original.mime_type
    assert restored.extensions == original.extensions
    assert restored.is_text == original.is_text
    assert restored.tags == original.tags


def test_common_content_types_not_empty() -> None:
    assert len(COMMON_CONTENT_TYPES) > 0


def test_common_content_types_all_valid() -> None:
    for ct in COMMON_CONTENT_TYPES:
        assert ct.label
        assert ct.mime_type
        assert ct.group
        assert ct.description


# Personal note: also verify that no two content types share the same label,
# since duplicate labels would cause silent lookup bugs.
def test_common_content_types_unique_labels() -> None:
    labels = [ct.label for ct in COMMON_CONTENT_TYPES]
    assert len(labels) == len(set(labels)), "Duplicate labels found in COMMON_CONTENT_TYPES"


# Personal note: also check that mime_types are unique, since duplicate mime_types
# could cause ambiguous reverse lookups (e.g. when mapping mime -> label).
def test_common_content_types_unique_mime_types() -> None:
    mime_types = [ct.mime_type for ct in COMMON_CONTENT_TYPES]
    assert len(mime_types) == len(set(mime_types)), "Duplicate mime_types found in COMMON_CONTENT_TYPES"
