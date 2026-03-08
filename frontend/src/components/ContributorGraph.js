import { useMemo } from "react"
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts"

const BAR_COLORS = ["#6366f1", "#8b5cf6", "#a855f7", "#c084fc", "#d8b4fe", "#e9d5ff", "#a5b4fc", "#818cf8", "#6366f1", "#4f46e5"]

function ContributorGraph({ contributors }) {
  const data = useMemo(() => {
    if (!contributors || !contributors.length) return []
    return contributors.slice(0, 10).map((c) => ({
      login: (c.login || "?").trim().replace(/^:+/, ""),
      name: (c.login || "?").trim().replace(/^:+/, ""),
      contributions: c.contributions || 0,
      avatar_url: c.avatar_url,
    }))
  }, [contributors])

  if (!data.length) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title">Top contributors</h2>
        <p className="text-slate-400 text-sm">No contributor data available.</p>
      </div>
    )
  }

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Top contributors</h2>
      <div className="flex gap-3 mb-4 flex-wrap">
        {data.map((c, i) => (
          <a
            key={c.login}
            href={`https://github.com/${c.login}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-slate-700/60 hover:bg-slate-600/60 transition-colors group"
          >
            <img
              src={c.avatar_url}
              alt=""
              className="w-7 h-7 rounded-full ring-2 ring-slate-600 group-hover:ring-indigo-500/50"
            />
            <span className="text-sm font-medium text-slate-200 group-hover:text-white truncate max-w-[100px]" title={c.login}>{c.login}</span>
            <span className="text-xs text-slate-500 tabular-nums">{c.contributions}</span>
          </a>
        ))}
      </div>
      <div className="h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 0, right: 24, top: 4, bottom: 4 }}>
            <XAxis type="number" stroke="#64748b" tick={{ fontSize: 11 }} />
            <YAxis
              type="category"
              dataKey="name"
              width={120}
              stroke="#64748b"
              tick={{ fontSize: 12, fill: "#94a3b8" }}
              tickFormatter={(v) => (v && v.length > 14 ? `${v.slice(0, 12)}…` : v) || "?"}
            />
            <Tooltip
              contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
              formatter={(v) => [`${v} commits`, "Contributions"]}
              labelFormatter={(label) => `@${label}`}
            />
            <Bar dataKey="contributions" radius={[0, 4, 4, 0]} minPointSize={4}>
              {data.map((_, i) => (
                <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default ContributorGraph
