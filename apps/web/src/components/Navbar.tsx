import { Link } from "react-router-dom";
import "./Navbar.css";
import logo from "../assets/logo.svg";

export default function Navbar() {
  return (
    <nav className="navbar">
      {/* LEFT: LOGO */}
      <div className="nav-left">
        <img src={logo} alt="NutryGym Logo" className="nav-logo" />
      </div>

      {/* CENTER: MENU */}
      <ul className="nav-menu">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/plans">Plans</Link></li>
        <li><Link to="/nutrigym">NutriGym</Link></li>
      </ul>

      {/* RIGHT: AUTH */}
      <div className="nav-right">
        <Link to="/auth" className="auth-link">
          Login / Sign up
        </Link>
      </div>
    </nav>
  );
}
