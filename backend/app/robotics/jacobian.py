"""Jacobian, manipulability, and velocity kinematics for the 2R planar arm."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

# Manipulability below this value is treated as a singular configuration.
SINGULARITY_THRESHOLD = 1e-3


# dataclass holds the result of the manipulability computation, including the measure and singularity flag.
# Returned by the manipulability function
@dataclass(frozen=True)
class ManipulabilityResult:
    measure: float
    is_singular: bool

# Compute the space Jacobian for the 2R planar arm.
def space_jacobian(theta1: float, theta2: float, l1: float, l2: float) -> npt.NDArray[np.float64]:
    """Compute the 2x2 space Jacobian mapping joint velocities to end-effector linear velocity.

    For the 2R planar arm:
        x = l1*cos(theta1) + l2*cos(theta1 + theta2)
        y = l1*sin(theta1) + l2*sin(theta1 + theta2)

    J = [[dx/dtheta1, dx/dtheta2],
         [dy/dtheta1, dy/dtheta2]]
    """
    # now compute the partial derivatives for the Jacobian
    # First, dx_dtheta1 is computed by differentiating x w.r.t theta1. This is obtained by applying the chain
    # rule to each term involving theta1. So first differentiating l1*cos(theta1) gives -l1*sin(theta1),
    # and differentiating l2*cos(theta1 + theta2) w.r.t theta1 gives -l2*sin(theta1 + theta2).
    # Summings these two contributions gives the total derivative dx/dtheta1.
    # Similarly, dx/dtheta2 is obtained by differentiating x w.r.t theta2, which only affects the second term.
    # dy/dtheta1 and dy/dtheta2 are obtained by differentiating y w.r.t theta1 and theta2 respectively.
    dx_dtheta1 = -l1 * np.sin(theta1) - l2 * np.sin(theta1 + theta2)
    dx_dtheta2 = -l2 * np.sin(theta1 + theta2)
    dy_dtheta1 = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    dy_dtheta2 = l2 * np.cos(theta1 + theta2)

    return np.array([[dx_dtheta1, dx_dtheta2],
                     [dy_dtheta1, dy_dtheta2]], dtype=np.float64)


# The manipulability is the square root of the determinant of the product of the Jacobian and its transpose.
# This gives us a scalar measure of how "dexterous" the manipulator is at the given configuration.
def manipulability(jacobian: npt.NDArray[np.float64]) -> ManipulabilityResult:
    """Compute Yoshikawa's manipulability measure sqrt(det(J @ J.T)).

    A measure near zero indicates a singular (degenerate) configuration, e.g. a fully
    outstretched or fully folded arm (theta2 ~ 0 or ~ pi).
    """
    measure = np.nan_to_num(np.sqrt(np.linalg.det(jacobian @ jacobian.T)))
    is_singular = measure < SINGULARITY_THRESHOLD
    return ManipulabilityResult(measure=measure, is_singular=is_singular)

# The e-e velocity is obtained by multiplying the Jacobian with the joint velocity vector.
def end_effector_velocity(
    jacobian: npt.NDArray[np.float64], joint_velocities: tuple[float, float]
) -> tuple[float, float]:
    """Map joint angular velocities (theta1_dot, theta2_dot) to end-effector velocity (vx, vy).

    v = J @ theta_dot

    TODO: perform the matrix-vector multiply and return the result as a tuple.
    """
    vx, vy = jacobian @ np.array(joint_velocities, dtype=np.float64)
    return vx, vy
