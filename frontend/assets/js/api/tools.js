import { apiRequest } from "./client.js";

export function submitVideoCompress(formData) {
  return apiRequest("/api/tools/video-compress", { method: "POST", body: formData });
}

export function submitVttSubtitle(formData) {
  return apiRequest("/api/tools/vtt-subtitle", { method: "POST", body: formData });
}

export function submitVideoSubtitleBurn(formData) {
  return apiRequest("/api/tools/video-subtitle-burn", { method: "POST", body: formData });
}

export function fetchToolRuns(limit = 8) {
  return apiRequest(`/api/tools/runs?limit=${limit}`);
}
