import { createHttp } from "./http";

const profileHttp = createHttp(import.meta.env.VITE_PROFILE_API_URL);

export async function getMyProfile(token: string) {
  const res = await profileHttp.get("/profiles/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function createProfile(token: string, payload: any) {
  const res = await profileHttp.post("/profiles", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}
