import { useState } from "react";

interface Props {
  onSubmit: (file: File) => Promise<void>;
  loading: boolean;
}

export default function UploadForm({ onSubmit, loading }: Props) {
  const [file, setFile] = useState<File | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    await onSubmit(file);
  }

  return (
    <form onSubmit={handleSubmit} className="card upload-card">
      <div className="upload-header">
        <div>
          <h2>Upload Stickhandling Video</h2>
          <p className="upload-subtext">
            Supported formats: MP4, MOV, AVI, MKV
          </p>
        </div>
      </div>

      <div className="upload-row">
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <button type="submit" disabled={!file || loading}>
          {loading ? "Analyzing..." : "Analyze Video"}
        </button>
      </div>

      <div className="selected-file">
        {file ? `Selected: ${file.name}` : "No file selected yet"}
      </div>
    </form>
  );
}