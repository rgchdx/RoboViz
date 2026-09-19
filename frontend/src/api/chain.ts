/** Typed client for the RoboViz N-link chain API (see backend/app/models/chain.py). */

import type { Point2D } from './kinematics'

export interface PlanarChainRequest {
    thetas: number[]
    lengths: number[]
}

export interface ChainForwardKinematicsResponse {
    joint_positions: Point2D[]
    end_effector: Point2D
}

export interface ChainJacobianResponse {
    matrix: number[][]
    manipulability: number
    is_singular: boolean
}

const API_BASE = '/api'

export async function fetchChainForwardKinematics(
    request: PlanarChainRequest,
    signal?: AbortSignal,
): Promise<ChainForwardKinematicsResponse> {
    const response = await fetch(`${API_BASE}/chain/forward`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal,
    })

    if (!response.ok) {
        const detail = await response.text()
        throw new Error(`Chain forward kinematics request failed (${response.status}): ${detail}`)
    }

    return response.json() as Promise<ChainForwardKinematicsResponse>
}

export async function fetchChainJacobian(
    request: PlanarChainRequest,
    signal?: AbortSignal,
): Promise<ChainJacobianResponse> {
    const response = await fetch(`${API_BASE}/chain/jacobian`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal,
    })

    if (!response.ok) {
        const detail = await response.text()
        throw new Error(`Chain Jacobian request failed (${response.status}): ${detail}`)
    }

    return response.json() as Promise<ChainJacobianResponse>
}

export interface ChainInverseKinematicsRequest {
    x: number
    y: number
    lengths: number[]
    initial_thetas?: number[] | null
}

export interface ChainInverseKinematicsResponse {
    reachable: boolean
    thetas: number[] | null
    iterations: number
    final_error: number
    message: string | null
}

export async function fetchChainInverseKinematics(
    request: ChainInverseKinematicsRequest,
    signal?: AbortSignal,
): Promise<ChainInverseKinematicsResponse> {
    const response = await fetch(`${API_BASE}/chain/inverse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal,
    })

    if (!response.ok) {
        const detail = await response.text()
        throw new Error(`Chain inverse kinematics request failed (${response.status}): ${detail}`)
    }

    return response.json() as Promise<ChainInverseKinematicsResponse>
}

export interface ChainCollisionResponse {
    has_self_collision: boolean
    colliding_pairs: [number, number][]
}

export async function fetchChainCollision(
    request: PlanarChainRequest,
    signal?: AbortSignal,
): Promise<ChainCollisionResponse> {
    const response = await fetch(`${API_BASE}/chain/collision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal,
    })

    if (!response.ok) {
        const detail = await response.text()
        throw new Error(`Chain collision check failed (${response.status}): ${detail}`)
    }

    return response.json() as Promise<ChainCollisionResponse>
}
