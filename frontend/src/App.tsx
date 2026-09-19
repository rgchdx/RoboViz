// This module defines the main React application: a 2R arm and an N-link chain, switchable via a toggle.
import { useState } from 'react'
import { Scene } from './visualization/Scene'
import { PlanarArm } from './robot/PlanarArm'
import { RobotArm } from './robot/RobotArm'
import { ControlPanel } from './components/ControlPanel'
import { ChainControlPanel } from './components/ChainControlPanel'
import { InfoPanel } from './components/InfoPanel'
import { ChainInfoPanel } from './components/ChainInfoPanel'
import { useForwardKinematics } from './hooks/useForwardKinematics'
import { useChainForwardKinematics } from './hooks/useChainForwardKinematics'
import { useChainJacobian } from './hooks/useChainJacobian'
import { useChainInverseKinematics } from './hooks/useChainInverseKinematics'
import {
    DEFAULT_PLANAR_ARM_CONFIG,
    DEFAULT_PLANAR_CHAIN_CONFIG,
    type PlanarArmConfig,
    type PlanarChainConfig,
} from './types/robot'
import './App.css'

type Mode = '2r' | 'chain'

function App() {
    const [mode, setMode] = useState<Mode>('2r')

    const [armConfig, setArmConfig] = useState<PlanarArmConfig>(DEFAULT_PLANAR_ARM_CONFIG)
    const armFk = useForwardKinematics(armConfig)

    const [chainConfig, setChainConfig] = useState<PlanarChainConfig>(DEFAULT_PLANAR_CHAIN_CONFIG)
    const chainFk = useChainForwardKinematics(chainConfig)
    const chainJacobian = useChainJacobian(chainConfig)
    const chainIk = useChainInverseKinematics()
    const [targetMessage, setTargetMessage] = useState<string | null>(null)

    const handleTargetClick = async ({ x, y }: { x: number; y: number }) => {
        const result = await chainIk.solve({ x, y, lengths: chainConfig.lengths, initialThetas: chainConfig.thetas })
        if (!result) return

        if (result.reachable && result.thetas) {
            setChainConfig({ ...chainConfig, thetas: result.thetas })
            setTargetMessage(null)
        } else {
            setTargetMessage(result.message ?? 'Target unreachable.')
        }
    }

    return (
        <div className="app">
            <Scene onTargetClick={mode === 'chain' ? handleTargetClick : undefined}>
                {mode === '2r' && armFk.data && (
                    <PlanarArm
                        joint1={[armFk.data.joint1.x, armFk.data.joint1.y]}
                        endEffector={[armFk.data.end_effector.x, armFk.data.end_effector.y]}
                    />
                )}
                {mode === 'chain' && chainFk.data && <RobotArm jointPositions={chainFk.data.joint_positions} />}
            </Scene>

            <div className="mode-toggle">
                <button className={mode === '2r' ? 'active' : ''} onClick={() => setMode('2r')} type="button">
                    2R Arm
                </button>
                <button className={mode === 'chain' ? 'active' : ''} onClick={() => setMode('chain')} type="button">
                    N-Link Chain
                </button>
            </div>

            {mode === 'chain' && <p className="target-hint">Click anywhere in the scene to move the arm there.</p>}

            {mode === '2r' ? (
                <>
                    <ControlPanel config={armConfig} onChange={setArmConfig} />
                    <InfoPanel data={armFk.data} loading={armFk.loading} error={armFk.error} />
                </>
            ) : (
                <>
                    <ChainControlPanel config={chainConfig} onChange={setChainConfig} />
                    <ChainInfoPanel
                        forwardData={chainFk.data}
                        jacobianData={chainJacobian.data}
                        loading={chainFk.loading}
                        error={chainFk.error}
                        targetMessage={targetMessage}
                    />
                </>
            )}
        </div>
    )
}

export default App
