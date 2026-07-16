import { apiRequest } from "./client.js";

export function adminApi(path, { method = "GET", body } = {}) {
  const headers = {};
  let requestBody = body;
  if (body && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    requestBody = JSON.stringify(body);
  }
  return apiRequest(path, { method, body: requestBody, headers });
}

export const loadStoragePolicy = () => adminApi("/api/admin/storage-policy");
export const saveStoragePolicy = (policy) => adminApi("/api/admin/storage-policy", { method: "PUT", body: policy });
export const runStorageCleanup = () => adminApi("/api/admin/storage-policy/run-cleanup", { method: "POST" });
