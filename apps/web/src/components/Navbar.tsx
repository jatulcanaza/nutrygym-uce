import { Link } from "react-router-dom";
import { useState } from "react";
import "./navbar.css";
import logo from "../assets/logo.svg";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="navbar">
      {/* LEFT: LOGO */}
      <div className="nav-left">
        <img src={logo} alt="NutryGym Logo" className="nav-logo" />
      </div>

      {/* Toggle (solo móvil) */}
      <button
        className="nav-toggle"
        type="button"
        aria-label="Toggle menu"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        ☰
      </button>

      {/* CENTER: MENU */}
      <ul className={`nav-menu ${open ? "open" : ""}`}>
        <li><Link to="/" onClick={() => setOpen(false)}>Home</Link></li>
        <li><Link to="/about" onClick={() => setOpen(false)}>About</Link></li>
        <li><Link to="/plans" onClick={() => setOpen(false)}>Plans</Link></li>
        <li><Link to="/nutrigym" onClick={() => setOpen(false)}>NutriGym</Link></li>

        {/* AUTH también dentro en móvil para que no se corte */}
        <li className="nav-auth-mobile">
          <Link to="/auth" className="auth-link" onClick={() => setOpen(false)}>
            Login / Sign up
          </Link>
        </li>
      </ul>

      {/* RIGHT: AUTH (solo desktop) */}
      <div className="nav-right">
        <Link to="/auth" className="auth-link">
          Login / Sign up
        </Link>
      </div>
    </nav>
  );
}
