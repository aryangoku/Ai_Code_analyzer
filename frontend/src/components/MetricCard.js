export default function MetricCard({title,value}){

return(

<div style={{
background:"#fff",
padding:20,
borderRadius:10,
boxShadow:"0 4px 10px rgba(0,0,0,0.1)",
width:200
}}>

<h4 style={{color:"#666"}}>{title}</h4>

<h2>{value}</h2>

</div>

)

}