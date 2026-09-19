import { useCallback, useState } from 'react'
import { fetchChainInverseKinematics, type ChainInverseKinematicsResponse } from '../api/chain'

interface ChainInverseKinematicsState {
    data: ChainInverseKinematicsResponse | null
    error: string | null
    loading: boolean
}

interface SolveArgs {
    x: number
    y: number
    lengths: number[]
    initialThetas?: number[]
}

/** Imperative "solve on demand" IK hook: unlike the other chain hooks, this doesn't
 * auto-refetch on config change. Call `solve(...)` explicitly, e.g. from a click handler.
 */
export function useChainInverseKinematics() {
    const [state, setState] = useState<ChainInverseKinematicsState>({ data: null, error: null, loading: false })

    const solve = useCallback(async ({ x, y, lengths, initialThetas }: SolveArgs) => {
        setState((prev) => ({ ...prev, loading: true }))
        try {
            const data = await fetchChainInverseKinematics({
                x,
                y,
                lengths,
                initial_thetas: initialThetas ?? null,
            })
            setState({ data, error: null, loading: false })
            return data
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : String(error)
            setState({ data: null, error: message, loading: false })
            return null
        }
    }, [])

    return { ...state, solve }
}
