import type { AnalyzeResponse } from "../types/analyze";

const API_BASE = "http://localhost:3000";

export async function analyzeVideo(file: File): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("video", file);

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Analysis failed");
  }

  return data;
}

export function getOutputUrl(relativePath?: string): string | null {
  if (!relativePath) return null;
  return `${API_BASE}${relativePath}`;
}