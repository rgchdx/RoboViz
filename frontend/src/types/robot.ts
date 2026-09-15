// This module defines TypeScript types and default configurations for the 2R planar robotic arm.
/** Configuration for the planar 2-revolute-joint arm (see docs/architecture.md). */
export interface PlanarArmConfig {
    /** Link lengths [L1, L2] in scene units. */
    linkLengths: [number, number]
    /** Joint angles [theta1, theta2] in radians. */
    jointAngles: [number, number]
}

export const DEFAULT_PLANAR_ARM_CONFIG: PlanarArmConfig = {
    linkLengths: [2, 1.5],
    jointAngles: [Math.PI / 6, -Math.PI / 4],
}

/** Configuration for an N-link planar chain, generalizing PlanarArmConfig (see robotics/chain.py). */
export interface PlanarChainConfig {
    /** Link lengths, base to tip. */
    lengths: number[]
    /** Joint angles in radians, base to tip. */
    thetas: number[]
}

export const DEFAULT_PLANAR_CHAIN_CONFIG: PlanarChainConfig = {
    lengths: [2, 1.5, 1],
    thetas: [Math.PI / 6, -Math.PI / 4, Math.PI / 8],
}
