import { createHttp } from "./http";

const NUTRITION_FORM_URL = import.meta.env.VITE_NUTRITION_FORM_API_URL;

if (!NUTRITION_FORM_URL) {
  throw new Error("VITE_NUTRITION_FORM_API_URL is missing in .env");
}

const nutritionHttp = createHttp(NUTRITION_FORM_URL);

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
  const res = await nutritionHttp.get("/nutrition-form/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function createNutritionForm(
  token: string,
  payload: NutritionFormPayload
): Promise<NutritionFormResponse> {
  const res = await nutritionHttp.post("/nutrition-form", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function updateMyNutritionForm(
  token: string,
  payload: NutritionFormPayload
): Promise<NutritionFormResponse> {
  const res = await nutritionHttp.put("/nutrition-form/me", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data as NutritionFormResponse;
}

export async function deleteMyNutritionForm(token: string): Promise<void> {
  await nutritionHttp.delete("/nutrition-form/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
