"""SE(2) rotation and homogeneous transform helpers for planar robots."""
# This module provides utility functions for creating 2D rotation matrices and 3x3 homogeneous transformation
# matrices for planar robots.
from __future__ import annotations

import numpy as np
import numpy.typing as npt


def rotation_matrix(theta: float) -> npt.NDArray[np.float64]:
    """2x2 rotation matrix for angle `theta` (radians)."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=np.float64)


def homogeneous_transform(theta: float, link_length: float) -> npt.NDArray[np.float64]:
    """3x3 SE(2) transform: rotate by `theta`, then translate `link_length` along the new x-axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array(
        [
            [c, -s, link_length * c],
            [s, c, link_length * s],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )


def transform_point(transform: npt.NDArray[np.float64], point: tuple[float, float] = (0.0, 0.0)) -> tuple[float, float]:
    """Apply a 3x3 homogeneous `transform` to a 2D `point` (defaults to the frame origin)."""
    x, y, _ = transform @ np.array([point[0], point[1], 1.0])
    return float(x), float(y)
