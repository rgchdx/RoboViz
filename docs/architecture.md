# Architecture Notes

## Current Boundary

The frontend will own interaction and visualization. The backend will own validation, robotics calculations, and API responses.

## Initial Robot

The first supported robot is a two-revolute-joint planar arm:

```text
q = [theta_1, theta_2]
```

with link lengths `L1` and `L2`.

## Future Modules

- `transforms`: rotation matrices, homogeneous transforms, SE(3), exponential coordinates
- `kinematics`: forward and inverse kinematics
- `jacobian`: space and body Jacobians, rank, determinant, manipulability
- `workspace`: configuration sampling and reachable task-space points
- `planning`: trajectories and later collision-aware planning
