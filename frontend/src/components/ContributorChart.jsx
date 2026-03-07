import { BarChart,Bar,XAxis,YAxis,Tooltip } from "recharts"

function ContributorChart({stars,forks,issues}){

const data=[

{name:"Stars",value:stars},
{name:"Forks",value:forks},
{name:"Issues",value:issues}

]

return(

<div className="bg-slate-800 p-6 rounded-xl">

<h2 className="mb-4 text-lg">
Repository Activity
</h2>

<BarChart width={250} height={200} data={data}>

<XAxis dataKey="name"/>
<YAxis/>
<Tooltip/>

<Bar dataKey="value" fill="#6366f1"/>

</BarChart>

</div>

)

}

export default ContributorChart