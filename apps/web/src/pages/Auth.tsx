import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, registerUser } from "../api/auth.api";
import { useAuth } from "../context/AuthContext";
import "../pages/Auth.css";

export default function Auth() {
  const navigate = useNavigate();
  const { login, role, isLoadingRole, isAuthenticated } = useAuth();

  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    if (!isAuthenticated) return;
    if (isLoadingRole) return;
    if (!role) return;

    if (role === "ADMIN") navigate("/admin", { replace: true });
    if (role === "ESTUDIANTE") navigate("/nutrigym", { replace: true });
  }, [isAuthenticated, isLoadingRole, role, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    console.log("[Auth] submit fired", { isLogin, email: form.email });

    try {
      setLoading(true);

      if (isLogin) {
        console.log("[Auth] calling /auth/login ...");
        const data = await loginUser(form.email, form.password);
        console.log("[Auth] login OK:", data);

        login(data.access_token);
      } else {
        console.log("[Auth] calling /auth/register ...");
        const data = await registerUser(form.name, form.email, form.password);
        console.log("[Auth] register OK:", data);
      }
    } catch (error: any) {
      console.error("[Auth] error:", error);

      // Para ver el error real del backend:
      const status = error?.response?.status;
      const detail = error?.response?.data;
      alert(`Auth error (${status ?? "no-status"}): ${JSON.stringify(detail)}`);
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
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </>
            )}

            <label>Email</label>
            <input
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />

            <label>Password</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />

            {/* NO bloquear login por rol */}
            <button disabled={loading}>
              {loading ? "Processing..." : isLogin ? "Login" : "Register"}
            </button>

            {isAuthenticated && isLoadingRole && (
              <p style={{ marginTop: 12 }}>Loading role...</p>
            )}
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
