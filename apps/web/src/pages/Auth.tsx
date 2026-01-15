import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, registerUser } from "../api/auth.api";
import { useAuth } from "../context/AuthContext";
import "../pages/Auth.css";

export default function Auth() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setLoading(true);

      if (isLogin) {
        const data = await loginUser(form.email, form.password);
        login(data.access_token);
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
        <div className="auth-left">
          <img src="src/assets/logo.svg" alt="NutryGym Logo" className="logo" />
        </div>

        <div className="auth-right">
          <h1>
            <span className="green">Welcome</span> Back!
          </h1>

          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <>
                <label>Name</label>
                <input
                  value={form.name}
                  onChange={(e) =>
                    setForm({ ...form, name: e.target.value })
                  }
                />
              </>
            )}

            <label>Email</label>
            <input
              value={form.email}
              onChange={(e) =>
                setForm({ ...form, email: e.target.value })
              }
            />

            <label>Password</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />

            <button disabled={loading}>
              {loading ? "Processing..." : isLogin ? "Login" : "Register"}
            </button>
          </form>

          <p className="switch">
            {isLogin ? "No account?" : "Already registered?"}
            <span onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? " Register" : " Login"}
            </span>
          </p>

          <Link to="/">← Back to home</Link>
        </div>
      </div>
    </div>
  );
}
