import { useState } from "react"
import Landing from "./components/Landing"
import Dashboard from "./components/Dashboard"
import Footer from "./components/Footer"
import { analyzeRepo } from "./api"

export default function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (url) => {
    setError(null)
    setData(null)
    try {
      setLoading(true)
      const res = await analyzeRepo(url)
      setData(res)
    } catch (e) {
      const message =
        e.response?.data?.detail ||
        e.response?.statusText ||
        e.message ||
        "Analysis failed. Check that the backend is running and the URL is valid."
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzeAnother = () => {
    setData(null)
    setError(null)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  return (
    <div className="min-h-screen text-white relative flex flex-col">
      <header className="relative z-20 flex items-center justify-between gap-4 px-6 md:px-10 py-6">
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-indigo-400">
            CodePulse
          </span>
        </h1>
      </header>

      <main className="flex-1">
        {!data ? (
          <Landing onAnalyze={handleAnalyze} disabled={loading} />
        ) : (
          <div className="relative z-10 px-6 md:px-10 pb-10">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
              <div>
                <h2 className="text-xl font-semibold text-white">
                  {data.repo_name || "Repository"}
                </h2>
                {data.repo_url && (
                  <a
                    href={data.repo_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-slate-400 hover:text-indigo-400 transition-colors"
                  >
                    {data.repo_url}
                  </a>
                )}
              </div>
              <button
                type="button"
                onClick={handleAnalyzeAnother}
                className="text-sm px-5 py-2.5 rounded-xl bg-indigo-600/90 hover:bg-indigo-500 text-white font-medium border border-indigo-500/50 shadow-lg shadow-indigo-900/20 transition-all hover:scale-[1.02]"
              >
                Analyze another repo
              </button>
            </div>
            <Dashboard data={data} />
          </div>
        )}
      </main>

      <Footer />

      {error && (
        <div
          className="fixed bottom-6 left-1/2 -translate-x-1/2 z-30 max-w-xl w-full mx-4 p-4 rounded-xl bg-red-900/90 border border-red-500/50 text-red-200 shadow-xl backdrop-blur-sm"
          role="alert"
        >
          {error}
        </div>
      )}

      {loading && (
        <div className="fixed inset-0 z-30 flex items-center justify-center bg-slate-900/70 backdrop-blur-sm">
          <div className="text-center">
            <div className="w-14 h-14 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-slate-300 font-medium">Analyzing repository…</p>
          </div>
        </div>
      )}
    </div>
  )
}
