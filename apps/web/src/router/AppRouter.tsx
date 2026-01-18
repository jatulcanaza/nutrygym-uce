import { Routes, Route } from "react-router-dom";
import Welcome from "../pages/Welcome";
import About from "../pages/About";
import Plans from "../pages/Plans";
import NutriGym from "../pages/NutriGym";
import Auth from "../pages/Auth";
import AdminGym from "../pages/AdminGym";
import NotAuthorized from "../pages/NotAuthorized";
import { ProtectedRoute } from "./ProtectedRoute";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/about" element={<About />} />
      <Route path="/plans" element={<Plans />} />
      <Route path="/auth" element={<Auth />} />

      <Route path="/not-authorized" element={<NotAuthorized />} />

      <Route
        path="/nutrigym"
        element={
          <ProtectedRoute allowedRoles={["ESTUDIANTE"]}>
            <NutriGym />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRoles={["ADMIN"]}>
            <AdminGym />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
