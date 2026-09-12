import { useState } from 'react'
import { Scene } from './visualization/Scene'
import { ControlPanel } from './components/ControlPanel'
import { InfoPanel } from './components/InfoPanel'
import { useForwardKinematics } from './hooks/useForwardKinematics'
import { DEFAULT_PLANAR_ARM_CONFIG, type PlanarArmConfig } from './types/robot'
import './App.css'

function App() {
    const [config, setConfig] = useState<PlanarArmConfig>(DEFAULT_PLANAR_ARM_CONFIG)
    const { data, loading, error } = useForwardKinematics(config)

    return (
        <div className="app">
            {data && (
                <Scene joint1={[data.joint1.x, data.joint1.y]} endEffector={[data.end_effector.x, data.end_effector.y]} />
            )}
            <ControlPanel config={config} onChange={setConfig} />
            <InfoPanel data={data} loading={loading} error={error} />
        </div>
    )
}

export default App
