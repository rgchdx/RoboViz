// This module defines a custom React hook for fetching the forward kinematics of a 2R planar robotic arm from the backend.
import { useEffect, useState } from 'react'
import { fetchForwardKinematics, type ForwardKinematicsResponse } from '../api/kinematics'
import type { PlanarArmConfig } from '../types/robot'

interface ForwardKinematicsState {
    data: ForwardKinematicsResponse | null
    error: string | null
    loading: boolean
}

/** Refetches forward kinematics from the backend whenever `config` changes; aborts stale requests. */
export function useForwardKinematics(config: PlanarArmConfig): ForwardKinematicsState {
    const [state, setState] = useState<ForwardKinematicsState>({ data: null, error: null, loading: true })

    useEffect(() => {
        const controller = new AbortController()
        const [l1, l2] = config.linkLengths
        const [theta1, theta2] = config.jointAngles

        setState((prev) => ({ ...prev, loading: true }))

        fetchForwardKinematics({ theta1, theta2, l1, l2 }, controller.signal)
            .then((data) => setState({ data, error: null, loading: false }))
            .catch((error: unknown) => {
                if (error instanceof DOMException && error.name === 'AbortError') return
                setState({ data: null, error: error instanceof Error ? error.message : String(error), loading: false })
            })

        return () => controller.abort()
    }, [config])

    return state
}
