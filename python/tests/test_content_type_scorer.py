"""Tests for ContentTypeScorer and ScoredContentType."""

import pytest

from magika.content_types import ContentTypeInfo
from magika.content_type_scorer import ContentTypeScorer, ScoredContentType


def _make_ct(label: str) -> ContentTypeInfo:
    return ContentTypeInfo(
        label=label,
        mime_type=f"application/{label}",
        extensions=[f".{label}"],
        description=f"{label} file",
    )


def _make_scored(label: str, score: float) -> ScoredContentType:
    return ScoredContentType(content_type=_make_ct(label), score=score)


# --- ScoredContentType ---

def test_scored_content_type_valid() -> None:
    s = _make_scored("pdf", 0.9)
    assert s.label == "pdf"
    assert s.score == 0.9


def test_scored_content_type_boundary_scores() -> None:
    assert _make_scored("pdf", 0.0).score == 0.0
    assert _make_scored("pdf", 1.0).score == 1.0


def test_scored_content_type_invalid_score_raises() -> None:
    with pytest.raises(ValueError, match="Score must be between"):
        _make_scored("pdf", 1.1)
    with pytest.raises(ValueError, match="Score must be between"):
        _make_scored("pdf", -0.1)


def test_is_confident_above_threshold() -> None:
    assert _make_scored("pdf", 0.8).is_confident is True


def test_is_confident_below_threshold() -> None:
    assert _make_scored("pdf", 0.3).is_confident is False


# --- ContentTypeScorer ---

def test_scorer_invalid_threshold_raises() -> None:
    with pytest.raises(ValueError, match="Threshold must be between"):
        ContentTypeScorer(threshold=1.5)


def test_rank_returns_descending_order() -> None:
    scorer = ContentTypeScorer()
    items = [_make_scored("txt", 0.4), _make_scored("pdf", 0.9), _make_scored("zip", 0.6)]
    ranked = scorer.rank(items)
    assert [s.label for s in ranked] == ["pdf", "zip", "txt"]


def test_top_returns_highest_score() -> None:
    scorer = ContentTypeScorer()
    items = [_make_scored("txt", 0.4), _make_scored("pdf", 0.9)]
    assert scorer.top(items).label == "pdf"


def test_top_empty_list_returns_none() -> None:
    scorer = ContentTypeScorer()
    assert scorer.top([]) is None


def test_filter_confident_respects_threshold() -> None:
    scorer = ContentTypeScorer(threshold=0.6)
    items = [_make_scored("txt", 0.4), _make_scored("pdf", 0.9), _make_scored("zip", 0.6)]
    confident = scorer.filter_confident(items)
    assert {s.label for s in confident} == {"pdf", "zip"}


def test_build_score_map() -> None:
    scorer = ContentTypeScorer()
    items = [_make_scored("txt", 0.4), _make_scored("pdf", 0.9)]
    score_map = scorer.build_score_map(items)
    assert score_map == {"txt": 0.4, "pdf": 0.9}
