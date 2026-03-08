import { BarChart,Bar,XAxis,YAxis,Tooltip } from "recharts"

function ContributorChart({stars,forks,issues}){

const data=[

{name:"Stars",value:stars},
{name:"Forks",value:forks},
{name:"Issues",value:issues}

]

return(

<div className="dashboard-card">

<h2 className="card-title mb-4">Repository Activity</h2>

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