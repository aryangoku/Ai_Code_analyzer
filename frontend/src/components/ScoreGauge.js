import { RadialBarChart,RadialBar,PolarAngleAxis } from "recharts"

function ScoreGauge({score}){

const data=[{value:score}]

return(

<div className="dashboard-card text-center">

<h2 className="card-title mb-4">Health Score</h2>

<RadialBarChart
width={250}
height={250}
innerRadius="70%"
outerRadius="100%"
data={data}
startAngle={90}
endAngle={-270}
>

<PolarAngleAxis
type="number"
domain={[0,100]}
tick={false}
/>

<RadialBar
dataKey="value"
background
fill="#6366f1"
/>

</RadialBarChart>

<p className="text-3xl mt-4 font-bold">
{score}/100
</p>

</div>

)

}

export default ScoreGauge