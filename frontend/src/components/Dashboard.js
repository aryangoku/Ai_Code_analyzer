import ScoreGauge from "./ScoreGauge"
import RiskCards from "./RiskCards"
import ContributorChart from "./ContributorChart"

function Dashboard({data}){

return(

<div className="grid grid-cols-3 gap-6">

<ScoreGauge score={data.health_score}/>

<RiskCards data={data}/>

<ContributorChart stars={data.stars} forks={data.forks} issues={data.issues}/>

</div>

)

}

export default Dashboard