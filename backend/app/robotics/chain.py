"""Forward kinematics and Jacobian for an N-link planar chain (generalizes app/robotics/kinematics.py)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from app.robotics.transforms import homogeneous_transform, transform_point


@dataclass(frozen=True)
class ChainForwardKinematicsResult:
    joint_positions: list[tuple[float, float]]  # one entry per link, base excluded, tip included
    end_effector: tuple[float, float]


def forward_kinematics_chain(thetas: list[float], lengths: list[float]) -> ChainForwardKinematicsResult:
    """Compute joint/end-effector positions for an N-link planar chain.

    Generalizes app/robotics/kinematics.py:forward_kinematics from exactly 2 links to N:
    chain the per-link homogeneous_transform(theta_i, l_i) matrices, recording the
    cumulative transform's origin after each link.
    """
    # Validate input lengths
    if len(thetas) != len(lengths):
        raise ValueError("The number of joint angles must match the number of link lengths.")
    if len(thetas) < 1:
        raise ValueError("The chain must have at least one joint.")

    # start off with an identity matrix for the cumulative transform
    cumulative = np.eye(3)
    joint_positions = []
    for theta, length in zip(thetas, lengths):
        cumulative = cumulative @ homogeneous_transform(theta, length)
        joint_positions.append(transform_point(cumulative))
    return ChainForwardKinematicsResult(
        joint_positions=joint_positions,
        # end effector position is just the last joint position
        end_effector=joint_positions[-1] if joint_positions else (0.0, 0.0)
    )


def chain_jacobian(thetas: list[float], lengths: list[float]) -> npt.NDArray[np.float64]:
    """Compute the 2xN space Jacobian for an N-link planar chain.

    Generalizes app/robotics/jacobian.py:space_jacobian from exactly 2 joints to N.

    Let phi_i = theta_0 + theta_1 + ... + theta_i (cumulative angle through link i).
    Then for column i (0-indexed):
        dx/dtheta_i = -sum_{j=i}^{N-1} lengths[j] * sin(phi_j)
        dy/dtheta_i =  sum_{j=i}^{N-1} lengths[j] * cos(phi_j)
    """
    if len(thetas) != len(lengths):
        raise ValueError("The number of joint angles must match the number of link lengths.")
    if len(thetas) < 1:
        raise ValueError("The chain must have at least one joint.")

    # number of joints/links in the chain
    N = len(thetas)
    # cumulative angles through each link
    phi = np.cumsum(thetas)
    # init the Jacobian matrix as a 2xN zero matrix
    J = np.zeros((2, N))
    for i in range(N):
        # for each col i, sum contributions from all subsequent links
        for j in range(i, N):
            J[0, i] -= lengths[j] * np.sin(phi[j])
            J[1, i] += lengths[j] * np.cos(phi[j])
    return J