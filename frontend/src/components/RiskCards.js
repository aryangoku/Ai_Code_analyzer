import { useState } from "react"

function RiskCards({ data }) {
  const [showSecurity, setShowSecurity] = useState(false)

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Repository Insights</h2>
      <p>⭐ Stars: {data.stars}</p>
      <p>🍴 Forks: {data.forks}</p>
      <p>⚙ Language: {data.language}</p>
      <p>🐞 Issues: {data.issues}</p>

      <hr className="my-4 border-slate-700" />

      <h3 className="mb-2">Code Metrics</h3>
      <p>📁 Python Files: {data.total_files}</p>
      <p>📦 Large Files: {data.large_files}</p>

      <hr className="my-4 border-slate-700" />

      <h3 className="mb-2">Risk Score</h3>
      <p className="text-red-400">{data.risk_score}/100</p>

      <hr className="my-4 border-slate-700" />

      <h3 className="mb-2">AI Recommendation</h3>
      <p className="text-indigo-300 whitespace-pre-wrap">{data.ai_recommendation}</p>

      {data.security_report && (
        <>
          <hr className="my-4 border-slate-700" />
          <h3 className="mb-2">Security (Bandit)</h3>
          <button
            type="button"
            className="text-sm text-indigo-400 hover:text-indigo-300 mb-2 px-2 py-1 rounded hover:bg-slate-700/50 transition-colors"
            onClick={() => setShowSecurity(!showSecurity)}
          >
            {showSecurity ? "Hide" : "Show"} report
          </button>
          {showSecurity && (
            <pre className="text-xs text-slate-300 bg-slate-900/80 p-3 rounded-lg overflow-x-auto max-h-48 overflow-y-auto border border-slate-700/50">
              {data.security_report}
            </pre>
          )}
        </>
      )}
    </div>
  )
}

export default RiskCards