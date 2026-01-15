import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import "./Welcome.css";

export default function Welcome() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 30);
    return () => clearTimeout(t);
  }, []);

  return (
    <section className={`welcome-page ${mounted ? "is-mounted" : ""}`}>
      {/* HERO IMAGE */}
      <header className="welcome-hero">
        <div className="hero-overlay" />

        <div className="hero-content">
          <div className="hero-left">
            <div className="welcome-kicker">NutryGym • UCE</div>

            <h1 className="welcome-title">
              Nutry<span className="green">Gym</span>
              <br />
              <span className="hero-subline">Your AI-powered nutrition</span>
            </h1>

            <p className="welcome-subtitle">
              Personalized plans based on your goals, profile and preferences. Designed to provide clarity,
              structure and actionable weekly guidance.
            </p>

            <div className="welcome-actions">
              <Link to="/plans" className="btn btn-primary">
                Get started
              </Link>
              <Link to="/auth" className="btn btn-ghost">
                Login / Sign up
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* HOW IT WORKS */}
      <section className="section">
        <div className="section-title">
          <h2>How does it work?</h2>
          <p>Follow a guided flow to generate and manage your weekly nutrition plan.</p>
        </div>

        <div className="how-grid">
          <div className="how-step">
            <div className="how-icon">
              {/* lock icon */}
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M17 9h-1V7a4 4 0 10-8 0v2H7a2 2 0 00-2 2v8a2 2 0 002 2h10a2 2 0 002-2v-8a2 2 0 00-2-2zm-7-2a2 2 0 114 0v2h-4V7zm7 12H7v-8h10v8z" />
              </svg>
            </div>
            <div className="how-text">
              <div className="how-title">Step 1</div>
              <div className="how-desc">Log in. If you don’t have an account, create one.</div>
            </div>
          </div>

          <div className="how-step">
            <div className="how-icon">
              {/* profile icon */}
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 12a4 4 0 10-4-4 4 4 0 004 4zm0 2c-4.42 0-8 2-8 4v2h16v-2c0-2-3.58-4-8-4z" />
              </svg>
            </div>
            <div className="how-text">
              <div className="how-title">Step 2</div>
              <div className="how-desc">Enter your information to create your nutrition profile.</div>
            </div>
          </div>

          <div className="how-step">
            <div className="how-icon">
              {/* AI icon */}
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M9 2h6v2h-1v2.1a6.5 6.5 0 013.9 3.9H20v6h-2v-1a6.5 6.5 0 01-3.9 3.9V22h-6v-2h1v-2.1A6.5 6.5 0 014.1 14.1H2v-6h2v1A6.5 6.5 0 017.9 4.1V4H9V2zm3 5a5 5 0 100 10 5 5 0 000-10z" />
              </svg>
            </div>
            <div className="how-text">
              <div className="how-title">Step 3</div>
              <div className="how-desc">Generate your plan with AI based on your preferences.</div>
            </div>
          </div>

          <div className="how-step">
            <div className="how-icon">
              {/* check icon */}
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.5-1.5L9 16.2z" />
              </svg>
            </div>
            <div className="how-text">
              <div className="how-title">Step 4</div>
              <div className="how-desc">Review your progress: edit, cancel, and manage history.</div>
            </div>
          </div>
        </div>
      </section>

      {/* CHARACTERISTICS */}
      <section className="section">
        <div className="section-split">
          <div className="cards-3">
            <article className="feature-card">
              <div className="feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M3 4h18v2H3V4zm2 4h14v12H5V8zm2 2v2h4v-2H7zm0 4v2h6v-2H7z" />
                </svg>
              </div>
              <h3>Personalized weekly plans</h3>
              <p>Structured Monday–Sunday meal schedule tailored to your profile.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M4 19h16v2H4v-2zm2-2h12V3H6v14zm2-2V5h8v10H8z" />
                </svg>
              </div>
              <h3>Track and manage progress</h3>
              <p>Edit or cancel plans and keep a clear history of results.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2a10 10 0 1010 10A10 10 0 0012 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                </svg>
              </div>
              <h3>Smart recommendations</h3>
              <p>AI-driven summary and conclusion to guide your decisions.</p>
            </article>
          </div>

          <div className="right-copy">
            <div className="kicker">Characteristics</div>
            <h2 className="big-title">
              A clean workflow that reduces uncertainty
            </h2>
            <p className="muted">
              NutryGym is designed to be practical. The platform collects the right data first,
              then produces a clear weekly plan and provides management tools for consistent use.
            </p>

            <div className="cta-row">
              <Link to="/nutrigym" className="btn btn-primary">
                Open NutriGym
              </Link>
              <Link to="/about" className="btn btn-ghost">
                About the project
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* MODULES (Gym + NutriGym) */}
      <section className="section">
        <div className="section-title">
          <h2>Modules</h2>
          <p>Choose the module you want to use. Start with NutriGym, then align training in Gym.</p>
        </div>

        <div className="modules-grid">
          <article className="module-card">
            <div className="module-head">
              <div className="module-badge">AI Nutrition</div>
              <h3>NutriGym</h3>
              <p>Profile + preferences → weekly plan → edit and history.</p>
            </div>
            <div className="module-actions">
              <Link to="/nutrigym" className="btn btn-primary">
                Go to dashboard
              </Link>
              <Link to="/plans" className="btn btn-ghost">
                View details
              </Link>
            </div>
          </article>

          <article className="module-card">
            <div className="module-head">
              <div className="module-badge badge-dark">Training</div>
              <h3>Gym</h3>
              <p>Workout routines and training structure aligned to your goal.</p>
            </div>
            <div className="module-actions">
              <Link to="/gym" className="btn btn-primary">
                Open training
              </Link>
              <Link to="/plans" className="btn btn-ghost">
                View details
              </Link>
            </div>
          </article>
        </div>
      </section>
    </section>
  );
}
