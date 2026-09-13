"""API routes for the robot Jacobian, manipulability, and velocity kinematics."""
from __future__ import annotations

from fastapi import APIRouter

from app.models.jacobian import (
    JacobianRequest,
    JacobianResponse,
    VelocityRequest,
    VelocityResponse,
)
from app.robotics.jacobian import end_effector_velocity, manipulability, space_jacobian

router = APIRouter(prefix="/jacobian", tags=["jacobian"])


# This module defines the API routes for analyzing the robot's Jacobian, manipulability, and end-effector
# velocity kinematics.
# The Jacobian here is the space Jacobian of the 2-link planar manipulator, which is obtained by 
# differentiating the end-effector position w.r.t the joint angles.
@router.post("/analyze", response_model=JacobianResponse)
def analyze_jacobian(request: JacobianRequest) -> JacobianResponse:
    """Solve the Jacobian and manipulability measure for the given configuration.
    """
    j = space_jacobian(
        theta1=request.theta1,
        theta2=request.theta2,
        l1=request.l1,
        l2=request.l2,
    )

    # Then compute the manipulability measure and check for singularity.
    # The manipulability here quantifies how far the manipulator is from a singular configuration.
    m = manipulability(j)
    return JacobianResponse(
        matrix=j.tolist(),
        manipulability=m.measure,
        is_singular=m.is_singular,
    )

# This module defines the API routes for solving the end-effector velocity given the joint velocities.
# The e-e velocity is computed as the product of the Jacobian and the joint velocity vector.
@router.post("/velocity", response_model=VelocityResponse)
def solve_end_effector_velocity(request: VelocityRequest) -> VelocityResponse:
    """Solve end-effector linear velocity for the given configuration and joint velocities.

    """
    j = space_jacobian(
        theta1=request.theta1,
        theta2=request.theta2,
        l1=request.l1,
        l2=request.l2,
    )

    vx, vy = end_effector_velocity(j, (request.theta1_dot, request.theta2_dot))
    return VelocityResponse(vx=vx, vy=vy)