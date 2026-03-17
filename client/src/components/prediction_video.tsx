interface Props {
  url: string | null;
  loading: boolean;
}

export default function PredictionVideo({ url, loading }: Props) {
  return (
    <div className="card panel-card">
      <div className="panel-header">
        <h2>Annotated Video</h2>
        <span className="panel-badge">
          {loading ? "Processing..." : url ? "Ready" : "Waiting"}
        </span>
      </div>

      <div className="video-shell">
        {url ? (
          <video controls width="100%">
            <source src={url} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="video-placeholder">
            <div className="video-placeholder-icon">▶</div>
            <p>Your annotated detection preview will appear here.</p>
          </div>
        )}
      </div>
    </div>
  );
}