import { createHttp } from "./http";

const nutritionHttp = createHttp(import.meta.env.VITE_NUTRITION_API_URL);

export async function createNutritionForm(token: string, payload: any) {
  const res = await nutritionHttp.post("/nutrition-form", payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}
