import { useEffect, useState } from 'react'
import { fetchChainForwardKinematics, type ChainForwardKinematicsResponse } from '../api/chain'
import type { PlanarChainConfig } from '../types/robot'

interface ChainForwardKinematicsState {
    data: ChainForwardKinematicsResponse | null
    error: string | null
    loading: boolean
}

/** Refetches N-link chain forward kinematics whenever `config` changes; aborts stale requests. */
export function useChainForwardKinematics(config: PlanarChainConfig): ChainForwardKinematicsState {
    const [state, setState] = useState<ChainForwardKinematicsState>({ data: null, error: null, loading: true })

    useEffect(() => {
        const controller = new AbortController()
        setState((prev) => ({ ...prev, loading: true }))

        fetchChainForwardKinematics({ thetas: config.thetas, lengths: config.lengths }, controller.signal)
            .then((data) => setState({ data, error: null, loading: false }))
            .catch((error: unknown) => {
                if (error instanceof DOMException && error.name === 'AbortError') return
                setState({ data: null, error: error instanceof Error ? error.message : String(error), loading: false })
            })

        return () => controller.abort()
    }, [config])

    return state
}
