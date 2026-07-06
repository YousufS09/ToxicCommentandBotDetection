import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="page-container">
      <section className="hero">
        <div className="hero-panel">
          <div className="hero-kicker">AI moderation workspace</div>
          <h1>Detect harmful language and suspicious accounts with clarity.</h1>
          <p className="page-intro">
            This platform combines toxicity detection, bot identification, and
            joint risk scoring into one minimalist dashboard for safer social
            media review.
          </p>

          <div className="hero-actions">
            <Link to="/combined" className="hero-action hero-action--primary">
              Start combined analysis
            </Link>
            <Link to="/toxic" className="hero-action hero-action--secondary">
              Review toxic comments
            </Link>
          </div>
        </div>

        <aside className="info-panel">
          <div className="metric-grid">
            <div className="metric-card">
              <strong>01</strong>
              <span>Toxicity classification</span>
            </div>
            <div className="metric-card">
              <strong>02</strong>
              <span>Bot account signals</span>
            </div>
            <div className="metric-card">
              <strong>03</strong>
              <span>Combined risk scoring</span>
            </div>
          </div>

          <div className="floating-divider" />

          <p className="section-copy">
            Built with a FastAPI backend, React interface, and model-backed
            inference pipelines for real-world moderation workflows.
          </p>
        </aside>
      </section>

      <div className="section-grid">
        <section className="section-panel">
          <h3>What it does</h3>
          <ul>
            <li>Analyzes comments for toxic or non-toxic language.</li>
            <li>Estimates whether an account behaves like a bot.</li>
            <li>Combines both signals into a single risk recommendation.</li>
          </ul>
        </section>

        <section className="section-panel section-panel--accent">
          <h3>Why it stands out</h3>
          <ul>
            <li>Clean API-driven workflow for easy integration.</li>
            <li>ML-backed inference with confidence and interpretation.</li>
            <li>Minimalist interface designed for fast review.</li>
          </ul>
        </section>
      </div>
    </div>
  );
}

export default Home;
