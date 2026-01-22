// src/pages/Auth.tsx
import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, registerUser } from "../api/auth.api";
import { useAuth } from "../context/AuthContext";
import "../pages/auth.css";

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

  const [errorMsg, setErrorMsg] = useState<string>("");
  const [successMsg, setSuccessMsg] = useState<string>("");

  const [fieldErrors, setFieldErrors] = useState<{
    name?: string;
    email?: string;
    password?: string;
  }>({});

  // ✅ Solo UCE en REGISTER
  const isUceEmail = (email: string) => {
    const e = email.trim().toLowerCase();
    return /^[^\s@]+@uce\.edu\.ec$/.test(e);
  };

  const isValidEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());

  // Si ya está autenticado y ya tenemos role, redirigir automáticamente
  useEffect(() => {
    if (!isAuthenticated) return;
    if (isLoadingRole) return;
    if (!role) return;

    if (role === "ADMIN") navigate("/admin", { replace: true });
    if (role === "ESTUDIANTE") navigate("/nutrigym", { replace: true });
  }, [isAuthenticated, isLoadingRole, role, navigate]);

  // ✅ Cuando cambias Login/Register: limpia form y mensajes (para que no se queden email/password)
  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    setErrorMsg("");
    setSuccessMsg("");
    setFieldErrors({});
    setForm({ name: "", email: "", password: "" });
  };

  const validate = () => {
    const e: { name?: string; email?: string; password?: string } = {};

    if (!isLogin && !form.name.trim()) e.name = "Name is required.";

    if (!form.email.trim()) e.email = "Email is required.";
    else if (!isValidEmail(form.email)) e.email = "Please enter a valid email.";

    // ✅ Restricción de dominio SOLO en register
    if (!isLogin && form.email.trim() && !isUceEmail(form.email)) {
      e.email = "Invalid email. Use your @uce.edu.ec email.";
    }

    if (!form.password.trim()) e.password = "Password is required.";
    else if (!isLogin && form.password.length < 8) {
      e.password = "Password must be at least 8 characters.";
    }

    setFieldErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Limpia banners al enviar
    setErrorMsg("");
    setSuccessMsg("");

    // ✅ Validación frontend
    if (!validate()) return;

    try {
      setLoading(true);

      if (isLogin) {
        const data = await loginUser(form.email, form.password);
        login(data.access_token);
        // NO navegues aquí: dejamos que el useEffect redirija cuando role esté listo
      } else {
        await registerUser(form.name, form.email, form.password);

        setSuccessMsg("Account created successfully. You can now log in.");
        setIsLogin(true);
        setFieldErrors({});
        // ✅ Limpia todo (incluyendo email/password) al volver a login
        setForm({ name: "", email: "", password: "" });
      }
    } catch (error: any) {
      console.error("[Auth] error:", error);

      const status = error?.response?.status;
      const detail = error?.response?.data;

      // Mensajes amigables
      let msg = "Something went wrong. Please try again.";
      if (status === 401) msg = "Invalid email or password.";
      if (status === 409) msg = "This email is already registered.";
      if (status === 422) msg = "Please check the fields and try again.";

      // Si backend manda detail como string
      if (typeof detail?.detail === "string") msg = detail.detail;

      setSuccessMsg("");
      setErrorMsg(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        <div className="auth-left">
          <img src="/logo.svg" alt="NutryGym Logo" className="logo" />
        </div>

        <div className="auth-right">
          <h1>
            <span className="green">Welcome</span> Back!
          </h1>

          <form onSubmit={handleSubmit} className="auth-form">
            {errorMsg && (
              <div className="auth-alert auth-alert-error">{errorMsg}</div>
            )}
            {successMsg && (
              <div className="auth-alert auth-alert-success">{successMsg}</div>
            )}

            {!isLogin && (
              <>
                <label>Name</label>
                <input
                  value={form.name}
                  onChange={(e) => {
                    setForm({ ...form, name: e.target.value });
                    setErrorMsg("");
                    setSuccessMsg("");
                    setFieldErrors((prev) => ({ ...prev, name: undefined }));
                  }}
                  placeholder="Enter your full name"
                  autoComplete="name"
                  className={fieldErrors.name ? "input-error" : ""}
                />
                {fieldErrors.name && (
                  <small className="field-error">{fieldErrors.name}</small>
                )}
              </>
            )}

            <label>Email</label>
            <input
              value={form.email}
              onChange={(e) => {
                setForm({ ...form, email: e.target.value });
                setErrorMsg("");
                setSuccessMsg("");
                setFieldErrors((prev) => ({ ...prev, email: undefined }));
              }}
              placeholder={isLogin ? "Enter your email" : "Enter your @uce.edu.ec email"}
              autoComplete="email"
              className={fieldErrors.email ? "input-error" : ""}
            />
            {fieldErrors.email && (
              <small className="field-error">{fieldErrors.email}</small>
            )}

            <label>Password</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => {
                setForm({ ...form, password: e.target.value });
                setErrorMsg("");
                setSuccessMsg("");
                setFieldErrors((prev) => ({ ...prev, password: undefined }));
              }}
              placeholder="Enter your password"
              autoComplete={isLogin ? "current-password" : "new-password"}
              className={fieldErrors.password ? "input-error" : ""}
            />
            {fieldErrors.password && (
              <small className="field-error">{fieldErrors.password}</small>
            )}

            <button disabled={loading}>
              {loading ? "Processing..." : isLogin ? "Login" : "Register"}
            </button>

            {isAuthenticated && isLoadingRole && (
              <p style={{ marginTop: 12 }}>Loading role...</p>
            )}
          </form>

          <p className="switch">
            {isLogin ? "No account?" : "Already registered?"}
            <span onClick={toggleMode}>{isLogin ? " Register" : " Login"}</span>
          </p>

          <Link to="/">← Back to home</Link>
        </div>
      </div>
    </div>
  );
}
