const LANG_COLORS = {
  Python: "#3776ab",
  JavaScript: "#f7df1e",
  TypeScript: "#3178c6",
  "React (JSX)": "#61dafb",
  "React (TSX)": "#61dafb",
  Go: "#00add8",
  Java: "#ed8b00",
  Ruby: "#cc342d",
  PHP: "#777bb4",
  "C#": "#239120",
  "C++": "#00599c",
  C: "#a8b9cc",
  Rust: "#dea584",
  Kotlin: "#7f52ff",
  Swift: "#fa7343",
  Dart: "#0175c2",
  HTML: "#e34f26",
  CSS: "#1572b6",
  SCSS: "#cc6699",
  Vue: "#42b883",
  Svelte: "#ff3e00",
  Shell: "#89e051",
}

function TechStackCard({ techStack }) {
  if (!techStack || techStack.length === 0) return null

  const languages = techStack.filter((t) => t.type === "language")
  const frameworks = techStack.filter((t) => t.type === "framework")

  return (
    <div className="dashboard-card">
      <h2 className="card-title mb-4">Tech Stack</h2>

      {languages.length > 0 && (
        <div className="mb-4">
          <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2">
            Languages
          </h3>
          <div className="flex flex-wrap gap-2">
            {languages.map((lang) => (
              <span
                key={lang.name}
                className="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1.5 rounded-lg border border-slate-600/50 bg-slate-700/50"
              >
                <span
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{
                    backgroundColor: LANG_COLORS[lang.name] || "#6b7280",
                  }}
                />
                {lang.name}
                <span className="text-slate-500 ml-0.5">{lang.count}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {frameworks.length > 0 && (
        <div>
          <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2">
            Frameworks & Tools
          </h3>
          <div className="flex flex-wrap gap-2">
            {frameworks.map((fw) => (
              <span
                key={fw.name}
                className="text-xs font-medium px-2.5 py-1.5 rounded-lg border border-indigo-500/30 bg-indigo-500/10 text-indigo-300"
              >
                {fw.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default TechStackCard
