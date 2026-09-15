import { useEffect, useState } from 'react'
import { fetchChainJacobian, type ChainJacobianResponse } from '../api/chain'
import type { PlanarChainConfig } from '../types/robot'

interface ChainJacobianState {
    data: ChainJacobianResponse | null
    error: string | null
    loading: boolean
}

/** Refetches the N-link chain Jacobian/manipulability whenever `config` changes; aborts stale requests. */
export function useChainJacobian(config: PlanarChainConfig): ChainJacobianState {
    const [state, setState] = useState<ChainJacobianState>({ data: null, error: null, loading: true })

    useEffect(() => {
        const controller = new AbortController()
        setState((prev) => ({ ...prev, loading: true }))

        fetchChainJacobian({ thetas: config.thetas, lengths: config.lengths }, controller.signal)
            .then((data) => setState({ data, error: null, loading: false }))
            .catch((error: unknown) => {
                if (error instanceof DOMException && error.name === 'AbortError') return
                setState({ data: null, error: error instanceof Error ? error.message : String(error), loading: false })
            })

        return () => controller.abort()
    }, [config])

    return state
}
