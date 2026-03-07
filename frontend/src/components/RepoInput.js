import { useState } from "react"

function RepoInput({onAnalyze}){

const [url,setUrl]=useState("")

return(

<div className="flex justify-center gap-4 mb-10">

<input
className="bg-slate-800 px-4 py-3 rounded-lg w-96"
placeholder="Paste GitHub repo URL"
value={url}
onChange={(e)=>setUrl(e.target.value)}
/>

<button
className="bg-indigo-600 px-6 py-3 rounded-lg hover:bg-indigo-500"
onClick={()=>onAnalyze(url)}
>
Analyze
</button>

</div>

)

}

export default RepoInput