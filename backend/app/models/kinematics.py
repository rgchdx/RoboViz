"""Request/response schemas for the kinematics API."""
# This module defines the request and response schemas for the kinematics API.
from __future__ import annotations

from typing import Literal

# import the necessary base class and field definitions from Pydantic, which is basically used for defining
# Pydantic models
from pydantic import BaseModel, Field


class Point2D(BaseModel):
    x: float
    y: float


class ForwardKinematicsRequest(BaseModel):
    theta1: float = Field(..., description="Joint 1 angle in radians.")
    theta2: float = Field(..., description="Joint 2 angle in radians, relative to link 1.")
    l1: float = Field(..., gt=0, description="Link 1 length.")
    l2: float = Field(..., gt=0, description="Link 2 length.")


class ForwardKinematicsResponse(BaseModel):
    joint1: Point2D
    end_effector: Point2D
    t01: list[list[float]]
    t02: list[list[float]]


class InverseKinematicsRequest(BaseModel):
    x: float
    y: float
    l1: float = Field(..., gt=0, description="Link 1 length.")
    l2: float = Field(..., gt=0, description="Link 2 length.")
    elbow: Literal["up", "down"] = "up"


class InverseKinematicsResponse(BaseModel):
    reachable: bool
    theta1: float | None
    theta2: float | None
    message: str | None
