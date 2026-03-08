import { useState } from "react"

const GITHUB_URL_REGEX = /github\.com\/[\w.-]+\/[\w.-]+/

function RepoInput({ onAnalyze, disabled }) {
  const [url, setUrl] = useState("")
  const [validationError, setValidationError] = useState(null)

  const handleSubmit = () => {
    setValidationError(null)
    const trimmed = url.trim()
    if (!trimmed) {
      setValidationError("Please enter a repository URL.")
      return
    }
    if (!GITHUB_URL_REGEX.test(trimmed)) {
      setValidationError("Please enter a valid GitHub repo URL (e.g. https://github.com/owner/repo).")
      return
    }
    onAnalyze(trimmed)
  }

  return (
    <div className="flex flex-col items-center gap-4 mb-10">
      <div className="flex justify-center gap-4 w-full max-w-2xl">
        <input
          className="bg-slate-800/90 border border-slate-600 px-5 py-3.5 rounded-xl flex-1 max-w-md focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 outline-none transition-all placeholder:text-slate-500"
          placeholder="Paste GitHub repo URL (e.g. https://github.com/owner/repo)"
          value={url}
          onChange={(e) => {
            setUrl(e.target.value)
            setValidationError(null)
          }}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          disabled={disabled}
          aria-invalid={!!validationError}
        />
        <button
          className="bg-indigo-600 px-7 py-3.5 rounded-xl hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-lg shadow-indigo-900/25 transition-all hover:shadow-indigo-500/20 hover:scale-[1.02]"
          onClick={handleSubmit}
          disabled={disabled}
        >
          Analyze
        </button>
      </div>
      {validationError && (
        <p className="text-amber-400 text-sm" role="alert">
          {validationError}
        </p>
      )}
    </div>
  )
}

export default RepoInput