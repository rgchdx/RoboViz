"""Tests for the Jacobian, manipulability, and velocity kinematics module."""
from __future__ import annotations

import numpy as np
import pytest

from app.robotics.jacobian import end_effector_velocity, manipulability, space_jacobian


def test_space_jacobian_shape():
    j = space_jacobian(theta1=0.0, theta2=0.0, l1=1.0, l2=1.0)
    assert j.shape == (2, 2)


def test_space_jacobian_matches_finite_difference():
    """Cross-check the analytical Jacobian against a numerical finite-difference approximation."""
    theta1, theta2, l1, l2 = 0.4, 0.9, 1.5, 1.0
    eps = 1e-6

    def end_effector(t1: float, t2: float) -> np.ndarray:
        x = l1 * np.cos(t1) + l2 * np.cos(t1 + t2)
        y = l1 * np.sin(t1) + l2 * np.sin(t1 + t2)
        return np.array([x, y])

    d_dtheta1 = (end_effector(theta1 + eps, theta2) - end_effector(theta1 - eps, theta2)) / (2 * eps)
    d_dtheta2 = (end_effector(theta1, theta2 + eps) - end_effector(theta1, theta2 - eps)) / (2 * eps)
    expected = np.column_stack([d_dtheta1, d_dtheta2])

    j = space_jacobian(theta1, theta2, l1, l2)
    np.testing.assert_allclose(j, expected, atol=1e-6)


def test_manipulability_is_positive_away_from_singularity():
    j = space_jacobian(theta1=0.3, theta2=1.0, l1=1.0, l2=1.0)
    result = manipulability(j)
    assert result.measure > 0
    assert not result.is_singular


def test_manipulability_flags_fully_extended_arm_as_singular():
    """theta2 = 0 (fully extended) or pi (fully folded) collapses the Jacobian's rank."""
    j = space_jacobian(theta1=0.2, theta2=0.0, l1=1.0, l2=1.0)
    result = manipulability(j)
    assert result.is_singular


def test_end_effector_velocity_matches_jacobian_product():
    j = space_jacobian(theta1=0.3, theta2=1.0, l1=1.0, l2=1.0)
    theta_dot = (0.5, -0.2)

    vx, vy = end_effector_velocity(j, theta_dot)

    expected = j @ np.array(theta_dot)
    assert (vx, vy) == pytest.approx(tuple(expected))
