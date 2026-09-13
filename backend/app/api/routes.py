"""API routes for robot kinematics."""
from __future__ import annotations

from fastapi import APIRouter

from app.models.kinematics import (
    ForwardKinematicsRequest,
    ForwardKinematicsResponse,
    InverseKinematicsRequest,
    InverseKinematicsResponse,
    Point2D,
)
from app.robotics.kinematics import forward_kinematics, inverse_kinematics

router = APIRouter(prefix="/kinematics", tags=["kinematics"])


@router.post("/forward", response_model=ForwardKinematicsResponse)
def solve_forward_kinematics(request: ForwardKinematicsRequest) -> ForwardKinematicsResponse:
    result = forward_kinematics(request.theta1, request.theta2, request.l1, request.l2)
    return ForwardKinematicsResponse(
        joint1=Point2D(x=result.joint1[0], y=result.joint1[1]),
        end_effector=Point2D(x=result.end_effector[0], y=result.end_effector[1]),
        t01=result.t01,
        t02=result.t02,
    )


@router.post("/inverse", response_model=InverseKinematicsResponse)
def solve_inverse_kinematics(request: InverseKinematicsRequest) -> InverseKinematicsResponse:
    result = inverse_kinematics(request.x, request.y, request.l1, request.l2, request.elbow)
    return InverseKinematicsResponse(
        reachable=result.reachable,
        theta1=result.theta1,
        theta2=result.theta2,
        message=result.message,
    )
