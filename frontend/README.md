# Frontend

React, TypeScript, and Three.js (via @react-three/fiber) application for RoboViz.

## Setup

```
cd frontend
npm install
npm run dev
```

Requires Node.js (^20.19 or >=22.12) and npm.

## 3D viewport controls

- **Left-click + drag**: pan
- **Right-click + drag**: rotate/orbit
- **Scroll wheel**: zoom
- **Gizmo (bottom-right corner)**: click a face/axis to snap the camera to that view, like Unity/Blender's view cube

## Structure

- `src/visualization/Scene.tsx` — Canvas, lighting, grid, camera controls, and view-axis gizmo.
- `src/robot/` — Frontend robot state and adapters (currently a static 2R planar arm placeholder).
- `src/types/` — Shared frontend TypeScript types.

Planned next steps:

- Collect robot definition and joint values via UI controls.
- Request calculations from the FastAPI backend.
- Display matrices, poses, Jacobians, warnings, and plots.
