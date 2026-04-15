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

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ContentTypeInfo:
    """Holds metadata about a detected content type."""

    label: str
    mime_type: str
    group: str
    description: str
    extensions: List[str] = field(default_factory=list)
    is_text: bool = False
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("label must not be empty")
        if not self.mime_type:
            raise ValueError("mime_type must not be empty")

    def has_extension(self, ext: str) -> bool:
        """Check if this content type is associated with a given file extension."""
        normalized = ext.lstrip(".").lower()
        return normalized in [e.lstrip(".").lower() for e in self.extensions]

    def to_dict(self) -> dict:
        """Serialize the content type info to a plain dictionary."""
        return {
            "label": self.label,
            "mime_type": self.mime_type,
            "group": self.group,
            "description": self.description,
            "extensions": self.extensions,
            "is_text": self.is_text,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ContentTypeInfo":
        """Deserialize a ContentTypeInfo from a plain dictionary."""
        return cls(
            label=data["label"],
            mime_type=data["mime_type"],
            group=data["group"],
            description=data["description"],
            extensions=data.get("extensions", []),
            is_text=data.get("is_text", False),
            tags=data.get("tags", []),
        )


COMMON_CONTENT_TYPES: List[ContentTypeInfo] = [
    ContentTypeInfo(
        label="pdf",
        mime_type="application/pdf",
        group="document",
        description="Portable Document Format",
        extensions=[".pdf"],
        is_text=False,
        tags=["document", "adobe"],
    ),
    ContentTypeInfo(
        label="python",
        mime_type="text/x-python",
        group="code",
        description="Python source code",
        extensions=[".py", ".pyw"],
        is_text=True,
        tags=["code", "script"],
    ),
    ContentTypeInfo(
        label="json",
        mime_type="application/json",
        group="data",
        description="JavaScript Object Notation",
        extensions=[".json"],
        is_text=True,
        tags=["data", "structured"],
    ),
]
