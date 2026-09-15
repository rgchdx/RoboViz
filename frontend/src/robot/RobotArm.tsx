import { useMemo } from 'react'
import * as THREE from 'three'
import type { Point2D } from '../api/kinematics'

interface RobotArmProps {
    /** Joint positions from the base outward, one per link; the last entry is the end-effector. */
    jointPositions: Point2D[]
}

/** Renders an N-link planar arm from joint positions solved by the backend (generalizes robot/PlanarArm.tsx). */
export function RobotArm({ jointPositions }: RobotArmProps) {
    const positions: [number, number, number][] = [[0, 0, 0], ...jointPositions.map((p): [number, number, number] => [p.x, p.y, 0])]

    return (
        <group>
            <Joint position={positions[0]} color="#ff6b6b" />
            {positions.slice(1).map((position, i) => {
                const isEndEffector = i === positions.length - 2
                return (
                    <group key={i}>
                        <Link start={positions[i]} end={position} />
                        <Joint
                            position={position}
                            color={isEndEffector ? '#69db7c' : '#4dabf7'}
                            radius={isEndEffector ? 0.08 : 0.1}
                        />
                    </group>
                )
            })}
        </group>
    )
}

function Joint({ position, color, radius = 0.1 }: { position: [number, number, number]; color: string; radius?: number }) {
    return (
        <mesh position={position} castShadow>
            <sphereGeometry args={[radius, 24, 24]} />
            <meshStandardMaterial color={color} />
        </mesh>
    )
}

function Link({ start, end }: { start: [number, number, number]; end: [number, number, number] }) {
    const { midpoint, length, quaternion } = useMemo(() => {
        const startVec = new THREE.Vector3(...start)
        const endVec = new THREE.Vector3(...end)
        const direction = endVec.clone().sub(startVec)
        const len = direction.length()
        const quat = new THREE.Quaternion().setFromUnitVectors(
            new THREE.Vector3(0, 1, 0),
            direction.clone().normalize(),
        )
        return { midpoint: startVec.add(endVec).multiplyScalar(0.5), length: len, quaternion: quat }
    }, [start, end])

    return (
        <mesh position={midpoint} quaternion={quaternion} castShadow>
            <cylinderGeometry args={[0.06, 0.06, length, 16]} />
            <meshStandardMaterial color="#adb5bd" />
        </mesh>
    )
}
