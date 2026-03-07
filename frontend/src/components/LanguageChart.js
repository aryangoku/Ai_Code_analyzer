import {PieChart,Pie,Tooltip,Cell} from "recharts"

export default function LanguageChart({languages}){

const data = Object.keys(languages).map(k=>({
name:k,
value:languages[k]
}))

const COLORS=["#0088FE","#00C49F","#FFBB28","#FF8042"]

return(

<PieChart width={400} height={300}>

<Pie
data={data}
dataKey="value"
nameKey="name"
outerRadius={100}
>

{data.map((_,i)=>(
<Cell key={i} fill={COLORS[i % COLORS.length]}/>
))}

</Pie>

<Tooltip/>

</PieChart>

)
}