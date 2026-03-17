interface ScoreData {
  total: number;
  subscores: Record<string, number>;
}

interface Props {
  score: ScoreData | null;
  loading: boolean;
}

const metricOrder = [
  "speed",
  "reversals",
  "smoothness",
  "tightness",
  "rhythm",
  "confidence_adj",
];

function formatMetricLabel(key: string): string {
  const labels: Record<string, string> = {
    speed: "Speed",
    reversals: "Reversals",
    smoothness: "Smoothness",
    tightness: "Tightness",
    rhythm: "Rhythm",
    confidence_adj: "Confidence Adj.",
  };

  return labels[key] || key;
}

export default function ScoreDashboard({ score, loading }: Props) {
  return (
    <div className="card panel-card">
      <div className="panel-header">
        <h2>Performance Scores</h2>
        <span className="panel-badge">
          {loading ? "Analyzing..." : score ? "Ready" : "Waiting"}
        </span>
      </div>

      <div className="score-box">
        <div className="score-label">Total Score</div>
        <div className={`score-value ${!score ? "score-placeholder" : ""}`}>
          {score ? score.total.toFixed(2) : "--.--"}
        </div>
      </div>

      <div className="metrics-grid">
        {metricOrder.map((key) => {
          const value = score?.subscores?.[key];

          return (
            <div key={key} className="metric-card">
              <div className="metric-title">{formatMetricLabel(key)}</div>
              <div className={`metric-value ${value === undefined ? "metric-placeholder" : ""}`}>
                {value !== undefined ? value.toFixed(2) : "--.--"}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}