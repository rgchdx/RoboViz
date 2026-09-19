import { useEffect, useState } from 'react'
import { fetchChainCollision, type ChainCollisionResponse } from '../api/chain'
import type { PlanarChainConfig } from '../types/robot'

interface ChainCollisionState {
    data: ChainCollisionResponse | null
    error: string | null
    loading: boolean
}

/** Refetches the N-link chain self-collision check whenever `config` changes; aborts stale requests. */
export function useChainCollision(config: PlanarChainConfig): ChainCollisionState {
    const [state, setState] = useState<ChainCollisionState>({ data: null, error: null, loading: true })

    useEffect(() => {
        const controller = new AbortController()
        setState((prev) => ({ ...prev, loading: true }))

        fetchChainCollision({ thetas: config.thetas, lengths: config.lengths }, controller.signal)
            .then((data) => setState({ data, error: null, loading: false }))
            .catch((error: unknown) => {
                if (error instanceof DOMException && error.name === 'AbortError') return
                setState({ data: null, error: error instanceof Error ? error.message : String(error), loading: false })
            })

        return () => controller.abort()
    }, [config])

    return state
}
