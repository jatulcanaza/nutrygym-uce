// src/api/auth.api.ts
import { api } from "./client";

export async function loginUser(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  // Compatibilidad con OAuth2PasswordRequestForm
  formData.append("grant_type", "");
  formData.append("scope", "");
  formData.append("client_id", "");
  formData.append("client_secret", "");

  const response = await api.post("/api/auth/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return response.data;
}

export async function registerUser(name: string, email: string, password: string) {
  const response = await api.post("/api/auth/auth/register", { name, email, password });
  return response.data;
}

export async function getMe(token: string) {
  const response = await api.get("/api/auth/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}
