function RiskCards({data}){

return(

<div className="bg-slate-800 p-6 rounded-xl">

<h2 className="text-lg mb-4">Repository Insights</h2>

<p>⭐ Stars: {data.stars}</p>
<p>🍴 Forks: {data.forks}</p>
<p>⚙ Language: {data.language}</p>
<p>🐞 Issues: {data.issues}</p>

<hr className="my-4 border-slate-700"/>

<h3 className="mb-2">Code Metrics</h3>

<p>📁 Python Files: {data.total_files}</p>
<p>📦 Large Files: {data.large_files}</p>

<hr className="my-4 border-slate-700"/>

<h3 className="mb-2">Risk Score</h3>

<p className="text-red-400">
{data.risk_score}/100
</p>

<hr className="my-4 border-slate-700"/>

<h3 className="mb-2">AI Recommendation</h3>

<p className="text-indigo-300">
{data.ai_recommendation}
</p>

</div>

)

}

export default RiskCards