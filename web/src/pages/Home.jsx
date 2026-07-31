import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { submitJob } from "../api/client";
import StatusBadge from "../components/StatusBadge";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("searchie_jobs") || "[]");
    } catch {
      return [];
    }
  });

  const navigate = useNavigate();

  function saveJobs(list) {
    setJobs(list);
    localStorage.setItem("searchie_jobs", JSON.stringify(list));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!topic.trim() || loading) return;
    setLoading(true);
    try {
      const data = await submitJob(topic.trim());
      const entry = {
        id: data.job_id,
        topic: topic.trim(),
        status: data.status,
        created: new Date().toISOString(),
      };
      saveJobs([entry, ...jobs].slice(0, 20));
      navigate(`/job/${data.job_id}`);
    } catch (err) {
      alert("Failed to submit: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <section className="hero">
        <div className="hero__badge">Multi-Agent Pipeline</div>
        <h1 className="hero__title">
          Research anything,
          <br />
          verified by AI.
        </h1>
        <p className="hero__subtitle">
          Searchie orchestrates four specialized agents to search, extract,
          synthesize, and fact-check — delivering trustworthy research reports in
          seconds.
        </p>

        <form className="search-box" onSubmit={handleSubmit}>
          <input
            id="search-input"
            className="search-box__input"
            type="text"
            placeholder="Enter a research topic…"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            autoFocus
          />
          <button
            id="search-submit"
            className="search-box__btn"
            type="submit"
            disabled={loading || !topic.trim()}
          >
            {loading ? (
              <>
                <span className="spinner" /> Submitting…
              </>
            ) : (
              "Research"
            )}
          </button>
        </form>
      </section>

      {jobs.length > 0 && (
        <>
          <div className="section-header">
            <span className="section-header__title">Recent Research</span>
          </div>
          <div className="job-list">
            {jobs.map((job) => (
              <Link
                key={job.id}
                to={`/job/${job.id}`}
                className="job-card"
                id={`job-${job.id}`}
              >
                <div className="job-card__icon">🔍</div>
                <div className="job-card__body">
                  <div className="job-card__topic">{job.topic}</div>
                  <div className="job-card__meta">
                    {new Date(job.created).toLocaleString()}
                  </div>
                </div>
                <StatusBadge status={job.status} />
              </Link>
            ))}
          </div>
        </>
      )}

      {jobs.length === 0 && (
        <div className="empty-state">
          <div className="empty-state__icon">📚</div>
          <div className="empty-state__title">No research yet</div>
          <div className="empty-state__desc">
            Enter a topic above to start your first multi-agent research.
          </div>
        </div>
      )}
    </>
  );
}
