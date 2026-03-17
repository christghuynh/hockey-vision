import { useState } from "react";
import "./index.css";

import UploadForm from "./components/upload_form";
import ScoreDashboard from "./components/score_dashboard";
import PredictionVideo from "./components/prediction_video";

import { analyzeVideo, getOutputUrl } from "./api/analyze";
import type { AnalyzeResponse } from "./types/analyze";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState("");

  async function handleAnalyze(file: File) {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await analyzeVideo(file);
      setResult(res);
    } catch (err: any) {
      console.error("Frontend analyze error:", err);
      setError(err.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  const videoUrl = getOutputUrl(result?.artifacts?.prediction_video);

  return (
    <div className="app-shell">
      <div className="container">
        <header className="hero">
          <p className="eyebrow">AI Hockey Training Assistant</p>
          <h1>Hockey Vision</h1>
          <p className="hero-subtext">
            Upload a stickhandling drill and get AI-powered feedback on speed,
            smoothness, rhythm, and control.
          </p>
        </header>

        <UploadForm onSubmit={handleAnalyze} loading={loading} />

        {error && (
          <div className="card error-card">
            <h2>Error</h2>
            <p>{error}</p>
          </div>
        )}

        <div className="results-grid">
          <ScoreDashboard
            score={result?.score ?? null}
            loading={loading}
          />

          <PredictionVideo
            url={videoUrl}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}