import { Link } from "react-router-dom";

export default function Plans() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Planes</h1>

      <div style={{ marginTop: "1rem" }}>
        <Link to="/nutrigym">
          <button>NutriGym</button>
        </Link>
      </div>
    </div>
  );
}
