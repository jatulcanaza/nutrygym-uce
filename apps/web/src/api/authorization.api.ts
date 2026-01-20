// src/api/authorization.api.ts
import { api } from "./client";

export type Role = "ADMIN" | "ESTUDIANTE";

/**
 * Obtiene el rol del usuario autenticado
 * Backend: GET /authorize/my-role
 */
export async function getMyRole(token: string): Promise<Role> {
  const res = await api.get("/api/authz/authorize/my-role", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return res.data.role as Role;
}
