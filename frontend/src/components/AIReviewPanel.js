function AIReviewPanel({ aiReview }) {
  if (!aiReview) return null

  if (aiReview.error) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title mb-3">AI Architecture Review</h2>
        <p className="text-sm text-amber-400/80">{aiReview.error}</p>
      </div>
    )
  }

  const sections = [
    {
      key: "strengths",
      label: "Strengths",
      icon: "\u2705",
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/20",
    },
    {
      key: "concerns",
      label: "Concerns",
      icon: "\u26A0\uFE0F",
      color: "text-amber-400",
      bg: "bg-amber-500/10 border-amber-500/20",
    },
    {
      key: "suggestions",
      label: "Suggestions",
      icon: "\uD83D\uDCA1",
      color: "text-sky-400",
      bg: "bg-sky-500/10 border-sky-500/20",
    },
  ]

  const hasContent = sections.some(
    (s) => aiReview[s.key] && aiReview[s.key].length > 0
  )
  if (!hasContent) return null

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">
        <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 to-indigo-400">
          AI Architecture Review
        </span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sections.map((section) => {
          const items = aiReview[section.key] || []
          if (items.length === 0) return null
          return (
            <div
              key={section.key}
              className={`rounded-xl border p-4 ${section.bg}`}
            >
              <h3 className={`text-sm font-semibold mb-3 ${section.color}`}>
                {section.icon} {section.label}
              </h3>
              <ul className="space-y-2">
                {items.map((item, i) => (
                  <li
                    key={i}
                    className="text-xs text-slate-300 leading-relaxed pl-3 border-l-2 border-slate-600/50"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default AIReviewPanel
