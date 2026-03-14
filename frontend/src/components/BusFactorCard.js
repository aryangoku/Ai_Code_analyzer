function BusFactorCard({ busFactor }) {
  if (!busFactor || busFactor.bus_factor === 0) return null

  const bf = busFactor.bus_factor
  let riskLevel, riskColor, riskBg
  if (bf <= 1) {
    riskLevel = "Critical"
    riskColor = "text-red-400"
    riskBg = "bg-red-500/20 border-red-500/30"
  } else if (bf <= 2) {
    riskLevel = "High"
    riskColor = "text-orange-400"
    riskBg = "bg-orange-500/20 border-orange-500/30"
  } else if (bf <= 4) {
    riskLevel = "Moderate"
    riskColor = "text-amber-400"
    riskBg = "bg-amber-500/20 border-amber-500/30"
  } else {
    riskLevel = "Low"
    riskColor = "text-emerald-400"
    riskBg = "bg-emerald-500/20 border-emerald-500/30"
  }

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Bus Factor</h2>

      <div className="flex items-center gap-4 mb-4">
        <div className="text-4xl font-bold text-white">{bf}</div>
        <div>
          <span
            className={`text-xs font-semibold px-2 py-1 rounded-md border ${riskBg} ${riskColor}`}
          >
            {riskLevel} Risk
          </span>
          <p className="text-xs text-slate-400 mt-1">
            {bf === 1
              ? "Only 1 person holds 50%+ of contributions"
              : `${bf} people account for 50%+ of contributions`}
          </p>
        </div>
      </div>

      {busFactor.top_contributors && busFactor.top_contributors.length > 0 && (
        <div className="space-y-2">
          {busFactor.top_contributors.map((c, i) => (
            <div key={i} className="flex items-center gap-3">
              <span className="text-xs text-slate-400 w-4">{i + 1}.</span>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm text-white font-medium">
                    {c.login}
                  </span>
                  <span className="text-xs text-slate-400">
                    {c.contributions} commits ({c.cumulative_pct}%)
                  </span>
                </div>
                <div className="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all"
                    style={{ width: `${c.cumulative_pct}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <p className="text-xs text-slate-500 mt-3">
        Total: {busFactor.total_contributions.toLocaleString()} contributions
      </p>
    </div>
  )
}

export default BusFactorCard
