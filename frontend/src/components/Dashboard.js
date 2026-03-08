import ScoreGauge from "./ScoreGauge"
import RiskCards from "./RiskCards"
import ContributorChart from "./ContributorChart"
import CommitHeatmap from "./CommitHeatmap"
import ContributorGraph from "./ContributorGraph"
import EngineeringHealthScore from "./EngineeringHealthScore"
import DependencyGraph from "./DependencyGraph"
import AIArchitecturePanel from "./AIArchitecturePanel"

function Dashboard({ data }) {
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ScoreGauge score={data.health_score} />
        <RiskCards data={data} />
        <ContributorChart stars={data.stars} forks={data.forks} issues={data.issues} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CommitHeatmap commitActivity={data.commit_activity} />
        <ContributorGraph contributors={data.contributors} />
      </div>

      {data.engineering_health && (
        <EngineeringHealthScore engineeringHealth={data.engineering_health} />
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DependencyGraph dependencyGraph={data.dependency_graph} />
        <AIArchitecturePanel aiArchitectureReview={data.ai_architecture_review} />
      </div>
    </div>
  )
}

export default Dashboard