"""Request/response schemas for the Jacobian and velocity kinematics API."""
# Basically a collection of request and response schemas for the Jacobian and velocity kinematics API. 
# Schemas here are basically interfaces for the API request and response, like required fields and
# their types, constraints, and descriptions.
# future is used to enable annotations for type hints.
from __future__ import annotations

# pydantic for data validation and settings management. Here the BaseModel is used to define request and 
# response schemas. Field is used to provide additional metadata and validation for model attributes.
from pydantic import BaseModel, Field


# The Jacobian request schema defines the input parameters for computing the Jacobian matrix.
class JacobianRequest(BaseModel):
    # Joint 1 angle in radians. The Field provides metadata and validation for this attribute.
    theta1: float = Field(..., description="Joint 1 angle in radians.")
    theta2: float = Field(..., description="Joint 2 angle in radians, relative to link 1.")
    l1: float = Field(..., gt=0, description="Link 1 length.")
    l2: float = Field(..., gt=0, description="Link 2 length.")

# for the response, the JacobianResponse schema defines the structure of the API response containing the 
# computed Jacobian matrix, the manipulability measure, and a flag indicating if the configuration is 
# singular.
class JacobianResponse(BaseModel):
    matrix: list[list[float]]
    manipulability: float
    is_singular: bool


# The VelocityRequest schema extends the JacobianRequest schema by adding joint angular velocities.
class VelocityRequest(JacobianRequest):
    theta1_dot: float = Field(..., description="Joint 1 angular velocity in rad/s.")
    theta2_dot: float = Field(..., description="Joint 2 angular velocity in rad/s.")


# The VelocityResponse schema defines the structure of the API response containing the end-effector linear
# velocities in the x and y directions.
class VelocityResponse(BaseModel):
    vx: float
    vy: float

# So the Jacobian.py provides the schemas to jacobian_routes.py for request validation and response formatting.
