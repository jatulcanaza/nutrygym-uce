import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function NotAuthorized() {
  const { isAuthenticated } = useAuth();

  return (
    <div style={{ padding: 24 }}>
      <h1>Not authorized</h1>

      {!isAuthenticated ? (
        <>
          <p>You must log in to access this page.</p>
          <Link to="/auth">Go to login</Link>
        </>
      ) : (
        <p>You don’t have the required permissions to access this page.</p>
      )}
    </div>
  );
}
