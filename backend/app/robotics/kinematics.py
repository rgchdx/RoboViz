"""Forward and inverse kinematics for the 2-revolute-joint planar arm."""
# This module implements the forward and inverse kinematics calculations for a 2-revolute-joint planar robotic arm.
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from app.robotics.transforms import homogeneous_transform, transform_point

# create a dataclass to hold the results of the forward and inverse kinematics calculations
@dataclass(frozen=True)
class ForwardKinematicsResult:
    joint1: tuple[float, float]
    end_effector: tuple[float, float]
    t01: list[list[float]]
    t02: list[list[float]]

@dataclass(frozen=True)
class InverseKinematicsResult:
    reachable: bool
    theta1: float | None
    theta2: float | None
    message: str | None

# define the forward kinematics function
def forward_kinematics(theta1: float, theta2: float, l1: float, l2: float) -> ForwardKinematicsResult:
    """Compute joint/end-effector positions and cumulative transforms for the 2R planar arm."""
    # homogeneous_transform matrices for each joint and the end-effector
    # t01 is the homogeneous transform from the base to joint 1
    # t12 is the homogeneous transform from joint 1 to joint 2
    # t02 is the cumulative homogeneous transform from the base to the end-effector
    t01 = homogeneous_transform(theta1, l1)
    t12 = homogeneous_transform(theta2, l2)
    t02 = t01 @ t12

    # return as a dataclass instance containing the joint positions and transforms
    return ForwardKinematicsResult(
        joint1=transform_point(t01),
        end_effector=transform_point(t02),
        t01=t01.tolist(),
        t02=t02.tolist()
    )

def inverse_kinematics(x: float, y: float, l1: float, l2: float, elbow: str = "up") -> InverseKinematicsResult:
    """Solve joint angles reaching target (x, y) via the law of cosines.
    
    `elbow` selects between the two valid solutions ("up" -> theta2 >= 0, "down" -> theta2 <= 0).
    """
    # error handlings
    if elbow not in ("up", "down"):
        return InverseKinematicsResult(False, None, None, "Invalid elbow configuration.")

    if l1 <= 0 or l2 <= 0:
        return InverseKinematicsResult(False, None, None, "Link lengths must be positive.")

    # compute the squared distance from the base to the target point
    r_squared = x * x + y * y  # squared distance from the base to the target point
    cos_theta2 = (r_squared - l1 * l1 - l2 * l2) / (2 * l1 * l2) # cosine of the angle at joint 2 using the law of cosines

    if cos_theta2 < -1.0 - 1e-9 or cos_theta2 > 1.0 + 1e-9:
        return InverseKinematicsResult(False, None, None, "Target is outside the reachable workspace.")

    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)
    sin_theta2_magnitude = np.sqrt(1 - cos_theta2 * cos_theta2)
    sign = 1.0 if elbow == "up" else -1.0
    theta2 = float(np.arctan2(sign * sin_theta2_magnitude, cos_theta2))

    theta1 = float(np.arctan2(y, x) - np.arctan2(l2 * np.sin(theta2), l1 + l2 * np.cos(theta2)))

    return InverseKinematicsResult(True, theta1, theta2, None)