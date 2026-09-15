import type { PlanarChainConfig } from '../types/robot'

interface ChainControlPanelProps {
    config: PlanarChainConfig
    onChange: (config: PlanarChainConfig) => void
}

/** Dynamic sliders for an N-link chain's angles/lengths, plus add/remove link controls
 * (generalizes components/ControlPanel.tsx from exactly 2 links to N).
 */
export function ChainControlPanel({ config, onChange }: ChainControlPanelProps) {
    const updateTheta = (index: number, value: number) => {
        const thetas = [...config.thetas]
        thetas[index] = value
        onChange({ ...config, thetas })
    }

    const updateLength = (index: number, value: number) => {
        const lengths = [...config.lengths]
        lengths[index] = value
        onChange({ ...config, lengths })
    }

    const addLink = () => {
        onChange({
            thetas: [...config.thetas, 0],
            lengths: [...config.lengths, 1],
        })
    }

    const removeLink = (index: number) => {
        if (config.thetas.length <= 1) return
        onChange({
            thetas: config.thetas.filter((_, i) => i !== index),
            lengths: config.lengths.filter((_, i) => i !== index),
        })
    }

    return (
        <div className="control-panel">
            <h2>N-Link Planar Chain</h2>
            {config.thetas.map((theta, i) => (
                <div className="chain-link-row" key={i}>
                    <Slider
                        label={`Joint ${i + 1} angle`}
                        value={theta}
                        min={-Math.PI}
                        max={Math.PI}
                        step={0.01}
                        unit=" rad"
                        onChange={(v) => updateTheta(i, v)}
                    />
                    <Slider
                        label={`Link ${i + 1} length`}
                        value={config.lengths[i]}
                        min={0.5}
                        max={4}
                        step={0.1}
                        onChange={(v) => updateLength(i, v)}
                    />
                    <button
                        type="button"
                        className="remove-link-button"
                        onClick={() => removeLink(i)}
                        disabled={config.thetas.length <= 1}
                    >
                        Remove link
                    </button>
                </div>
            ))}
            <button type="button" onClick={addLink}>
                Add link
            </button>
        </div>
    )
}

function Slider({
    label,
    value,
    min,
    max,
    step,
    unit = '',
    onChange,
}: {
    label: string
    value: number
    min: number
    max: number
    step: number
    unit?: string
    onChange: (value: number) => void
}) {
    return (
        <label className="control-slider">
            <span>
                {label}: {value.toFixed(2)}
                {unit}
            </span>
            <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} />
        </label>
    )
}
