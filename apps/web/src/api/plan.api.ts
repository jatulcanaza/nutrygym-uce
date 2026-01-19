// src/api/plan.api.ts
import { createHttp } from "./http";

const baseURL =
  import.meta.env.VITE_PLAN_MANAGEMENT_URL || "http://localhost:3005";

console.log("[ENV] VITE_PLAN_MANAGEMENT_URL =", import.meta.env.VITE_PLAN_MANAGEMENT_URL);
console.log("[Plan API] baseURL =", baseURL);


const http = createHttp(baseURL);

export type MealPlan = {
  id: string;
  user_id: string;
  title: string;
  description: string;
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  status: string; // active/archived/draft (según backend)
  version: number;
  is_current: boolean;
  created_at: string; // ISO
  updated_at: string | null;
};

function authHeaders(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export async function getMyPlans(token: string): Promise<MealPlan[]> {
  const res = await http.get<MealPlan[]>("/plans", {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function getCurrentPlan(token: string): Promise<MealPlan> {
  const res = await http.get<MealPlan>("/plans/current", {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function generatePlan(token: string): Promise<MealPlan> {
  // Plan Management ya toma profile + nutrition-form internamente
  const res = await http.post<MealPlan>("/plans/generate", null, {
    headers: authHeaders(token),
  });
  return res.data;
}
export async function deletePlan(token: string, planId: string): Promise<void> {
  await http.delete(`/plans/${planId}`, {
    headers: authHeaders(token),
  });
}
export async function updatePlan(
  token: string,
  planId: string,
  data: Partial<MealPlan>
): Promise<MealPlan> {
  const res = await http.put<MealPlan>(`/plans/${planId}`, data, {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function archivePlan(token: string, planId: string) {
  const res = await http.put(
    `/plans/${planId}`,
    { status: "archived", is_current: false },
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function endPlan(token: string): Promise<MealPlan> {
  const res = await http.post<MealPlan>(
    "/plans/current/end",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function cancelPlan(token: string): Promise<MealPlan> {
  const res = await http.post<MealPlan>(
    "/plans/current/cancel",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function regenerateCurrentPlan(token: string): Promise<MealPlan> {
  const res = await http.post<MealPlan>(
    "/plans/current/regenerate",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}
