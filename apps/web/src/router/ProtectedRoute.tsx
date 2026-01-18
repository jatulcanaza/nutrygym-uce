import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import type { Role } from "../api/authorization.api";

export function ProtectedRoute({
  children,
  allowedRoles,
}: {
  children: React.ReactNode;
  allowedRoles: Role[];
}) {
  const { isAuthenticated, role, isLoadingRole } = useAuth();

  // 1) No logueado => NotAuthorized (no mandarlo al login)
  if (!isAuthenticated) return <Navigate to="/not-authorized" replace />;

  // 2) Esperar rol sin parpadeo
  if (isLoadingRole) return <div style={{ padding: 24 }}>Loading...</div>;

  // 3) Si no hay rol o no está permitido => NotAuthorized
  if (!role) return <Navigate to="/not-authorized" replace />;
  if (!allowedRoles.includes(role)) return <Navigate to="/not-authorized" replace />;

  return <>{children}</>;
}
