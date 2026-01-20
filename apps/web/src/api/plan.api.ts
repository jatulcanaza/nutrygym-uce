// src/api/plan.api.ts
import { api } from "./client";

export type MealPlan = {
  id: string;
  user_id: string;
  title: string;
  description: string;
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  status: string;
  version: number;
  is_current: boolean;
  created_at: string;
  updated_at: string | null;
};

function authHeaders(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export async function getMyPlans(token: string): Promise<MealPlan[]> {
  const res = await api.get<MealPlan[]>("/api/plans/plans", {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function getCurrentPlan(token: string): Promise<MealPlan> {
  const res = await api.get<MealPlan>("/api/plans/plans/current", {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function generatePlan(token: string): Promise<MealPlan> {
  const res = await api.post<MealPlan>("/api/plans/plans/generate", null, {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function deletePlan(token: string, planId: string): Promise<void> {
  await api.delete(`/api/plans/plans/${planId}`, {
    headers: authHeaders(token),
  });
}

export async function updatePlan(
  token: string,
  planId: string,
  data: Partial<MealPlan>
): Promise<MealPlan> {
  const res = await api.put<MealPlan>(`/api/plans/plans/${planId}`, data, {
    headers: authHeaders(token),
  });
  return res.data;
}

export async function archivePlan(token: string, planId: string) {
  const res = await api.put(
    `/api/plans/plans/${planId}`,
    { status: "archived", is_current: false },
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function endPlan(token: string): Promise<MealPlan> {
  const res = await api.post<MealPlan>(
    "/api/plans/plans/current/end",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function cancelPlan(token: string): Promise<MealPlan> {
  const res = await api.post<MealPlan>(
    "/api/plans/plans/current/cancel",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}

export async function regenerateCurrentPlan(token: string): Promise<MealPlan> {
  const res = await api.post<MealPlan>(
    "/api/plans/plans/current/regenerate",
    null,
    { headers: authHeaders(token) }
  );
  return res.data;
}
