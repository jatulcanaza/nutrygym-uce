import { createHttp } from "./http";

const PROFILE_URL = import.meta.env.VITE_PROFILE_API_URL;

if (!PROFILE_URL) {
  throw new Error("VITE_PROFILE_API_URL is missing in .env");
}

const profileHttp = createHttp(PROFILE_URL);

export type ProfilePayload = {
  first_name: string;
  last_name: string;
  birth_date: string; // YYYY-MM-DD
  gender: string;
  height_cm: number;
  weight_kg: number;
  goal: string;
  activity_level: string;
};

export type ProfileResponse = ProfilePayload & {
  id: string;
  user_id: string;
};

export async function getMyProfile(token: string): Promise<ProfileResponse> {
  const res = await profileHttp.get("/profiles/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

export async function createProfile(
  token: string,
  payload: ProfilePayload
): Promise<ProfileResponse> {
  const res = await profileHttp.post("/profiles", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

/**
 * Actualiza el perfil del usuario autenticado.
 * Requiere backend: PUT /profiles/me
 */
export async function updateMyProfile(
  token: string,
  payload: ProfilePayload
): Promise<ProfileResponse> {
  const res = await profileHttp.put("/profiles/me", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

/**
 * Elimina el perfil del usuario autenticado.
 * Requiere backend: DELETE /profiles/me
 */
export async function deleteMyProfile(token: string): Promise<{ detail: string }> {
  const res = await profileHttp.delete("/profiles/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as { detail: string };
}
