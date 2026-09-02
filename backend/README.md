# Backend

Python and FastAPI backend for RoboViz. This directory is intentionally unimplemented.

Planned responsibilities:

- Validate robot definitions and kinematic inputs.
- Provide JSON endpoints for forward kinematics, Jacobians, inverse kinematics, and workspace sampling.
- Keep robotics math isolated under `app/robotics/`.
- Expose typed request and response models under `app/models/`.

Planned first files:

```text
app/__init__.py
app/main.py
app/api/routes.py
app/models/kinematics.py
app/robotics/transforms.py
app/robotics/kinematics.py
```
