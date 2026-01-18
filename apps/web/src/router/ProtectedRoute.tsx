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

  if (!isAuthenticated) return <Navigate to="/auth" replace />;

  // Evita parpadeo mientras carga el rol
  if (isLoadingRole) return <div style={{ padding: 24 }}>Loading...</div>;

  // Si no hay rol o no está permitido
  if (!role) return <Navigate to="/auth" replace />;
  if (!allowedRoles.includes(role)) return <Navigate to="/not-authorized" replace />;

  return <>{children}</>;
}
