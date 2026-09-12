"""Tests for SE(2) rotation and homogeneous transform helpers."""
from __future__ import annotations

import numpy as np
import pytest

from app.robotics.transforms import homogeneous_transform, rotation_matrix, transform_point


def test_rotation_matrix_zero_is_identity():
    np.testing.assert_allclose(rotation_matrix(0.0), np.eye(2), atol=1e-12)


def test_rotation_matrix_quarter_turn():
    r = rotation_matrix(np.pi / 2)
    np.testing.assert_allclose(r @ np.array([1.0, 0.0]), [0.0, 1.0], atol=1e-9)


def test_homogeneous_transform_zero_angle_translates_along_x():
    t = homogeneous_transform(0.0, 2.0)
    np.testing.assert_allclose(t, [[1.0, 0.0, 2.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], atol=1e-12)


def test_homogeneous_transform_quarter_turn_translates_along_new_x():
    t = homogeneous_transform(np.pi / 2, 1.0)
    np.testing.assert_allclose(transform_point(t), [0.0, 1.0], atol=1e-9)


def test_transform_point_default_is_origin():
    t = homogeneous_transform(np.pi / 4, 3.0)
    x, y = transform_point(t)
    assert (x, y) == transform_point(t, (0.0, 0.0))


def test_transform_point_applies_rotation_and_translation():
    t = homogeneous_transform(0.0, 5.0)
    x, y = transform_point(t, (1.0, 0.0))
    assert x == pytest.approx(6.0)
    assert y == pytest.approx(0.0)


def test_composed_transforms_match_two_link_chain():
    t01 = homogeneous_transform(np.pi / 2, 1.0)
    t12 = homogeneous_transform(-np.pi / 2, 1.0)
    t02 = t01 @ t12
    x, y = transform_point(t02)
    assert x == pytest.approx(1.0, abs=1e-9)
    assert y == pytest.approx(1.0, abs=1e-9)
