import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import "./Plans.css";

export default function Plans() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Solo para activar animación de entrada
    const t = setTimeout(() => setMounted(true), 30);
    return () => clearTimeout(t);
  }, []);

  return (
    <section className={`plans-page ${mounted ? "is-mounted" : ""}`}>
      <header className="plans-header">
        <div>
          <div className="plans-kicker">Services</div>
          <h1 className="plans-title">
            Choose your module<span className="dot">.</span>
          </h1>
          <p className="plans-subtitle">
            Access NutriGym for AI-based nutrition plans or Gym for workout routines and training features.
          </p>
        </div>
      </header>

      <div className="plans-grid">
        {/* NutriGym card */}
        <article className="plan-card">
          <div className="plan-badge">AI Nutrition</div>

          <h2 className="plan-name">NutriGym</h2>
          <p className="plan-desc">
            Generate a personalized weekly nutrition plan based on your profile and preferences. Edit, cancel, and track history.
          </p>

          <ul className="plan-list">
            <li>Profile + nutrition form flow</li>
            <li>Weekly plan table (Mon–Sun)</li>
            <li>Plan history and management</li>
          </ul>

          <div className="plan-actions">
            <Link to="/nutrigym" className="btn btn-primary">
              Open NutriGym
            </Link>
            <Link to="/auth" className="btn btn-ghost">
              Login required
            </Link>
          </div>
        </article>

        {/* Gym card */}
        <article className="plan-card">
          <div className="plan-badge badge-dark">Training</div>

          <h2 className="plan-name">Gym</h2>
          <p className="plan-desc">
            Explore workout routines, weekly training structure, and recommended exercises. Designed for consistency and progression.
          </p>

          <ul className="plan-list">
            <li>Workout routines by objective</li>
            <li>Weekly training schedule</li>
            <li>Progress-friendly structure</li>
          </ul>

          <div className="plan-actions">
            {/* Ajusta la ruta cuando tengas lista la página */}
            <Link to="/gym" className="btn btn-primary">
              Open Gym
            </Link>
            <Link to="/about" className="btn btn-ghost">
              Learn more
            </Link>
          </div>
        </article>
      </div>

      <div className="plans-footer">
        <div className="info-card">
          <h3>Recommended workflow</h3>
          <p>
            Start with NutriGym to set your nutrition plan. Then use Gym to align training routines with your goal.
          </p>
        </div>
      </div>
    </section>
  );
}
