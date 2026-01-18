import { useAuth } from "../context/AuthContext";

export default function AdminGym() {
  const { user, logout } = useAuth();

  return (
    <section style={{ padding: 24 }}>
      <h1>AdminGym</h1>
      <p>Welcome, {user?.email}</p>

      <button onClick={logout} type="button">
        Log out
      </button>
    </section>
  );
}
