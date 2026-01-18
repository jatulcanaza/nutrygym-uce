import { createHttp } from "./http";

export type Role = "ADMIN" | "ESTUDIANTE";

const AUTHZ_URL = import.meta.env.VITE_AUTHZ_API_URL;

console.log("[ENV] VITE_AUTHZ_API_URL =", AUTHZ_URL);

if (!AUTHZ_URL) {
  throw new Error("VITE_AUTHZ_API_URL is missing in .env");
}

const authzHttp = createHttp(AUTHZ_URL);

/**
 * Obtiene el rol del usuario autenticado
 * desde /authorize/my-role
 */
export async function getMyRole(token: string): Promise<Role> {
  const res = await authzHttp.get("/authorize/my-role", {
    headers: { Authorization: `Bearer ${token}` },
  });

  // ✅ el backend devuelve un objeto → usamos solo el campo role
  return res.data.role as Role;
}
