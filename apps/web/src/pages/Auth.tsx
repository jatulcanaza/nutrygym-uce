import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, registerUser } from "../api/auth.api";
import "../pages/Auth.css";

export default function Auth() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const newErrors: { [key: string]: string } = {};

    if (!isLogin && !form.name.trim()) {
      newErrors.name = "Name is required";
    }
    if (!form.email.includes("@")) {
      newErrors.email = "Invalid email";
    }
    if (form.password.length < 6) {
      newErrors.password = "Minimum 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);
      if (isLogin) {
        await loginUser(form.email, form.password);
      } else {
        await registerUser(form.name, form.email, form.password);
      }
      navigate("/nutrigym");
    } catch (error: any) {
      alert(error?.response?.data?.detail || "Authentication error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        {/* LEFT */}
        <div className="auth-left">
          <img
            src="src/assets/logo.svg"
            alt="NutryGym Logo"
            className="logo"
          />
        </div>

        {/* RIGHT */}
        <div className="auth-right">
          <h1>
            <span className="green">Welcome</span> Back!
          </h1>
          <p className="subtitle">
            {isLogin ? "Login to get started" : "Register to get started"}
          </p>

          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <>
                <label>Name</label>
                <input
                  type="text"
                  placeholder="Enter your name"
                  value={form.name}
                  onChange={(e) =>
                    setForm({ ...form, name: e.target.value })
                  }
                />
                {errors.name && <small>{errors.name}</small>}
              </>
            )}

            <label>Email address</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={form.email}
              onChange={(e) =>
                setForm({ ...form, email: e.target.value })
              }
            />
            {errors.email && <small>{errors.email}</small>}

            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={form.password}
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />
            {errors.password && <small>{errors.password}</small>}

            <button type="submit" disabled={loading}>
              {loading ? "Processing..." : isLogin ? "Login" : "Register"}
            </button>
          </form>

          <p className="switch">
            {isLogin
              ? "You don't have an account?"
              : "Already have an account?"}
            <span onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? " Register" : " Login"}
            </span>
          </p>

          <Link to="/" className="back-home">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}
