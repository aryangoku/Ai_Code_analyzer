import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts"

export default function LanguageChart({ languages }) {
  const entries = Object.entries(languages || {})
  if (!entries.length) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title mb-4">Languages</h2>
        <p className="text-slate-400 text-sm">No language data available for this repository.</p>
      </div>
    )
  }

  const total = entries.reduce((sum, [, v]) => sum + (v || 0), 0)
  const data = entries.map(([name, value]) => ({
    name,
    value,
    percent: total ? ((value / total) * 100).toFixed(1) : 0,
  }))

  const COLORS = ["#6366f1", "#22c55e", "#eab308", "#f97316", "#ec4899", "#06b6d4", "#a855f7"]

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Languages</h2>
      <div className="flex items-center gap-6">
        <div className="w-40 h-40">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                innerRadius={40}
                outerRadius={70}
                paddingAngle={2}
              >
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(_, name, props) => [
                  `${props?.payload?.percent ?? "0.0"}%`,
                  name,
                ]}
                contentStyle={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: 8 }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <ul className="flex-1 space-y-1 text-xs">
          {data.map((d, i) => (
            <li key={d.name} className="flex items-center gap-2 text-slate-300">
              <span
                className="inline-block w-2.5 h-2.5 rounded-full"
                style={{ backgroundColor: COLORS[i % COLORS.length] }}
              />
              <span className="font-medium">{d.name}</span>
              <span className="text-slate-400 ml-auto tabular-nums">{d.percent}%</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}