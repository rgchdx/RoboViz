import type { ForwardKinematicsResponse } from '../api/kinematics'

interface InfoPanelProps {
    data: ForwardKinematicsResponse | null
    loading: boolean
    error: string | null
}

/** Displays the end-effector position and cumulative transform returned by the backend. */
export function InfoPanel({ data, loading, error }: InfoPanelProps) {
    if (error) {
        return <div className="info-panel info-panel--error">Backend error: {error}</div>
    }

    if (!data) {
        return <div className="info-panel">{loading ? 'Solving forward kinematics…' : 'No data'}</div>
    }

    return (
        <div className="info-panel">
            <h3>End effector</h3>
            <p>
                x: {data.end_effector.x.toFixed(3)}, y: {data.end_effector.y.toFixed(3)}
            </p>
            <h3>T02 (base → end effector)</h3>
            <MatrixTable matrix={data.t02} />
        </div>
    )
}

function MatrixTable({ matrix }: { matrix: number[][] }) {
    return (
        <table>
            <tbody>
                {matrix.map((row, i) => (
                    <tr key={i}>
                        {row.map((cell, j) => (
                            <td key={j}>{cell.toFixed(3)}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    )
}
