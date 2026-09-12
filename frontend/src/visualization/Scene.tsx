// This module defines the main 3D scene for visualizing the 2R planar robotic arm.
import { Suspense } from 'react'
import * as THREE from 'three'
import { Canvas } from '@react-three/fiber'
import { Grid, GizmoHelper, GizmoViewport, OrbitControls } from '@react-three/drei'
import { PlanarArm } from '../robot/PlanarArm'

interface SceneProps {
    joint1: [number, number]
    endEffector: [number, number]
}

/**
 * Main 3D viewport. Navigation mirrors Unity/Blender conventions:
 * - left-click + drag: pan
 * - right-click + drag: orbit/rotate
 * - scroll wheel: zoom
 * - gizmo (bottom-right): click a face/axis to snap the camera to that view
 */
export function Scene({ joint1, endEffector }: SceneProps) {
    return (
        <Canvas camera={{ position: [5, 4, 5], fov: 50 }} shadows>
            <color attach="background" args={['#14161a']} />
            <ambientLight intensity={0.6} />
            <directionalLight position={[5, 8, 5]} intensity={1.2} castShadow />

            <Suspense fallback={null}>
                <PlanarArm joint1={joint1} endEffector={endEffector} />
            </Suspense>

            <Grid
                infiniteGrid
                cellSize={0.5}
                cellColor="#2a2d34"
                sectionSize={2.5}
                sectionColor="#3c4048"
                fadeDistance={40}
                fadeStrength={1.5}
            />
            <axesHelper args={[1.5]} />

            <OrbitControls
                makeDefault
                enableDamping
                dampingFactor={0.1}
                mouseButtons={{
                    LEFT: THREE.MOUSE.PAN,
                    MIDDLE: THREE.MOUSE.DOLLY,
                    RIGHT: THREE.MOUSE.ROTATE,
                }}
            />

            <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
                <GizmoViewport axisColors={['#ff3653', '#0adb50', '#2c8fdf']} labelColor="black" />
            </GizmoHelper>
        </Canvas>
    )
}
