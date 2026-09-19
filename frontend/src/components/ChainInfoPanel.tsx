import type { ChainCollisionResponse, ChainForwardKinematicsResponse, ChainJacobianResponse } from '../api/chain'

interface ChainInfoPanelProps {
    forwardData: ChainForwardKinematicsResponse | null
    jacobianData: ChainJacobianResponse | null
    collisionData: ChainCollisionResponse | null
    loading: boolean
    error: string | null
    /** Status message from the last click-to-target IK solve, if any. */
    targetMessage?: string | null
}

/** Displays end-effector position, manipulability, singularity, and self-collision status for an N-link chain. */
export function ChainInfoPanel({
    forwardData,
    jacobianData,
    collisionData,
    loading,
    error,
    targetMessage,
}: ChainInfoPanelProps) {
    if (error) {
        return <div className="info-panel info-panel--error">Backend error: {error}</div>
    }

    if (!forwardData) {
        return <div className="info-panel">{loading ? 'Solving forward kinematics…' : 'No data'}</div>
    }

    return (
        <div className="info-panel">
            <h3>End effector</h3>
            <p>
                x: {forwardData.end_effector.x.toFixed(3)}, y: {forwardData.end_effector.y.toFixed(3)}
            </p>
            {jacobianData && (
                <>
                    <h3>Manipulability</h3>
                    <p className={jacobianData.is_singular ? 'info-panel--error' : undefined}>
                        {jacobianData.manipulability.toFixed(4)}
                        {jacobianData.is_singular && ' (near singular)'}
                    </p>
                </>
            )}
            {collisionData?.has_self_collision && (
                <>
                    <h3>Self-collision</h3>
                    <p className="info-panel--error">
                        Links {collisionData.colliding_pairs.map(([i, j]) => `${i + 1}-${j + 1}`).join(', ')} overlap
                    </p>
                </>
            )}
            {targetMessage && (
                <>
                    <h3>Last target</h3>
                    <p className="info-panel--error">{targetMessage}</p>
                </>
            )}
        </div>
    )
}
