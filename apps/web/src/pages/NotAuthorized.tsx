import { Link } from "react-router-dom";

export default function NotAuthorized() {
  return (
    <section style={{ padding: 24 }}>
      <h1>Not authorized</h1>
      <p>You do not have permission to access this page.</p>
      <Link to="/">Go home</Link>
    </section>
  );
}
