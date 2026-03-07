export default function HotspotTable({files}){

return(

<table style={{
marginTop:20,
borderCollapse:"collapse"
}}>

<thead>

<tr>

<th style={{padding:10}}>File</th>
<th style={{padding:10}}>Lines</th>

</tr>

</thead>

<tbody>

{files.map((f,i)=>(

<tr key={i}>

<td style={{padding:10}}>{f[0]}</td>
<td style={{padding:10}}>{f[1]}</td>

</tr>

))}

</tbody>

</table>

)

}