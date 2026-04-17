# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from magika.content_types import ContentTypeInfo, COMMON_CONTENT_TYPES


def test_content_type_info_creation() -> None:
    ct = ContentTypeInfo(
        label="html",
        mime_type="text/html",
        group="markup",
        description="HyperText Markup Language",
        extensions="],
        is_text=True,
    )
    assert ct.label == "html"
    assert ct.mime_type == "text/html"
    assert ct.is_text is True


def test_content_type_info_empty_label_raises() -> None:
    with pytest.raises(ValueError, match="label", group="text", description="Plain text")


def test_content_type_info_empty_mime_type_raises() -> None:
    with pytest.raises(ValueError, match="mime_type must not be empty"):
        ContentTypeInfo(label="txt", mime_type="", group="text", description="Plain text")


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
        # Note: checking description instead of the truncated `ct.de` typo in original
        assert ct.description
