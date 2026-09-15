import type { ChainForwardKinematicsResponse, ChainJacobianResponse } from '../api/chain'

interface ChainInfoPanelProps {
    forwardData: ChainForwardKinematicsResponse | null
    jacobianData: ChainJacobianResponse | null
    loading: boolean
    error: string | null
}

/** Displays end-effector position, manipulability, and singularity status for an N-link chain. */
export function ChainInfoPanel({ forwardData, jacobianData, loading, error }: ChainInfoPanelProps) {
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
        </div>
    )
}
