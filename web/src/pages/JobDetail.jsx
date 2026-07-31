import { useParams, Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { getJob } from "../api/client";
import Pipeline from "../components/Pipeline";
import StatusBadge from "../components/StatusBadge";

export default function JobDetail() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    let mounted = true;

    async function poll() {
      try {
        const data = await getJob(id);
        if (!mounted) return;
        setJob(data);
        if (data.status === "completed" || data.status === "error") {
          clearInterval(intervalRef.current);
        }
      } catch (err) {
        if (!mounted) return;
        setError(err.message);
        clearInterval(intervalRef.current);
      }
    }

    poll();
    intervalRef.current = setInterval(poll, 2000);

    return () => {
      mounted = false;
      clearInterval(intervalRef.current);
    };
  }, [id]);

  if (error) {
    return (
      <>
        <Link to="/" className="back-link">
          ← Back
        </Link>
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
        <Link to="/" className="back-link">
          ← Back
        </Link>
        <div className="empty-state">
          <span className="spinner" />
          <div className="empty-state__title" style={{ marginTop: 16 }}>
            Loading…
          </div>
        </div>
      </>
    );
  }

  const result = job.result;
  const score = result?.fact_check_score;

  function scoreClass(s) {
    if (s >= 0.8) return "high";
    if (s >= 0.5) return "mid";
    return "low";
  }

  return (
    <>
      <Link to="/" className="back-link">
        ← Back to research
      </Link>

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
        <h1 style={{ fontSize: "1.4rem", fontWeight: 700, flex: 1 }}>
          {job.topic || "Research Job"}
        </h1>
        <StatusBadge status={job.status} />
      </div>

      <Pipeline step={job.step} status={job.status} />

      {job.status === "running" && (
        <div className="result-card">
          <div style={{ display: "flex", alignItems: "center", gap: 10, color: "var(--text-muted)" }}>
            <span className="spinner" />
            Processing step: <strong style={{ color: "var(--accent)" }}>{job.step}</strong>
          </div>
        </div>
      )}

      {job.status === "completed" && result && (
        <>
          {/* Report */}
          <div className="result-card">
            <div className="result-card__header">
              <span className="result-card__title">Research Report</span>
              {score != null && (
                <div className="score-ring">
                  <div className={`score-ring__circle score-ring__circle--${scoreClass(score)}`}>
                    {score > 1 ? Math.round(score) : Math.round(score * 100)}%
                  </div>
                  <span className="score-ring__label">Accuracy</span>
                </div>
              )}
            </div>
            <div className="report-body">
              <ReactMarkdown
                components={{
                  a: ({ node, ...props }) => <a target="_blank" rel="noopener noreferrer" {...props} />
                }}
              >
                {result.report || ""}
              </ReactMarkdown>
            </div>
          </div>

          {/* Fact-check verifications */}
          {result.verifications && result.verifications.length > 0 && (
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
