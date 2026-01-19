import "./About.css";

export default function About() {
  return (
    <section className="about-page">
      {/* HERO */}
      <header className="about-hero">
        <div className="about-hero-text">
          <div className="kicker">About NutryGym</div>

          <h1 className="title">
            Nutrition and training, designed for students<span className="dot">.</span>
          </h1>

          <p className="subtitle">
            NutryGym is a smart platform that helps UCE students generate personalized nutrition plans
            and follow structured training routines. The system uses a guided profile flow and AI-assisted
            plan generation to improve clarity, consistency, and results.
          </p>

          <div className="hero-actions">
            <a className="btn btn-primary" href="/plans">
              Explore modules
            </a>
            <a className="btn btn-ghost" href="/auth">
              Login / Sign up
            </a>
          </div>

          <div className="hero-metrics">
            <div className="metric">
              <div className="metric-value">6</div>
              <div className="metric-label">Microservices</div>
            </div>
            <div className="metric">
              <div className="metric-value">AI</div>
              <div className="metric-label">Plan generation</div>
            </div>
            <div className="metric">
              <div className="metric-value">UCE</div>
              <div className="metric-label">Student focus</div>
            </div>
          </div>
        </div>

        <div className="about-hero-media">
          {/* Coloca esta imagen en /public/about-hero.png */}
          <img
            className="hero-img"
            src="/about-hero.png"
            alt="NutryGym platform illustration"
          />
          <div className="media-card">
            <div className="media-card-title">Guided workflow</div>
            <div className="media-card-text">
              Profile → Nutrition Form → AI Plan → Manage & History
            </div>
          </div>
        </div>
      </header>

      {/* MISSION / VISION */}
      <div className="grid-2">
        <div className="panel">
          <h2>Mission</h2>
          <p className="muted">
            Help students make better nutrition decisions through guided data collection,
            AI-assisted plan generation, and a clear weekly structure that is easy to follow.
          </p>
        </div>

        <div className="panel">
          <h2>Vision</h2>
          <p className="muted">
            Become a reference platform for student wellbeing by integrating nutrition,
            training routines, and progress management into a unified, modern experience.
          </p>
        </div>
      </div>

      {/* WHAT WE SOLVE */}
      <section className="section">
        <div className="section-title">
          <h2>What problem does NutryGym solve?</h2>
          <p>
            Many students struggle to maintain consistent habits due to lack of structure, time,
            and clear guidance. NutryGym reduces uncertainty by providing a plan that matches the user profile.
          </p>
        </div>

        <div className="features">
          <article className="feature">
            <div className="feature-title">Clear weekly plan</div>
            <div className="feature-text">
              A Monday–Sunday table with meals, designed to be practical and easy to apply.
            </div>
          </article>

          <article className="feature">
            <div className="feature-title">Guided data flow</div>
            <div className="feature-text">
              The user completes profile and nutrition form before generating a plan, improving accuracy.
            </div>
          </article>

          <article className="feature">
            <div className="feature-title">Plan management</div>
            <div className="feature-text">
              Users can edit or cancel plans and maintain a clear history of previous plans.
            </div>
          </article>

          <article className="feature">
            <div className="feature-title">Scalable architecture</div>
            <div className="feature-text">
              Microservice design allows the platform to evolve with modular responsibilities.
            </div>
          </article>
        </div>
      </section>

      {/* ARCHITECTURE */}
      <section className="section">
        <div className="section-title">
          <h2>Platform architecture</h2>
          <p>
            The system is implemented as a set of services that communicate through an API layer, enabling scalability,
            separation of responsibilities, and easier maintenance.
          </p>
        </div>

        <div className="services">
          <div className="service-card">
            <div className="service-badge">Auth</div>
            <div className="service-title">auth-service</div>
            <div className="service-text">
              Login, registration, and token-based authentication.
            </div>
          </div>

          <div className="service-card">
            <div className="service-badge">Profile</div>
            <div className="service-title">user-profile-service</div>
            <div className="service-text">
              Stores profile data (height, weight, goals, activity level).
            </div>
          </div>

          <div className="service-card">
            <div className="service-badge">Nutrition</div>
            <div className="service-title">nutrition-form-service</div>
            <div className="service-text">
              Collects nutrition preferences and constraints for plan generation.
            </div>
          </div>

          <div className="service-card">
            <div className="service-badge">Roles</div>
            <div className="service-title">role_permission-service</div>
            <div className="service-text">
              Manages roles, permissions, and access control.
            </div>
          </div>

          <div className="service-card">
            <div className="service-badge">Plans</div>
            <div className="service-title">plan-management-service</div>
            <div className="service-text">
                Creates, stores, versions, and manages nutrition plans (active, ended, canceled, history).
            </div>
            </div>

            <div className="service-card">
            <div className="service-badge">AI</div>
            <div className="service-title">ai-generator-service</div>
            <div className="service-text">
                Generates structured weekly meal plans using AI based on profile and nutrition form data.
            </div>
            </div>

        </div>
      </section>

      {/* TEAM */}
      <section className="section">
        <div className="section-title">
          <h2>Creators</h2>
          <p>
            This project was developed as an academic and engineering initiative focused on real-world architecture,
            usability, and maintainability.
          </p>
        </div>

        <div className="team">
          <article className="team-card">
            {/* Pon esta imagen en /public/team-1.png (o usa una foto tuya) */}
            <img className="avatar" src="/team-1.png" alt="Team member" />
            <div className="team-name">Juan Tulcanaza</div>
            <div className="team-role">Full-stack / Cloud</div>
            <p className="team-text">
              Frontend experience design, service integration, and infrastructure workflows.
            </p>
          </article>

          <article className="team-card">
            <img className="avatar" src="/team-2.png" alt="Team member" />
            <div className="team-name">Juan Tulcanaza</div>
            <div className="team-role">Backend / Data</div>
            <p className="team-text">
              API design, validations, and data models for nutrition planning.
            </p>
          </article>

          <article className="team-card">
            <img className="avatar" src="/team-3.png" alt="Team member" />
            <div className="team-name">Juan Tulcanaza</div>
            <div className="team-role">AI / Integration</div>
            <p className="team-text">
              AI workflow integration and plan generation pipelines.
            </p>
          </article>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <div className="cta-card">
          <div>
            <h2>Ready to generate your plan?</h2>
            <p className="muted">
              Go to the modules page and start with NutriGym. You can edit your profile and preferences anytime.
            </p>
          </div>
          <div className="cta-actions">
            <a className="btn btn-primary" href="/plans">
              Go to modules
            </a>
            <a className="btn btn-ghost" href="/nutrigym">
              Open dashboard
            </a>
          </div>
        </div>
      </section>
    </section>
  );
}
