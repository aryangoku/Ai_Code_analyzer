import ScoreGauge from "./ScoreGauge"
import RiskCards from "./RiskCards"
import ContributorChart from "./ContributorChart"
import LanguageChart from "./LanguageChart"
import CommitHeatmap from "./CommitHeatmap"
import ContributorGraph from "./ContributorGraph"
import EngineeringHealthScore from "./EngineeringHealthScore"
import DependencyGraph from "./DependencyGraph"
import HotspotTable from "./HotspotTable"
import QualityChecklist from "./QualityChecklist"

function Dashboard({ data }) {
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ScoreGauge score={data.health_score} />
        <RiskCards data={data} />
        <ContributorChart stars={data.stars} forks={data.forks} issues={data.issues} />
      </div>

      {data.repo_summary && (
        <div className="dashboard-card">
          <h2 className="card-title mb-3">Repository summary</h2>
          <p className="text-sm text-slate-300">{data.repo_summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <CommitHeatmap commitActivity={data.commit_activity} />
        <ContributorGraph contributors={data.contributors} />
        <LanguageChart languages={data.languages} />
      </div>

      {data.engineering_health && (
        <EngineeringHealthScore engineeringHealth={data.engineering_health} />
      )}

      {data.quality && <QualityChecklist quality={data.quality} />}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DependencyGraph dependencyGraph={data.dependency_graph} />
        <HotspotTable hotspots={data.hotspots} />
      </div>
    </div>
  )
}

export default Dashboard