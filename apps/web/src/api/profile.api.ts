// src/api/profile.api.ts
import { api } from "./client";

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
  const res = await api.get("/api/profile/profiles/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

export async function createProfile(
  token: string,
  payload: ProfilePayload
): Promise<ProfileResponse> {
  const res = await api.post("/api/profile/profiles", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

export async function updateMyProfile(
  token: string,
  payload: ProfilePayload
): Promise<ProfileResponse> {
  const res = await api.put("/api/profile/profiles/me", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as ProfileResponse;
}

export async function deleteMyProfile(token: string): Promise<{ detail: string }> {
  const res = await api.delete("/api/profile/profiles/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as { detail: string };
}
