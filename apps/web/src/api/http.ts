import axios from "axios";

export function createHttp(baseURL: string) {
  const http = axios.create({ baseURL });

  // Si vas a usar token, lo ideal es NO forzar Content-Type aquí.
  // Axios lo setea automáticamente según el body (JSON, form, etc.)
  http.defaults.headers.common["Accept"] = "application/json";

  return http;
}
