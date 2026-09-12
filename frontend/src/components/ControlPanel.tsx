// This module defines a React component for controlling the parameters of a 2R planar robotic arm via sliders.
import type { PlanarArmConfig } from '../types/robot'

interface ControlPanelProps {
    config: PlanarArmConfig
    onChange: (config: PlanarArmConfig) => void
}

/** Sliders for link lengths and joint angles; values are sent to the backend as FK input. */
export function ControlPanel({ config, onChange }: ControlPanelProps) {
    const [l1, l2] = config.linkLengths
    const [theta1, theta2] = config.jointAngles

    const update = (partial: Partial<{ l1: number; l2: number; theta1: number; theta2: number }>) => {
        onChange({
            linkLengths: [partial.l1 ?? l1, partial.l2 ?? l2],
            jointAngles: [partial.theta1 ?? theta1, partial.theta2 ?? theta2],
        })
    }

    return (
        <div className="control-panel">
            <h2>2R Planar Arm</h2>
            <Slider label="Link 1 length" value={l1} min={0.5} max={4} step={0.1} onChange={(v) => update({ l1: v })} />
            <Slider label="Link 2 length" value={l2} min={0.5} max={4} step={0.1} onChange={(v) => update({ l2: v })} />
            <Slider label="Joint 1 angle" value={theta1} min={-Math.PI} max={Math.PI} step={0.01} unit=" rad" onChange={(v) => update({ theta1: v })} />
            <Slider label="Joint 2 angle" value={theta2} min={-Math.PI} max={Math.PI} step={0.01} unit=" rad" onChange={(v) => update({ theta2: v })} />
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
