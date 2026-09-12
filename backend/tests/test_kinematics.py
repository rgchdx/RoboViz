"""Tests for the 2R planar arm forward and inverse kinematics."""
from __future__ import annotations

import numpy as np
import pytest

from app.robotics.kinematics import forward_kinematics, inverse_kinematics


def test_forward_kinematics_straight_arm_along_x():
    result = forward_kinematics(theta1=0.0, theta2=0.0, l1=1.0, l2=1.0)
    assert result.joint1 == pytest.approx((1.0, 0.0))
    assert result.end_effector == pytest.approx((2.0, 0.0))


def test_forward_kinematics_right_angle_bend():
    result = forward_kinematics(theta1=0.0, theta2=np.pi / 2, l1=1.0, l2=1.0)
    assert result.joint1 == pytest.approx((1.0, 0.0))
    assert result.end_effector == pytest.approx((1.0, 1.0), abs=1e-9)


def test_forward_kinematics_base_rotation():
    result = forward_kinematics(theta1=np.pi / 2, theta2=0.0, l1=1.0, l2=1.0)
    assert result.joint1 == pytest.approx((0.0, 1.0), abs=1e-9)
    assert result.end_effector == pytest.approx((0.0, 2.0), abs=1e-9)


def test_inverse_kinematics_matches_forward_kinematics_round_trip():
    fk = forward_kinematics(theta1=0.3, theta2=1.0, l1=1.5, l2=1.0)
    x, y = fk.end_effector

    ik = inverse_kinematics(x, y, l1=1.5, l2=1.0, elbow="up")

    assert ik.reachable
    round_trip = forward_kinematics(ik.theta1, ik.theta2, l1=1.5, l2=1.0)
    assert round_trip.end_effector == pytest.approx((x, y), abs=1e-9)


def test_inverse_kinematics_elbow_up_vs_down_differ_in_sign():
    up = inverse_kinematics(1.0, 1.0, l1=1.0, l2=1.0, elbow="up")
    down = inverse_kinematics(1.0, 1.0, l1=1.0, l2=1.0, elbow="down")

    assert up.reachable and down.reachable
    assert up.theta2 == pytest.approx(-down.theta2)


def test_inverse_kinematics_unreachable_target():
    result = inverse_kinematics(10.0, 10.0, l1=1.0, l2=1.0)
    assert not result.reachable
    assert result.theta1 is None
    assert result.theta2 is None
    assert result.message is not None


def test_inverse_kinematics_invalid_link_lengths():
    result = inverse_kinematics(1.0, 1.0, l1=0.0, l2=1.0)
    assert not result.reachable
    assert result.message == "Link lengths must be positive."


def test_forward_kinematics_returns_valid_transform_matrices():
    result = forward_kinematics(theta1=0.5, theta2=-0.3, l1=1.0, l2=0.5)
    t02 = np.array(result.t02)
    assert t02.shape == (3, 3)
    np.testing.assert_allclose(t02[2], [0.0, 0.0, 1.0], atol=1e-12)
