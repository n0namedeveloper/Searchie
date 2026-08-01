import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { API_BASE } from "../api/client";
import Pipeline from "../components/Pipeline";
import StatusBadge from "../components/StatusBadge";

export default function JobDetail() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);
  const [reportStream, setReportStream] = useState("");

  useEffect(() => {
    let mounted = true;
    const eventSource = new EventSource(`${API_BASE}/api/v1/jobs/${id}/stream`);

    eventSource.addEventListener("init", (e) => {
      if (!mounted) return;
      const data = JSON.parse(e.data);
      setJob(data);
      if (data.result && data.result.report) {
         setReportStream(data.result.report);
      }
    });

    eventSource.addEventListener("step", (e) => {
      if (!mounted) return;
      const step = JSON.parse(e.data);
      setJob(prev => prev ? { ...prev, step } : null);
    });

    eventSource.addEventListener("stream", (e) => {
      if (!mounted) return;
      const chunk = JSON.parse(e.data);
      setReportStream(prev => prev + chunk);
    });

    eventSource.addEventListener("completed", (e) => {
      if (!mounted) return;
      const result = JSON.parse(e.data);
      setJob(prev => prev ? { ...prev, status: "completed", result } : null);
      if (result.report) setReportStream(result.report);
      eventSource.close();
    });

    eventSource.addEventListener("error", (e) => {
      if (!mounted) return;
      const errMsg = JSON.parse(e.data);
      setError(errMsg);
      setJob(prev => prev ? { ...prev, status: "error" } : null);
      eventSource.close();
    });

    return () => {
      mounted = false;
      eventSource.close();
    };
  }, [id]);

  const handleExport = () => {
    const blob = new Blob([reportStream], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${job?.topic || "research"}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (error) {
    return (
      <>
        <Link to="/" className="back-link">← Back</Link>
        <div className="empty-state">
          <div className="empty-state__icon">⚠️</div>
          <div className="empty-state__title">Error loading job</div>
          <div className="empty-state__desc">{error}</div>
        </div>
      </>
    );
  }

  if (!job) {
    return (
      <>
        <Link to="/" className="back-link">← Back</Link>
        <div className="empty-state">
          <span className="spinner" />
          <div className="empty-state__title" style={{ marginTop: 16 }}>Loading…</div>
        </div>
      </>
    );
  }

  const result = job.result;
  const rawScore = result?.fact_check_score;
  let displayScore = 0;
  if (rawScore != null) {
    const numScore = Number(rawScore);
    if (!isNaN(numScore)) {
      displayScore = numScore > 1 ? Math.round(numScore) : Math.round(numScore * 100);
      if (displayScore > 100) displayScore = 100;
    }
  }

  function scoreClass(s) {
    if (s >= 0.8) return "high";
    if (s >= 0.5) return "mid";
    return "low";
  }

  return (
    <>
      <Link to="/" className="back-link">← Back to research</Link>

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
        <h1 style={{ fontSize: "1.4rem", fontWeight: 700, flex: 1 }}>{job.topic || "Research Job"}</h1>
        <StatusBadge status={job.status} />
      </div>

      <Pipeline step={job.step} status={job.status} />

      {job.status === "running" && (
        <div className="result-card">
          <div style={{ display: "flex", alignItems: "center", gap: 10, color: "var(--text-muted)" }}>
            <span className="spinner" />
            Processing step: <strong style={{ color: "var(--accent)" }}>{job.step}</strong>
          </div>
          {reportStream && (
            <div className="report-body" style={{ marginTop: 20 }}>
              <ReactMarkdown>{reportStream}</ReactMarkdown>
            </div>
          )}
        </div>
      )}

      {job.status === "completed" && (
        <>
          <div className="result-card">
            <div className="result-card__header">
              <span className="result-card__title">Research Report</span>
              <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                <button onClick={handleExport} className="search-box__btn" style={{ padding: "8px 16px", fontSize: "0.9rem" }}>
                  Export .MD
                </button>
                {rawScore != null && (
                  <div className="score-ring">
                    <div className={`score-ring__circle score-ring__circle--${scoreClass(rawScore)}`}>
                      {displayScore}%
                    </div>
                    <span className="score-ring__label">Accuracy</span>
                  </div>
                )}
              </div>
            </div>
            <div className="report-body">
              <ReactMarkdown
                components={{
                  a: ({ node, ...props }) => <a target="_blank" rel="noopener noreferrer" {...props} />
                }}
              >
                {reportStream}
              </ReactMarkdown>
            </div>
          </div>

          {result?.verifications && result.verifications.length > 0 && (
            <div className="result-card">
              <div className="result-card__header">
                <span className="result-card__title">Fact-check Verifications</span>
              </div>
              <div className="verification-list">
                {result.verifications.map((v, i) => (
                  <div key={i} className="verification">
                    <div className={`verification__icon verification__icon--${v.is_accurate}`}>
                      {v.is_accurate ? "✓" : "✗"}
                    </div>
                    <div>
                      <div className="verification__claim">{v.claim}</div>
                      <div className="verification__reasoning">{v.reasoning}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}
