import { useMemo } from "react"

const DAY_LABELS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
const CELL_SIZE = 12
const GAP = 3

function CommitHeatmap({ commitActivity }) {
  const { grid, maxCount, totalCommits } = useMemo(() => {
    if (!commitActivity || !commitActivity.length) return { grid: [], maxCount: 1, totalCommits: 0 }
    const weeks = commitActivity.slice(-52)
    const byDay = []
    let total = 0
    for (let d = 0; d < 7; d++) {
      byDay[d] = []
      for (let w = 0; w < weeks.length; w++) {
        const dayCount = weeks[w].days?.[d] ?? 0
        total += dayCount
        byDay[d].push(dayCount)
      }
    }
    let max = 1
    byDay.forEach((row) => row.forEach((v) => { if (v > max) max = v }))
    return { grid: byDay, maxCount: max, totalCommits: total }
  }, [commitActivity])

  const getLevel = (count) => {
    if (count === 0) return 0
    if (maxCount <= 0) return 1
    const ratio = count / maxCount
    if (ratio <= 0.25) return 1
    if (ratio <= 0.5) return 2
    if (ratio <= 0.75) return 3
    return 4
  }

  if (!grid.length) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title">Commit activity</h2>
        <p className="text-slate-400 text-sm">No commit data (repo may be computing stats).</p>
      </div>
    )
  }

  return (
    <div className="dashboard-card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="card-title">Commit heatmap</h2>
        <span className="text-sm text-slate-400">{totalCommits.toLocaleString()} commits last year</span>
      </div>
      <div className="flex gap-4 items-start overflow-x-auto pb-2">
        <div className="flex flex-col justify-between text-xs text-slate-500 shrink-0 pt-0.5" style={{ height: 7 * CELL_SIZE + 6 * GAP }}>
          {DAY_LABELS.map((l) => (
            <span key={l} style={{ height: CELL_SIZE, lineHeight: `${CELL_SIZE}px` }}>{l}</span>
          ))}
        </div>
        <div className="flex flex-col gap-[3px] shrink-0">
          {grid.map((row, d) => (
            <div key={d} className="flex gap-[3px]" style={{ height: CELL_SIZE }}>
              {row.map((count, w) => {
                const level = getLevel(count)
                return (
                  <div
                    key={w}
                    title={`${count} commit${count !== 1 ? "s" : ""}`}
                    className="rounded-[2px] flex-shrink-0 transition-all duration-150 hover:ring-2 hover:ring-emerald-400/50 hover:ring-offset-1 hover:ring-offset-slate-800"
                    style={{
                      width: CELL_SIZE,
                      height: CELL_SIZE,
                      backgroundColor:
                        level === 0 ? "rgb(30 41 59)" :
                        level === 1 ? "rgb(34 197 94 / 0.4)" :
                        level === 2 ? "rgb(34 197 94 / 0.65)" :
                        level === 3 ? "rgb(34 197 94 / 0.85)" :
                        "rgb(34 197 94)",
                    }}
                  />
                )
              })}
            </div>
          ))}
        </div>
      </div>
      <div className="flex items-center gap-2 mt-4">
        <span className="text-xs text-slate-500">Less</span>
        <div className="flex gap-0.5">
          {[0, 1, 2, 3, 4].map((level) => (
            <div
              key={level}
              className="rounded-[2px]"
              style={{
                width: 10,
                height: 10,
                backgroundColor:
                  level === 0 ? "rgb(30 41 59)" :
                  level === 1 ? "rgb(34 197 94 / 0.4)" :
                  level === 2 ? "rgb(34 197 94 / 0.65)" :
                  level === 3 ? "rgb(34 197 94 / 0.85)" :
                  "rgb(34 197 94)",
              }}
            />
          ))}
        </div>
        <span className="text-xs text-slate-500">More</span>
      </div>
    </div>
  )
}

export default CommitHeatmap
