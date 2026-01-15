import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function NutriGym() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handlePlan = () => {
    if (!isAuthenticated) {
      navigate("/auth");
    } else {
      navigate("/nutrition-form");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      {isAuthenticated ? (
        <h2>
          Bienvenido {user?.email.split("@")[0]} 👋
        </h2>
      ) : (
        <h2>Bienvenido 👋</h2>
      )}

      <p>Tu plataforma inteligente de nutrición para estudiantes de la UCE.</p>

      <button onClick={handlePlan}>
        Quiero mi plan nutricional
      </button>

      {isAuthenticated && (
        <button onClick={logout} style={{ marginLeft: "1rem" }}>
          Cerrar sesión
        </button>
      )}
    </div>
  );
}
