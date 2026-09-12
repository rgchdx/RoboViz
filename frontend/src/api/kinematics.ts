/** Typed client for the RoboViz kinematics API (see backend/app/models/kinematics.py). */

export interface Point2D {
    x: number
    y: number
}

export interface ForwardKinematicsRequest {
    theta1: number
    theta2: number
    l1: number
    l2: number
}

export interface ForwardKinematicsResponse {
    joint1: Point2D
    end_effector: Point2D
    t01: number[][]
    t02: number[][]
}

const API_BASE = '/api'

export async function fetchForwardKinematics(
    request: ForwardKinematicsRequest,
    signal?: AbortSignal,
): Promise<ForwardKinematicsResponse> {
    const response = await fetch(`${API_BASE}/kinematics/forward`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal,
    })

    if (!response.ok) {
        const detail = await response.text()
        throw new Error(`Forward kinematics request failed (${response.status}): ${detail}`)
    }

    return response.json() as Promise<ForwardKinematicsResponse>
}
