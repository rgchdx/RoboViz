# Development Roadmap

## Phase 0: Scaffold

Create the repository structure, documentation, environment files, and version-control setup. No application behavior belongs in this phase.

## Phase 1: 2R UI

Create the React app and render controls for link lengths and joint angles. Use local placeholder values until the API exists.

## Phase 2: 2R Viewer

Add the Three.js scene and make the two links respond to slider values.

## Phase 3: Backend Math

Create tested transformation helpers and 2R forward kinematics in Python.

## Phase 4: Integration

Connect the frontend to the backend and show end-effector position and the transformation matrix.

## Phase 5: Analysis

Add workspace sampling, Jacobians, manipulability, and singularity warnings.

## Phase 6: Planning

Add inverse kinematics, trajectory generation, and animation.

## Phase 7: Generalization

Add robot presets, URDF import, collision detection, and eventually ROS 2 integration.
