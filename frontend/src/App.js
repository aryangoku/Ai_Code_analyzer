import { useState } from "react"
import RepoInput from "./components/RepoInput"
import Dashboard from "./components/Dashboard"
import { analyzeRepo } from "./api"

function App(){

const [data,setData]=useState(null)
const [loading,setLoading]=useState(false)

const handleAnalyze=async(url)=>{

try{

setLoading(true)

const res=await analyzeRepo(url)

setData(res)

setLoading(false)

}catch(e){

alert("Backend error")

setLoading(false)

}

}

return(

<div className="min-h-screen bg-slate-900 text-white p-10">

<h1 className="text-4xl font-bold text-center mb-10">
DevInsight AI
</h1>

<RepoInput onAnalyze={handleAnalyze}/>

{loading &&

<div className="text-center mt-10">
Analyzing repository...
</div>

}

{data && <Dashboard data={data}/>}

</div>

)

}

export default App