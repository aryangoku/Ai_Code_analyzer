export default function HealthGauge({score}){

return(

<h1 style={{
fontSize:60,
color: score>80 ? "green" : score>50 ? "orange":"red"
}}>

{score}/100

</h1>

)

}