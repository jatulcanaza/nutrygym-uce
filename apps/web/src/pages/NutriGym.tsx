import { useNavigate } from "react-router-dom";

export default function NutriGym() {
  const isLogged = false; // luego se conecta al auth real
  const navigate = useNavigate();

  const handlePlan = () => {
    if (!isLogged) {
      navigate("/auth");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>NutriGym</h1>
      <p>
        Obtén tu plan nutricional personalizado basado en tus objetivos.
      </p>

      <button onClick={handlePlan}>
        Quiero mi plan nutricional
      </button>
    </div>
  );
}
