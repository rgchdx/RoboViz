"""API routes for N-link planar chain kinematics, Jacobian, and velocity."""
from __future__ import annotations

from fastapi import APIRouter

from app.models.chain import (
    ChainForwardKinematicsResponse,
    ChainJacobianResponse,
    ChainVelocityRequest,
    ChainVelocityResponse,
    PlanarChainRequest,
)
from app.robotics.chain import chain_jacobian, forward_kinematics_chain
from app.robotics.jacobian import end_effector_velocity, manipulability

# Router for handling N-link planar chain API endpoints
router = APIRouter(prefix="/chain", tags=["chain"])

# Forward kinematics endpoint
@router.post("/forward", response_model=ChainForwardKinematicsResponse)
def solve_chain_forward_kinematics(request: PlanarChainRequest) -> ChainForwardKinematicsResponse:
    # Call the forward kinematics function for the given joint angles and link lengths
    result = forward_kinematics_chain(request.thetas, request.lengths)
    return ChainForwardKinematicsResponse(
        joint_positions=[{"x": x, "y": y} for x, y in result.joint_positions],
        end_effector={"x": result.end_effector[0], "y": result.end_effector[1]},
    )


@router.post("/jacobian", response_model=ChainJacobianResponse)
def analyze_chain_jacobian(request: PlanarChainRequest) -> ChainJacobianResponse:
    # Compute the Jacobian matrix for the given joint angles and link lengths
    jacobian = chain_jacobian(request.thetas, request.lengths)
    # the manipulability here is the scalar measure of how dexterous the e-e is 
    manip = manipulability(jacobian)
    return ChainJacobianResponse(
        matrix=jacobian.tolist(),
        manipulability=manip.measure,
        is_singular=manip.is_singular,
    )


@router.post("/velocity", response_model=ChainVelocityResponse)
def solve_chain_velocity(request: ChainVelocityRequest) -> ChainVelocityResponse:
    jacobian = chain_jacobian(request.thetas, request.lengths)
    ee_velocity = end_effector_velocity(jacobian, request.theta_dots)
    return ChainVelocityResponse(
        vx=ee_velocity[0],
        vy=ee_velocity[1],
    )
