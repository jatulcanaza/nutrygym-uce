// apps/web/src/api/client.ts
import { createHttp } from "./http";

// Base URL vacío = mismo host/puerto donde está el frontend (gateway)
// Ej: http://localhost:8080
export const api = createHttp("");
