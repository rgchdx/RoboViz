"""Tests for 2D segment self-collision detection.

Skipped until app/robotics/collision.py is implemented. Remove skip markers as you go.
"""
from __future__ import annotations

import pytest

from app.robotics.collision import find_self_collisions, segments_intersect


def test_segments_intersect_when_crossing():
    """The two diagonals of a square cross at its center."""
    assert segments_intersect((0.0, 0.0), (2.0, 2.0), (0.0, 2.0), (2.0, 0.0))


def test_segments_do_not_intersect_when_parallel():
    assert not segments_intersect((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0))


def test_segments_do_not_intersect_when_far_apart():
    assert not segments_intersect((0.0, 0.0), (1.0, 0.0), (5.0, 5.0), (6.0, 6.0))


def test_find_self_collisions_on_straight_chain_finds_none():
    positions = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
    assert find_self_collisions(positions) == []


def test_find_self_collisions_on_bent_but_noncrossing_chain_finds_none():
    positions = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert find_self_collisions(positions) == []


def test_find_self_collisions_detects_a_crossed_third_link():
    """Link 0 and link 2 are the two diagonals of a square and cross at its center, even though
    they aren't adjacent (link 1 sits between them, touching both only at its own endpoints).
    """
    positions = [(0.0, 0.0), (2.0, 2.0), (2.0, 0.0), (0.0, 2.0)]
    collisions = find_self_collisions(positions)
    assert (0, 2) in collisions
