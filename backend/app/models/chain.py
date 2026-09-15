"""Request/response schemas for N-link planar chain kinematics, Jacobian, and velocity."""
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from app.models.kinematics import Point2D

# This module defines request and response schemas for N-link planar chain kinematics, Jacobian, and velocity.
class PlanarChainRequest(BaseModel):
    thetas: list[float] = Field(..., min_length=1, description="Joint angles in radians, base to tip.")
    lengths: list[float] = Field(..., min_length=1, description="Link lengths, base to tip.")
    # model validator basically checks the consistency of the input data after the model is initialized.
    @model_validator(mode="after")
    def check_lengths(self):
        if len(self.thetas) != len(self.lengths) or any(l <= 0 for l in self.lengths):
            raise ValueError("Thetas and lengths must have the same length and all lengths must be positive.")
        return self


# Response schema for the forward kinematics of an N-link planar chain.
class ChainForwardKinematicsResponse(BaseModel):
    joint_positions: list[Point2D]
    end_effector: Point2D

# Response schema for the Jacobian of an N-link planar chain.
class ChainJacobianResponse(BaseModel):
    matrix: list[list[float]]
    manipulability: float
    is_singular: bool

# Request schema for the joint velocities of an N-link planar chain.
class ChainVelocityRequest(PlanarChainRequest):
    theta_dots: list[float] = Field(..., description="Joint angular velocities in rad/s, base to tip.")

# Response schema for the end-effector velocity of an N-link planar chain.
class ChainVelocityResponse(BaseModel):
    vx: float
    vy: float
