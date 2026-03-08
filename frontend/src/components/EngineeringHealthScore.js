import { useMemo } from "react"

const DIMENSIONS = [
  { key: "overall", label: "Overall", color: "text-indigo-400" },
  { key: "complexity_score", label: "Complexity", color: "text-amber-400" },
  { key: "risk_score", label: "Risk", color: "text-emerald-400" },
  { key: "security_score", label: "Security", color: "text-rose-400" },
  { key: "activity_score", label: "Activity", color: "text-cyan-400" },
]

function EngineeringHealthScore({ engineeringHealth }) {
  const data = useMemo(() => {
    if (!engineeringHealth) return []
    return DIMENSIONS.map((d) => ({
      ...d,
      value: engineeringHealth[d.key] ?? 0,
    }))
  }, [engineeringHealth])

  if (!data.length) return null

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Engineering health score</h2>
      <div className="space-y-3">
        {data.map(({ key, label, value, color }) => (
          <div key={key}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-400">{label}</span>
              <span className={color}>{Math.round(value)}/100</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  value >= 70 ? "bg-emerald-500" : value >= 40 ? "bg-amber-500" : "bg-rose-500"
                }`}
                style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default EngineeringHealthScore
