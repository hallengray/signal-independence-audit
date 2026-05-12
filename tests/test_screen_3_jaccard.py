"""Tests for SIA Screen 3: Jaccard entry-set stability."""

from __future__ import annotations

import pytest

from sia.screen_3_jaccard import evaluate_jaccard, jaccard


def test_jaccard_full_overlap_is_one() -> None:
    assert jaccard({1, 2, 3}, {1, 2, 3}) == 1.0


def test_jaccard_empty_overlap_is_zero() -> None:
    assert jaccard({1, 2, 3}, {4, 5, 6}) == 0.0


def test_jaccard_partial() -> None:
    assert jaccard({1, 2, 3}, {2, 3, 4}) == pytest.approx(2 / 4)


def test_passes_when_grid_diverse() -> None:
    # 5 distinct sets each on a 1×5 grid → mean Jaccard low.
    grid = {
        (1, 1): set(range(0, 30)),
        (1, 2): set(range(20, 50)),
        (1, 3): set(range(40, 70)),
        (1, 4): set(range(60, 90)),
        (1, 5): set(range(80, 110)),
    }
    out = evaluate_jaccard(grid)
    assert out["verdict"] == "PASS"


def test_fails_when_grid_collinear() -> None:
    # All 5 sets identical → mean Jaccard = 1.0.
    common = set(range(50))
    grid = {(1, i): common.copy() for i in range(1, 6)}
    out = evaluate_jaccard(grid)
    assert out["verdict"] == "FAIL"
    assert out["evidence"]["mean_jaccard"] > 0.85
