function AIArchitecturePanel({ aiArchitectureReview }) {
  if (!aiArchitectureReview || !aiArchitectureReview.trim()) {
    return (
      <div className="dashboard-card">
        <h2 className="card-title mb-4">AI architecture review</h2>
        <p className="text-slate-400 text-sm">
          Set <code className="bg-slate-700 px-1 rounded">OPENAI_API_KEY</code> in the backend to enable AI-powered architecture analysis.
        </p>
      </div>
    )
  }

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">AI architecture review</h2>
      <div className="prose prose-invert prose-sm max-w-none">
        <pre className="whitespace-pre-wrap text-slate-300 font-sans text-sm bg-slate-900/80 p-4 rounded-lg overflow-x-auto max-h-80 overflow-y-auto border border-slate-700/50">
          {aiArchitectureReview}
        </pre>
      </div>
    </div>
  )
}

export default AIArchitecturePanel
