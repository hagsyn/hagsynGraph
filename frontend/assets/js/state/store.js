export const state = {
  current: "dashboard",
  toolRoute: "",
  authRoute: "",
  activeTheme: localStorage.getItem("hagsyn_theme") || "midnight",
  locale: "zh-CN",
  modalState: null,
  toastId: 0,
  latestResult: null,
  latestSubtitleResult: null,
  latestBurnedVideoResult: null,
  selectedVideoFile: null,
  selectedSubtitleFile: null,
  selectedBurnFile: null,
  selectedVideoMode: "balanced",
  selectedSubtitleLanguage: "auto",
  selectedBurnLanguage: "auto",
  toolRuns: [],
  subtitleProgressTimer: null,
  burnProgressTimer: null,
  userMenuOpen: false,
  storagePolicyPanelOpen: false,
  storageCleanupActivity: [],
  authUser: null,
  authChecked: false,
};

export function getCurrentUser() {
  const role = localStorage.getItem("hagsyn_user_role") || "guest";
  const username = localStorage.getItem("hagsyn_user_name") || "guest";
  return { username, role };
}

export function isAdminUser() {
  return getCurrentUser().role === "admin";
}

export function getAuthToken() {
  return localStorage.getItem("hagsyn_token") || "";
}

export function setAuthSession({ token, user }) {
  localStorage.setItem("hagsyn_token", token);
  localStorage.setItem("hagsyn_user_name", user.username);
  localStorage.setItem("hagsyn_user_role", user.isAdmin ? "admin" : (user.role || "user"));
  state.authUser = user;
  state.authChecked = true;
}

export function clearAuthSession() {
  localStorage.removeItem("hagsyn_token");
  localStorage.removeItem("hagsyn_user_name");
  localStorage.removeItem("hagsyn_user_role");
  state.authUser = null;
  state.authChecked = true;
}

export function getDefaultStoragePolicy() {
  return {
    autoCleanupEnabled: true,
    uploadRetentionHours: 72,
    compressedRetentionHours: 168,
    subtitleRetentionHours: 168,
    toolRunRetentionHours: 24 * 30,
    deleteIntermediateAudio: true,
    cleanupFailedTemporaryFiles: true,
  };
}
