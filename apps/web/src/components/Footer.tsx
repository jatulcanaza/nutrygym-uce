import "./Footer.css";
import logo from "../assets/logo.svg";
import { Link } from "react-router-dom";
import { FaFacebookF, FaLinkedinIn } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">

        {/* LEFT: LOGO */}
        <div className="footer-brand">
          <img src={logo} alt="NutryGym Logo" className="footer-logo" />
          <p>
            NutryGym is a smart nutrition and fitness platform designed for
            students and professionals.
          </p>
        </div>

        {/* CENTER: LINKS */}
        <div className="footer-links">
          <div>
            <h4>Our Gym</h4>
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>
            <Link to="/contact">Contact</Link>
          </div>

          <div>
            <h4>Services</h4>
            <Link to="/plans">Plans</Link>
            <Link to="/nutrigym">NutryGym</Link>
            <Link to="/routine">Routine</Link>
          </div>

          <div>
            <h4>Contact</h4>
            <Link to="/faq">FAQs</Link>
            <Link to="/contact">Support</Link>
            <Link to="/about">About Us</Link>
          </div>
        </div>

        {/* RIGHT: SOCIAL */}
        <div className="footer-social">
          <a href="#" aria-label="Facebook">
            <FaFacebookF />
          </a>
          <a href="#" aria-label="LinkedIn">
            <FaLinkedinIn />
          </a>
        </div>

      </div>

      <div className="footer-bottom">
        © 2026 NutryGym – UCE. All rights reserved.
      </div>
    </footer>
  );
}
