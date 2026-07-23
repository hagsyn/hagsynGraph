import { API } from "../config.js?v=20260707-login-api-fix";
import { clearAuthSession, getAuthToken } from "../state/store.js";

export function buildApiError({ status = 0, detail = "", fallbackMessage = "REQUEST_FAILED" } = {}) {
  const error = new Error(fallbackMessage);
  error.name = "ApiError";
  error.status = status;
  error.detail = typeof detail === "string" ? detail : "";
  return error;
}

export async function apiRequest(path, { method = "GET", body, headers = {} } = {}) {
  // Centralize auth header injection and response decoding so page/tool modules
  // can stay focused on interaction flow instead of fetch boilerplate.
  const token = getAuthToken();
  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};
  let response;
  try {
    response = await fetch(`${API}${path}`, {
      method,
      body,
      headers: { ...authHeaders, ...headers },
    });
  } catch (error) {
    throw buildApiError({
      status: 0,
      detail: error instanceof Error ? error.message : String(error || ""),
      fallbackMessage: "NETWORK_ERROR",
    });
  }
  if (response.status === 401 && token) {
    clearAuthSession();
    if (window.location.hash !== "#login") {
      window.location.hash = "#login";
    }
  }
  const contentType = response.headers.get("content-type") || "";
  if (!response.ok) {
    if (contentType.includes("application/json")) {
      const payload = await response.json();
      throw buildApiError({
        status: response.status,
        detail: payload.detail || JSON.stringify(payload),
      });
    }
    throw buildApiError({
      status: response.status,
      detail: await response.text(),
    });
  }
  return contentType.includes("application/json") ? response.json() : response;
}

export async function authJson(path, payload) {
  return apiRequest(path, {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });
}

export async function downloadBlob(downloadUrl, fallbackName) {
  // Browser downloads are funneled through fetch first so protected artifact
  // endpoints can still use the same Bearer token flow as API requests.
  const token = getAuthToken();
  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await fetch(`${API}${downloadUrl}`, { headers: authHeaders });
  if (!response.ok) {
    throw buildApiError({
      status: response.status,
      detail: await response.text(),
      fallbackMessage: "DOWNLOAD_FAILED",
    });
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = fallbackName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
