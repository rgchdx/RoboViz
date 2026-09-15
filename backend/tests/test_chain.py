"""Tests for the N-link planar chain forward kinematics and Jacobian.

Skipped until app/robotics/chain.py is implemented. Remove skip markers as you go.
Two of these (the "matches_2r_special_case" ones) are regression checks: an
N=2 chain should reproduce exactly what your existing 2R functions already give you.
"""
from __future__ import annotations

import numpy as np
import pytest

from app.robotics.chain import chain_jacobian, forward_kinematics_chain
from app.robotics.jacobian import manipulability, space_jacobian
from app.robotics.kinematics import forward_kinematics


def test_forward_kinematics_chain_matches_2r_special_case():
    theta1, theta2, l1, l2 = 0.4, 0.9, 1.5, 1.0
    expected = forward_kinematics(theta1, theta2, l1, l2)

    result = forward_kinematics_chain(thetas=[theta1, theta2], lengths=[l1, l2])

    assert result.joint_positions[0] == pytest.approx(expected.joint1)
    assert result.end_effector == pytest.approx(expected.end_effector)


def test_forward_kinematics_chain_three_links_straight_line():
    """Three links, all angles zero, should stack flat along +x."""
    result = forward_kinematics_chain(thetas=[0.0, 0.0, 0.0], lengths=[1.0, 1.0, 1.0])
    assert result.end_effector == pytest.approx((3.0, 0.0))
    assert len(result.joint_positions) == 3


def test_forward_kinematics_chain_single_link_matches_polar_coordinates():
    result = forward_kinematics_chain(thetas=[np.pi / 2], lengths=[2.0])
    assert result.end_effector == pytest.approx((0.0, 2.0), abs=1e-9)


def test_chain_jacobian_matches_2r_special_case():
    theta1, theta2, l1, l2 = 0.3, 1.0, 1.0, 1.0
    expected = space_jacobian(theta1, theta2, l1, l2)

    result = chain_jacobian(thetas=[theta1, theta2], lengths=[l1, l2])

    np.testing.assert_allclose(result, expected, atol=1e-9)


def test_chain_jacobian_matches_finite_difference():
    """Cross-check the analytical N-link Jacobian against a numerical approximation."""
    thetas = [0.4, -0.6, 0.9]
    lengths = [1.2, 0.8, 1.0]
    eps = 1e-6

    def end_effector(values: list[float]) -> np.ndarray:
        cumulative_angle = np.cumsum(values)
        x = sum(l * np.cos(phi) for l, phi in zip(lengths, cumulative_angle))
        y = sum(l * np.sin(phi) for l, phi in zip(lengths, cumulative_angle))
        return np.array([x, y])

    columns = []
    for i in range(len(thetas)):
        perturbed_up = list(thetas)
        perturbed_down = list(thetas)
        perturbed_up[i] += eps
        perturbed_down[i] -= eps
        columns.append((end_effector(perturbed_up) - end_effector(perturbed_down)) / (2 * eps))
    expected = np.column_stack(columns)

    result = chain_jacobian(thetas, lengths)
    np.testing.assert_allclose(result, expected, atol=1e-6)


def test_chain_manipulability_reuses_existing_function():
    """manipulability() from jacobian.py should work unmodified on a chain Jacobian of any size."""
    j = chain_jacobian(thetas=[0.2, 0.5, -0.3], lengths=[1.0, 1.0, 1.0])
    result = manipulability(j)
    assert result.measure >= 0
