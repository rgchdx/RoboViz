import { useMemo } from 'react'
import * as THREE from 'three'
import { DEFAULT_PLANAR_ARM_CONFIG, type PlanarArmConfig } from '../types/robot'

/** Static placeholder rendering of the 2R planar arm; joint sliders arrive in a later phase. */
export function PlanarArm({ config = DEFAULT_PLANAR_ARM_CONFIG }: { config?: PlanarArmConfig }) {
    const { linkLengths, jointAngles } = config
    const [l1, l2] = linkLengths
    const [theta1, theta2] = jointAngles

    const joint1Position = useMemo<[number, number, number]>(
        () => [l1 * Math.cos(theta1), l1 * Math.sin(theta1), 0],
        [l1, theta1],
    )
    const endEffectorPosition = useMemo<[number, number, number]>(() => {
        const combined = theta1 + theta2
        return [joint1Position[0] + l2 * Math.cos(combined), joint1Position[1] + l2 * Math.sin(combined), 0]
    }, [joint1Position, l2, theta1, theta2])

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
