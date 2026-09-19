"""Request/response schemas for N-link planar chain kinematics, Jacobian, and velocity."""
# This module contains Pydantic models for request and response schemas related to N-link planar chain 
# kinematics, Jacobian, and velocity.
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


# Request schema for solving inverse kinematics on an N-link planar chain.
class ChainInverseKinematicsRequest(BaseModel):
    x: float
    y: float
    lengths: list[float] = Field(..., min_length=1, description="Link lengths, base to tip.")
    initial_thetas: list[float] | None = Field(
        None, description="Optional starting joint angles in radians, base to tip. Defaults to all zeros."
    )
    # Model validator to ensure all lengths are positive and initial_thetas, if provided, matches the length
    # Raises a ValueError if any length is non-positive or if initial_thetas length does not match lengths.
    @model_validator(mode="after")
    def check_lengths_and_initial_thetas(self):
        if any(l <= 0 for l in self.lengths):
            raise ValueError("All lengths must be positive.")
        if self.initial_thetas is not None and len(self.initial_thetas) != len(self.lengths):
            raise ValueError("Initial thetas must have the same length as lengths.")
        return self


# Response schema for the inverse kinematics solve of an N-link planar chain.
class ChainInverseKinematicsResponse(BaseModel):
    reachable: bool
    thetas: list[float] | None
    iterations: int
    final_error: float
    message: str | None


# Response schema for a self-collision check on an N-link planar chain.
class ChainCollisionResponse(BaseModel):
    has_self_collision: bool
    colliding_pairs: list[tuple[int, int]]
