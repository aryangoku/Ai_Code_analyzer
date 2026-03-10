export default function HotspotTable({ hotspots }) {
  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title mb-4">Complexity hotspots</h2>
        <p className="text-slate-400 text-sm">
          No Python hotspots detected. Try a repository with Python files to see the most complex modules.
        </p>
      </div>
    )
  }

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Complexity hotspots</h2>
      <p className="text-slate-400 text-xs mb-3">
        Top files by cyclomatic complexity × size. These are good candidates for refactoring and extra tests.
      </p>
      <div className="max-h-64 overflow-y-auto rounded-lg border border-slate-700/60 bg-slate-900/40">
        <table className="w-full text-xs">
          <thead className="bg-slate-900/60 text-slate-400 sticky top-0">
            <tr>
              <th className="text-left px-3 py-2 font-medium">File</th>
              <th className="text-right px-3 py-2 font-medium">LOC</th>
              <th className="text-right px-3 py-2 font-medium">Avg CC</th>
              <th className="text-right px-3 py-2 font-medium">Functions</th>
            </tr>
          </thead>
          <tbody>
            {hotspots.map((h) => (
              <tr key={h.path} className="border-t border-slate-800/60">
                <td className="px-3 py-2 font-mono text-slate-200 truncate max-w-[180px]" title={h.path}>
                  {h.path}
                </td>
                <td className="px-3 py-2 text-right text-slate-300">{h.loc}</td>
                <td className="px-3 py-2 text-right text-slate-300">{h.avg_complexity}</td>
                <td className="px-3 py-2 text-right text-slate-400">{h.functions}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}