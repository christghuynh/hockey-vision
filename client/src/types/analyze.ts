export interface AnalyzeResponse {
  success: boolean;
  session_id?: string;
  error?: string;
  score?: {
    total: number;
    subscores: {
      speed: number;
      reversals: number;
      smoothness: number;
      tightness: number;
      rhythm: number;
      confidence_adj?: number;
    };
  };
  artifacts?: {
    prediction_video: string;
    track_csv: string;
    score_json: string;
  };
}