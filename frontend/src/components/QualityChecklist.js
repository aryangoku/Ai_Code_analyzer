function QualityItem({ label, ok }) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-slate-300">{label}</span>
      <span
        className={`px-2 py-0.5 rounded-full text-xs font-medium ${
          ok
            ? "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30"
            : "bg-slate-800 text-slate-400 border border-slate-600/60"
        }`}
      >
        {ok ? "Good" : "Missing"}
      </span>
    </div>
  )
}

export default function QualityChecklist({ quality }) {
  if (!quality) return null

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-3">Repository quality checklist</h2>
      <p className="text-slate-400 text-xs mb-4">
        Quick view of docs, licensing, tests, CI, and recent activity.
      </p>
      <div className="space-y-2.5">
        <QualityItem label="README" ok={quality.readme} />
        <QualityItem label="License" ok={quality.license} />
        <QualityItem label="Tests folder" ok={quality.tests} />
        <QualityItem label="CI workflow (.github/workflows)" ok={quality.ci} />
        <QualityItem label="Recent commits (last ~3 months)" ok={quality.recent_activity} />
      </div>
    </div>
  )
}

