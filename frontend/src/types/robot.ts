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
