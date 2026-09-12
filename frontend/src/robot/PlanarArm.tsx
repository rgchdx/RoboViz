import { useMemo } from 'react'
import * as THREE from 'three'

interface PlanarArmProps {
    joint1: [number, number]
    endEffector: [number, number]
}

/** Renders the 2R planar arm from joint/end-effector positions solved by the backend. */
export function PlanarArm({ joint1, endEffector }: PlanarArmProps) {
    const joint1Position: [number, number, number] = [joint1[0], joint1[1], 0]
    const endEffectorPosition: [number, number, number] = [endEffector[0], endEffector[1], 0]

    return (
        <group>
            <Joint position={[0, 0, 0]} color="#ff6b6b" />
            <Link start={[0, 0, 0]} end={joint1Position} />
            <Joint position={joint1Position} color="#4dabf7" />
            <Link start={joint1Position} end={endEffectorPosition} />
            <Joint position={endEffectorPosition} color="#69db7c" radius={0.08} />
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
