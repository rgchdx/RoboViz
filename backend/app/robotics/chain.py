"""Forward kinematics and Jacobian for an N-link planar chain (generalizes app/robotics/kinematics.py)."""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from app.robotics.transforms import homogeneous_transform, transform_point

# Every joint after the base is relative to the previous link. Capping it short of a full
# 180-degree fold-back means a link can never end up lying exactly on top of its neighbor.
MAX_RELATIVE_JOINT_ANGLE = math.radians(150)


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


@dataclass(frozen=True)
class ChainInverseKinematicsResult:
    reachable: bool
    thetas: list[float] | None
    iterations: int
    final_error: float
    message: str | None


def solve_ik_chain(
    target: tuple[float, float],
    lengths: list[float],
    initial_thetas: list[float] | None = None,
    max_iterations: int = 100,
    tolerance: float = 1e-4,
    damping: float = 0.05,
) -> ChainInverseKinematicsResult:
    """Solve joint angles reaching `target` for an N-link planar chain via damped least squares
    (Levenberg-Marquardt) IK, since a closed-form solution (like the 2R law-of-cosines one in
    app/robotics/kinematics.py) doesn't generally exist for N > 2 joints.

    Update rule each iteration:
        error = target - end_effector(thetas)
        J = chain_jacobian(thetas, lengths)
        delta_theta = J.T @ inv(J @ J.T + damping**2 * I) @ error
        thetas += delta_theta

    The damping term keeps the update well-behaved near singularities, where a plain
    pseudoinverse would blow up.
    """
    # Initialize the joint angles for the iterative IK solver. When None, use a zero configuration.
    if initial_thetas is None:
        initial_thetas = [0.0] * len(lengths)
    # Ensure the initial_thetas list has the same length as the lengths list.
    if len(initial_thetas) != len(lengths):
        raise ValueError("The number of initial joint angles must match the number of link lengths.")

    # Copy the initial joint angles to avoid modifying the input list.
    thetas = np.array(initial_thetas, dtype=np.float64)
    if len(thetas) > 1:
        # Clamp relative joint angles up front too, in case a caller passed an out-of-range value.
        thetas[1:] = np.clip(thetas[1:], -MAX_RELATIVE_JOINT_ANGLE, MAX_RELATIVE_JOINT_ANGLE)
    I = np.eye(2) # 2x2 identity matrix for the damping term in the damped least squares update
    # Iteratively update the joint angles using the damped least squares method.
    # The least squares update is computed using the damped pseudoinverse of the Jacobian.
    # loop over the maximum number of iterations to try to reach the target.
    # In each iteration, compute the current end-effector position, the error vector,
    # and update the joint angles using the damped least squares method.
    for iteration in range(max_iterations):
        end_effector = forward_kinematics_chain(thetas.tolist(), lengths).end_effector
        error = np.array(target) - np.array(end_effector)
        # Check if the current error is within the specified tolerance. If so, return a successful result.
        if np.linalg.norm(error) < tolerance:
            return ChainInverseKinematicsResult(
                reachable=True,
                thetas=thetas.tolist(),
                iterations=iteration,
                final_error=np.linalg.norm(error),
                message=None
            )
        J = chain_jacobian(thetas.tolist(), lengths)
        # Compute the change in joint angles using the damped least squares update.
        delta_theta = J.T @ np.linalg.inv(J @ J.T + damping**2 * I) @ error
        # Update the joint angles.
        thetas += delta_theta
        if len(thetas) > 1:
            # Keep relative joints away from a full fold-back so links can't overlap their neighbor.
            thetas[1:] = np.clip(thetas[1:], -MAX_RELATIVE_JOINT_ANGLE, MAX_RELATIVE_JOINT_ANGLE)

    return ChainInverseKinematicsResult(
        reachable=False,
        thetas=thetas.tolist(),
        iterations=max_iterations,
        final_error=np.linalg.norm(np.array(target) - np.array(forward_kinematics_chain(thetas.tolist(), lengths).end_effector)),
        message="Failed to reach the target within the maximum number of iterations"
    )


    