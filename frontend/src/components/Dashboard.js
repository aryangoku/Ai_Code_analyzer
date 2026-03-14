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
import AIReviewPanel from "./AIReviewPanel"
import TechStackCard from "./TechStackCard"
import BusFactorCard from "./BusFactorCard"

function Dashboard({ data }) {
  return (
    <div className="space-y-8">
      {data.repo_summary && (
        <div className="dashboard-card">
          <h2 className="card-title mb-3">
            {data.ai_review && !data.ai_review.error ? (
              <span className="inline-flex items-center gap-2">
                Repository Summary
                <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-violet-500/20 text-violet-300 border border-violet-500/30">
                  AI
                </span>
              </span>
            ) : (
              "Repository Summary"
            )}
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed">
            {data.repo_summary}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ScoreGauge score={data.health_score} />
        <RiskCards data={data} />
        <ContributorChart
          stars={data.stars}
          forks={data.forks}
          issues={data.issues}
        />
      </div>

      <AIReviewPanel aiReview={data.ai_review} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <CommitHeatmap commitActivity={data.commit_activity} />
        <ContributorGraph contributors={data.contributors} />
        <LanguageChart languages={data.languages} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TechStackCard techStack={data.tech_stack} />
        <BusFactorCard busFactor={data.bus_factor} />
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
