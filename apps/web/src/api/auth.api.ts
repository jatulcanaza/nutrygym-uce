import { createHttp } from "./http";

const AUTH_URL = import.meta.env.VITE_AUTH_API_URL;

if (!AUTH_URL) {
  console.error("VITE_AUTH_API_URL is missing in .env");
}

const authHttp = createHttp(AUTH_URL);

export async function loginUser(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  // Estos campos pueden ir vacíos, pero los dejamos por compatibilidad con OAuth2PasswordRequestForm
  formData.append("grant_type", "");
  formData.append("scope", "");
  formData.append("client_id", "");
  formData.append("client_secret", "");

  const response = await authHttp.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return response.data;
}

export async function registerUser(name: string, email: string, password: string) {
  const response = await authHttp.post("/auth/register", { name, email, password });
  return response.data;
}

export async function getMe(token: string) {
  const response = await authHttp.get("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}
