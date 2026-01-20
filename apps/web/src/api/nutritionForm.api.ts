// src/api/nutritionForm.api.ts
import { api } from "./client";

export type NutritionFormPayload = {
  meals_per_day: number;
  diet_type: string;
  allergies: string[];
  preferences: string[];
  caloric_goal: number;
  water_intake: number;
};

export type NutritionFormResponse = NutritionFormPayload & {
  id: string;
  user_id: string;
};

export async function getMyNutritionForm(token: string): Promise<NutritionFormResponse> {
  const res = await api.get("/api/nutrition/nutrition-form/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function createNutritionForm(
  token: string,
  payload: NutritionFormPayload
): Promise<NutritionFormResponse> {
  const res = await api.post("/api/nutrition/nutrition-form", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function updateMyNutritionForm(
  token: string,
  payload: NutritionFormPayload
): Promise<NutritionFormResponse> {
  const res = await api.put("/api/nutrition/nutrition-form/me", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function deleteMyNutritionForm(token: string): Promise<void> {
  await api.delete("/api/nutrition/nutrition-form/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
