import { useMemo } from "react"

function DependencyGraph({ dependencyGraph }) {
  const { nodes, edges } = useMemo(() => {
    if (!dependencyGraph || !dependencyGraph.nodes) {
      return { nodes: [], edges: [] }
    }
    return {
      nodes: dependencyGraph.nodes || [],
      edges: dependencyGraph.edges || [],
    }
  }, [dependencyGraph])

  if (nodes.length === 0) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title mb-4">Dependency graph</h2>
        <p className="text-slate-400 text-sm">No Python modules / imports detected.</p>
      </div>
    )
  }

  return (
    <div className="bg-slate-800 p-6 rounded-xl">
      <h2 className="card-title mb-4">Dependency graph (Python imports)</h2>
      <div className="flex flex-wrap gap-2 mb-3">
        {nodes.slice(0, 20).map((n) => (
          <span
            key={n.id}
            className="px-2 py-1 rounded bg-slate-700 text-slate-200 text-xs font-mono"
          >
            {n.label || n.id}
          </span>
        ))}
        {nodes.length > 20 && (
          <span className="text-slate-500 text-xs">+{nodes.length - 20} more</span>
        )}
      </div>
      <div className="max-h-48 overflow-y-auto border border-slate-600 rounded-lg p-3 bg-slate-900/50">
        <table className="text-xs w-full">
          <thead>
            <tr className="text-slate-500 border-b border-slate-600">
              <th className="text-left py-1">From</th>
              <th className="text-left py-1">→</th>
              <th className="text-left py-1">To</th>
            </tr>
          </thead>
          <tbody>
            {edges.slice(0, 50).map((e, i) => (
              <tr key={i} className="border-b border-slate-700/50">
                <td className="py-1 font-mono text-slate-300">{e.source}</td>
                <td className="py-1 text-slate-500">→</td>
                <td className="py-1 font-mono text-indigo-300">{e.target}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {edges.length > 50 && (
          <p className="text-slate-500 text-xs mt-2">Showing first 50 of {edges.length} edges</p>
        )}
      </div>
    </div>
  )
}

export default DependencyGraph
