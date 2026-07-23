import { fetchToolRuns, submitVideoCompress, submitVideoSubtitleBurn, submitVttSubtitle } from "./api/tools.js";
import { apiRequest, authJson, downloadBlob } from "./api/client.js?v=20260707-login-api-fix";
import { loadStoragePolicy, runStorageCleanup, saveStoragePolicy } from "./api/admin.js";
import { API, pages, themes, tools as toolDefinitions } from "./config.js?v=20260707-login-api-fix";
import { renderLanguageSwitcherMarkup } from "./components/language-switcher.js";
import { renderModalMarkup } from "./components/modal.js";
import { renderCleanupActivityMarkup } from "./components/storage-policy-panel.js";
import { renderThemeSwitcherMarkup } from "./components/theme-switcher.js";
import { renderToastMarkup } from "./components/toast.js";
import { applyUserIdentity } from "./components/user-menu.js";
import { DEFAULT_LOCALE, SUPPORTED_LOCALES, getLocale, setLocale, t } from "./i18n/index.js";
import { state, clearAuthSession, getAuthToken, getCurrentUser, getDefaultStoragePolicy, isAdminUser, setAuthSession } from "./state/store.js";
import { renderBurnWorkspace } from "./tools/video-subtitle-burn.js";
import { renderVideoWorkspace } from "./tools/video-compress.js";
import { renderSubtitleWorkspace } from "./tools/vtt-subtitle.js";
import { toHistoryMessage, toUserMessage } from "./utils/errors.js";
import { formatBytes, formatDateTime, esc } from "./utils/format.js";
import { parseRoute, syncRoute } from "./utils/router.js";
import { renderDashboardView } from "./views/dashboard.js?v=20260707-login-minimal";
import { renderGraphView } from "./views/graph.js?v=20260707-login-minimal";
import { renderNodesView } from "./views/nodes.js?v=20260707-login-minimal";
import { renderRoadmapsView } from "./views/roadmaps.js?v=20260707-login-minimal";
import { renderAuthView } from "./views/auth.js?v=20260707-login-minimal";
import { renderToolsView } from "./views/tools.js?v=20260707-login-minimal";

const initialRoute = parseRoute();
state.current = initialRoute.page;
state.toolRoute = initialRoute.toolId;
state.locale = setLocale(getLocale() || DEFAULT_LOCALE);

function isAuthRoute(page) {
  return page === "login" || page === "register";
}

const nav = document.getElementById("nav");

function localizeTool(definition) {
  return {
    ...definition,
    title: t(definition.titleKey),
    status: t(definition.statusKey),
    summary: t(definition.summaryKey),
    detail: t(definition.detailKey),
    modes: (definition.modeKeys || []).map((key) => t(key)),
  };
}

function getTools() {
  return toolDefinitions.map(localizeTool);
}

function getTool(toolId) {
  return getTools().find((tool) => tool.id === toolId);
}

function renderNav() {
  nav.innerHTML = "";
  pages.forEach((key) => {
    const button = document.createElement("button");
    button.textContent = t(`nav.${key}`);
    button.dataset.page = key;
    button.onclick = () => show(key);
    nav.appendChild(button);
  });
}

function renderThemeSwitcher() {
  const root = document.getElementById("themeSwitcher");
  root.setAttribute("aria-label", t("theme.switcher"));
  root.innerHTML = renderThemeSwitcherMarkup(themes, state.activeTheme);
}

function renderLanguageSwitcher() {
  const root = document.getElementById("languageSwitcher");
  root.setAttribute("aria-label", t("locale.switcher"));
  root.innerHTML = renderLanguageSwitcherMarkup(SUPPORTED_LOCALES, state.locale, (locale) => t(`locale.${locale}`));
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function setShellCopy() {
  setText("shellTagline", t("brand.tagline"));
  const adminButton = document.getElementById("adminSettingsEntry");
  if (adminButton) {
    adminButton.setAttribute("aria-label", t("userMenu.adminSettings"));
    adminButton.setAttribute("title", t("userMenu.adminSettings"));
  }
  const mobileNavToggle = document.getElementById("mobileNavToggle");
  if (mobileNavToggle) {
    mobileNavToggle.setAttribute("aria-label", t("nav.mobile.open"));
    mobileNavToggle.setAttribute("title", t("nav.mobile.open"));
  }
  const mobileNavClose = document.getElementById("mobileNavClose");
  if (mobileNavClose) {
    mobileNavClose.setAttribute("aria-label", t("nav.mobile.close"));
    mobileNavClose.setAttribute("title", t("nav.mobile.close"));
  }
  setText("userAccountButton", t("userMenu.account"));
  setText("userSettingsButton", t("userMenu.settings"));
  setText("userLogoutButton", t("userMenu.logout"));

  setText("storagePolicyTitle", t("settings.title"));
  setText("storagePolicyIntro", t("settings.helper"));
  setText("storageMetricAdminLabel", t("settings.metric.admin"));
  setText("storageMetricAdminValue", t("common.status.enabled"));
  setText("storageMetricCleanupLabel", t("settings.metric.cleanup"));
  setText("storageMetricSourceLabel", t("settings.metric.source"));
  setText("storageMetricSourceValue", t("common.status.backendConfig"));
  setText("storageRetentionTitle", t("settings.retention.title"));
  setText("storageRetentionBadge", t("common.status.backendConfig"));
  setText("storageUploadRetentionLabel", t("settings.uploadRetention"));
  setText("storageCompressedRetentionLabel", t("settings.compressedRetention"));
  setText("storageSubtitleRetentionLabel", t("settings.subtitleRetention"));
  setText("storageToolRunRetentionLabel", t("settings.toolRunRetention"));
  setText("storageCleanupRulesTitle", t("settings.cleanupRules.title"));
  setText("storageCleanupRulesHelper", t("settings.cleanupRules.helper"));
  setText("storageAutoCleanupTitle", t("settings.autoCleanup.title"));
  setText("storageAutoCleanupDesc", t("settings.autoCleanup.desc"));
  setText("storageDeleteAudioTitle", t("settings.deleteAudio.title"));
  setText("storageDeleteAudioDesc", t("settings.deleteAudio.desc"));
  setText("storageCleanupFailedTitle", t("settings.cleanupFailed.title"));
  setText("storageCleanupFailedDesc", t("settings.cleanupFailed.desc"));
  setText("storageAboutTitle", t("settings.about.title"));
  setText("storageAboutBadge", t("common.realApi"));
  setText("storageAboutHelper", t("settings.about.helper"));
  setText("cleanupActivityTitle", t("settings.activity.title"));
  setText("cleanupActivityHelper", t("settings.activity.helper"));
  setText("manualCleanupButton", t("settings.manualCleanup"));
  setText("reloadStoragePolicyButton", t("settings.reload"));
  setText("saveStoragePolicyButton", t("settings.save"));
  const closeSettings = document.getElementById("closeStoragePolicyPanel");
  if (closeSettings) closeSettings.setAttribute("aria-label", t("settings.close"));
}

function renderChrome() {
  renderNav();
  renderThemeSwitcher();
  renderLanguageSwitcher();
  setShellCopy();
  syncUserIdentity();
  renderCleanupActivity();
}

function toast({ title, message, type = "success" }) {
  const id = `toast-${++state.toastId}`;
  const stack = document.getElementById("toastStack");
  const wrapper = document.createElement("div");
  wrapper.innerHTML = renderToastMarkup({ title, message, type }, id);
  stack.appendChild(wrapper.firstChild);
  setTimeout(() => document.getElementById(id)?.remove(), 3200);
}

function renderModal() {
  const root = document.getElementById("modalRoot");
  if (!state.modalState) {
    root.className = "modal-root";
    root.innerHTML = "";
    return;
  }
  root.className = "modal-root open";
  root.innerHTML = renderModalMarkup(state.modalState);
}

function showModal({ title, message, actions }) {
  state.modalState = { title, message, actions };
  renderModal();
}

function closeModal() {
  state.modalState = null;
  renderModal();
}

async function runModalAction(index) {
  if (!state.modalState) return;
  const action = state.modalState.actions[index];
  if (action?.closeOnClick !== false) closeModal();
  if (action?.handler) await action.handler();
}

function updateShellForRoute() {
  const appEl = document.querySelector(".app");
  const mainEl = document.querySelector("main");
  const navEl = document.getElementById("nav");
  const languageSwitcher = document.getElementById("languageSwitcher");
  const userButton = document.getElementById("userMenuButton");
  const adminEntry = document.getElementById("adminSettingsEntry");
  const mobileNavToggle = document.getElementById("mobileNavToggle");
  const isAuthOnly = isAuthRoute(state.current);
  if (appEl) appEl.classList.toggle("auth-route", isAuthOnly);
  if (mainEl) mainEl.classList.toggle("auth-main", isAuthOnly);
  if (navEl) navEl.style.display = isAuthOnly ? "none" : "grid";
  if (languageSwitcher) languageSwitcher.style.display = "flex";
  if (userButton) userButton.style.display = isAuthOnly ? "none" : "flex";
  if (adminEntry && isAuthOnly) adminEntry.style.display = "none";
  if (mobileNavToggle) mobileNavToggle.style.display = isAuthOnly ? "none" : "";
}

function applyTheme(name) {
  state.activeTheme = themes[name] ? name : "midnight";
  document.documentElement.setAttribute("data-theme", state.activeTheme);
  localStorage.setItem("hagsyn_theme", state.activeTheme);
  renderThemeSwitcher();
}

async function setAppLocale(locale) {
  state.locale = setLocale(locale);
  renderChrome();
  await show(state.current, state.toolRoute);
}

function setUserMenu(open) {
  state.userMenuOpen = open;
  const button = document.getElementById("userMenuButton");
  const menu = document.getElementById("userMenu");
  if (!button || !menu) return;
  button.classList.toggle("open", open);
  button.setAttribute("aria-expanded", String(open));
  menu.classList.toggle("open", open);
}

function setMobileNav(open) {
  state.mobileNavOpen = open;
  document.querySelector(".app")?.classList.toggle("mobile-nav-open", open);
  const toggle = document.getElementById("mobileNavToggle");
  if (toggle) toggle.setAttribute("aria-expanded", String(open));
  const scrim = document.getElementById("mobileNavScrim");
  if (scrim) scrim.hidden = !open;
}

function closeMobileNav() {
  if (!state.mobileNavOpen) return;
  setMobileNav(false);
}

function toggleMobileNav(event) {
  if (event) event.stopPropagation();
  setUserMenu(false);
  setMobileNav(!state.mobileNavOpen);
}

function syncUserIdentity() {
  const user = getCurrentUser();
  applyUserIdentity({ ...user, isAdmin: isAdminUser() });
  updateShellForRoute();
}

function renderCleanupActivity() {
  const list = document.getElementById("cleanupActivityList");
  const lastRun = document.getElementById("cleanupLastRun");
  if (!list || !lastRun) return;
  const payload = renderCleanupActivityMarkup(state.storageCleanupActivity);
  list.innerHTML = payload.html;
  if (!state.storageCleanupActivity.length) {
    lastRun.textContent = t("common.status.notRunYet");
    return;
  }
  lastRun.textContent = payload.lastRun;
}

function setStoragePolicyStatus(text) {
  const status = document.getElementById("storagePolicyStatus");
  if (status) status.textContent = text;
}

function setStoragePolicyPanel(open) {
  state.storagePolicyPanelOpen = open;
  const root = document.getElementById("settingsPanelRoot");
  const panel = document.getElementById("storagePolicyPanel");
  if (!root || !panel) return;
  root.className = open ? "modal-root open" : "modal-root";
  root.setAttribute("aria-hidden", String(!open));
  panel.classList.toggle("open", open);
}

async function loadStoragePolicySettings() {
  if (!isAdminUser()) return;
  const payload = await loadStoragePolicy();
  const policy = { ...getDefaultStoragePolicy(), ...(payload.policy || {}) };
  document.getElementById("storageUploadRetentionHours").value = String(policy.uploadRetentionHours);
  document.getElementById("storageCompressedRetentionHours").value = String(policy.compressedRetentionHours);
  document.getElementById("storageSubtitleRetentionHours").value = String(policy.subtitleRetentionHours);
  document.getElementById("storageToolRunRetentionHours").value = String(policy.toolRunRetentionHours);
  document.getElementById("storageAutoCleanupEnabled").checked = Boolean(policy.autoCleanupEnabled);
  document.getElementById("storageDeleteIntermediateAudio").checked = Boolean(policy.deleteIntermediateAudio);
  document.getElementById("storageCleanupFailedTemporaryFiles").checked = Boolean(policy.cleanupFailedTemporaryFiles);
  setStoragePolicyStatus(t("settings.status.loaded"));
  renderCleanupActivity();
}

async function openStoragePolicyPanel() {
  if (!isAdminUser()) return;
  setUserMenu(false);
  setStoragePolicyPanel(true);
  try {
    await loadStoragePolicySettings();
  } catch (error) {
    console.error(error);
    setStoragePolicyStatus(t("settings.status.unavailable"));
    toast({ title: t("settings.loadFail.title"), message: t("settings.loadFail.message"), type: "error" });
  }
}

function closeStoragePolicyPanel() {
  setStoragePolicyPanel(false);
}

async function saveStoragePolicySettings(event) {
  event.preventDefault();
  if (!isAdminUser()) return;
  const policy = {
    autoCleanupEnabled: document.getElementById("storageAutoCleanupEnabled").checked,
    uploadRetentionHours: Number(document.getElementById("storageUploadRetentionHours").value || getDefaultStoragePolicy().uploadRetentionHours),
    compressedRetentionHours: Number(document.getElementById("storageCompressedRetentionHours").value || getDefaultStoragePolicy().compressedRetentionHours),
    subtitleRetentionHours: Number(document.getElementById("storageSubtitleRetentionHours").value || getDefaultStoragePolicy().subtitleRetentionHours),
    toolRunRetentionHours: Number(document.getElementById("storageToolRunRetentionHours").value || getDefaultStoragePolicy().toolRunRetentionHours),
    deleteIntermediateAudio: document.getElementById("storageDeleteIntermediateAudio").checked,
    cleanupFailedTemporaryFiles: document.getElementById("storageCleanupFailedTemporaryFiles").checked,
  };
  await saveStoragePolicy(policy);
  setStoragePolicyStatus(t("settings.status.saved"));
  toast({ title: t("settings.saved.title"), message: t("settings.saved.message") });
}

async function runManualStorageCleanup() {
  if (!isAdminUser()) return;
  const result = await runStorageCleanup();
  const now = new Date().toISOString();
  state.storageCleanupActivity.unshift({
    timestamp: now,
    title: t("settings.cleanup.title", { count: result.filesDeleted }),
    message: t("settings.cleanup.message", { bytes: formatBytes(result.bytesFreed), directories: result.directories.join(" / ") }),
  });
  state.storageCleanupActivity = state.storageCleanupActivity.slice(0, 5);
  renderCleanupActivity();
  setStoragePolicyStatus(t("settings.status.lastCleanup", { time: formatDateTime(now) }));
  toast({ title: t("settings.cleanupDone.title"), message: t("settings.cleanupDone.message", { count: result.filesDeleted, bytes: formatBytes(result.bytesFreed) }) });
}

function toggleUserMenu(event) {
  if (event) event.stopPropagation();
  setUserMenu(!state.userMenuOpen);
}

function showAccountInfo() {
  setUserMenu(false);
  showModal({ title: t("userMenu.accountInfo.title"), message: t("userMenu.accountInfo.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
}

function showSettingsInfo() {
  setUserMenu(false);
  if (isAdminUser()) {
    openStoragePolicyPanel();
    return;
  }
  showModal({ title: t("userMenu.settingsInfo.title"), message: t("userMenu.settingsInfo.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
}

function handleLogout() {
  setUserMenu(false);
  clearAuthSession();
  syncUserIdentity();
  showModal({ title: t("userMenu.logout.title"), message: t("userMenu.logout.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  show("login");
}

function setPageMeta() {
  const titleMap = isAuthRoute(state.current) ? {
    login: [t("page.login.title"), t("page.login.subtitle")],
    register: [t("page.register.title"), t("page.register.subtitle")],
  } : {
    dashboard: [t("page.dashboard.title"), t("page.dashboard.subtitle")],
    tools: [t("page.tools.title"), t("page.tools.subtitle")],
    nodes: [t("page.nodes.title"), t("page.nodes.subtitle")],
    graph: [t("page.graph.title"), t("page.graph.subtitle")],
    roadmaps: [t("page.roadmaps.title"), t("page.roadmaps.subtitle")],
  }[state.current];
  document.getElementById("pageTitle").textContent = titleMap[0];
  document.getElementById("pageSubtitle").textContent = titleMap[1];
}

function setSelectedVideoFile(file) {
  state.selectedVideoFile = file || null;
}

function setSelectedSubtitleFile(file) {
  state.selectedSubtitleFile = file || null;
}

function setSelectedBurnFile(file) {
  state.selectedBurnFile = file || null;
}

function resetResult() {
  state.latestResult = null;
  const empty = document.getElementById("resultEmpty");
  const card = document.getElementById("resultCard");
  const status = document.getElementById("statusText");
  if (empty) empty.style.display = "block";
  if (card) card.classList.remove("show");
  if (status) status.textContent = t("common.waitingUpload");
}

function resetSubtitleResult() {
  state.latestSubtitleResult = null;
  const empty = document.getElementById("subtitleResultEmpty");
  const card = document.getElementById("subtitleResultCard");
  const status = document.getElementById("subtitleStatusText");
  if (empty) empty.style.display = "block";
  if (card) card.classList.remove("show");
  if (status) status.textContent = t("common.waitingUpload");
  setSubtitleProgress(false, 0, "");
}

function resetBurnedVideoResult() {
  state.latestBurnedVideoResult = null;
  const empty = document.getElementById("burnResultEmpty");
  const card = document.getElementById("burnResultCard");
  const status = document.getElementById("burnStatusText");
  if (empty) empty.style.display = "block";
  if (card) card.classList.remove("show");
  if (status) status.textContent = t("common.waitingUpload");
  setBurnProgress(false, 0, "");
}

function renderResult(payload) {
  state.latestResult = payload;
  document.getElementById("resultEmpty").style.display = "none";
  document.getElementById("resultCard").classList.add("show");
  document.getElementById("statusText").textContent = t("tool.videoCompress.done");
  const title = payload.outcome === "smaller" ? t("tool.videoCompress.done") : payload.outcome === "larger" ? t("tool.videoCompress.doneLarger") : t("tool.videoCompress.doneSame");
  const subtitle = payload.outcome === "smaller"
    ? t("tool.videoCompress.result.subtitle.smaller", { file: payload.originalName, mode: payload.modeLabel })
    : payload.outcome === "larger"
      ? t("tool.videoCompress.result.subtitle.larger", { file: payload.originalName, mode: payload.modeLabel })
      : t("tool.videoCompress.result.subtitle.same", { file: payload.originalName, mode: payload.modeLabel });
  document.querySelector("#resultCard .result-banner strong").textContent = title;
  document.getElementById("resultSubtitle").textContent = subtitle;
  document.getElementById("originalSize").textContent = formatBytes(payload.originalSize);
  document.getElementById("compressedSize").textContent = formatBytes(payload.compressedSize);
  document.getElementById("savedBytes").textContent = formatBytes(payload.savedBytes);
  document.getElementById("reductionRatio").textContent = `${payload.reductionRatio}%`;
  document.getElementById("originalName").textContent = payload.originalName;
  document.getElementById("modeLabel").textContent = payload.modeLabel;
  document.getElementById("downloadPath").textContent = payload.downloadUrl;
}

function renderSubtitleResult(payload) {
  state.latestSubtitleResult = payload;
  document.getElementById("subtitleResultEmpty").style.display = "none";
  document.getElementById("subtitleResultCard").classList.add("show");
  document.getElementById("subtitleStatusText").textContent = t("tool.vttSubtitle.done");
  document.getElementById("subtitleFileName").textContent = payload.originalName;
  document.getElementById("subtitleLanguage").textContent = payload.language;
  document.getElementById("subtitleSegmentCount").textContent = String(payload.segmentCount);
  document.getElementById("subtitleDownloadPath").textContent = payload.downloadUrl;
}

function renderBurnedVideoResult(payload) {
  state.latestBurnedVideoResult = payload;
  document.getElementById("burnResultEmpty").style.display = "none";
  document.getElementById("burnResultCard").classList.add("show");
  document.getElementById("burnStatusText").textContent = t("tool.videoSubtitleBurn.done");
  document.getElementById("burnFileName").textContent = payload.originalName;
  document.getElementById("burnLanguage").textContent = payload.language;
  document.getElementById("burnSegmentCount").textContent = String(payload.segmentCount);
  document.getElementById("burnDownloadPath").textContent = payload.downloadUrl;
}

function setSubmitting(isSubmitting) {
  const submitButton = document.getElementById("submitButton");
  if (!submitButton) return;
  submitButton.disabled = isSubmitting;
  submitButton.textContent = isSubmitting ? t("tool.videoCompress.submitting") : t("tool.videoCompress.submit");
  document.getElementById("statusText").textContent = isSubmitting ? t("tool.videoCompress.status.running") : (state.latestResult ? t("tool.videoCompress.done") : t("common.waitingUpload"));
}

function setSubtitleSubmitting(isSubmitting) {
  const submitButton = document.getElementById("subtitleSubmitButton");
  if (!submitButton) return;
  submitButton.disabled = isSubmitting;
  submitButton.textContent = isSubmitting ? t("tool.vttSubtitle.submitting") : t("tool.vttSubtitle.submit");
  if (isSubmitting || !state.latestSubtitleResult) {
    document.getElementById("subtitleStatusText").textContent = isSubmitting ? t("tool.vttSubtitle.status.running") : t("common.waitingUpload");
  }
}

function setBurnSubmitting(isSubmitting) {
  const submitButton = document.getElementById("burnSubmitButton");
  if (!submitButton) return;
  submitButton.disabled = isSubmitting;
  submitButton.textContent = isSubmitting ? t("tool.videoSubtitleBurn.submitting") : t("tool.videoSubtitleBurn.submit");
  if (isSubmitting || !state.latestBurnedVideoResult) {
    document.getElementById("burnStatusText").textContent = isSubmitting ? t("tool.videoSubtitleBurn.status.running") : t("common.waitingUpload");
  }
}

function syncVideoFileState() {
  const input = document.getElementById("videoFile");
  const stateEl = document.getElementById("videoFileState");
  const submit = document.getElementById("submitButton");
  if (!input || !stateEl || !submit) return;
  const file = input.files?.[0] || state.selectedVideoFile;
  setSelectedVideoFile(file);
  if (file) {
    stateEl.textContent = t("tool.videoCompress.file.ready", { name: file.name });
    stateEl.classList.add("ready");
    submit.disabled = false;
  } else {
    stateEl.textContent = t("tool.videoCompress.file.empty");
    stateEl.classList.remove("ready");
    submit.disabled = false;
  }
}

function syncSubtitleFileState() {
  const input = document.getElementById("subtitleVideoFile");
  const stateEl = document.getElementById("subtitleVideoFileState");
  const submit = document.getElementById("subtitleSubmitButton");
  if (!input || !stateEl || !submit) return;
  const file = input.files?.[0] || state.selectedSubtitleFile;
  setSelectedSubtitleFile(file);
  if (file) {
    stateEl.textContent = t("tool.vttSubtitle.file.ready", { name: file.name });
    stateEl.classList.add("ready");
    submit.disabled = false;
  } else {
    stateEl.textContent = t("tool.vttSubtitle.file.empty");
    stateEl.classList.remove("ready");
    submit.disabled = false;
  }
}

function syncBurnFileState() {
  const input = document.getElementById("burnVideoFile");
  const stateEl = document.getElementById("burnVideoFileState");
  const submit = document.getElementById("burnSubmitButton");
  if (!input || !stateEl || !submit) return;
  const file = input.files?.[0] || state.selectedBurnFile;
  setSelectedBurnFile(file);
  if (file) {
    stateEl.textContent = t("tool.videoSubtitleBurn.file.ready", { name: file.name });
    stateEl.classList.add("ready");
    submit.disabled = false;
  } else {
    stateEl.textContent = t("tool.videoSubtitleBurn.file.empty");
    stateEl.classList.remove("ready");
    submit.disabled = false;
  }
}

function setSubtitleProgress(show, percent, text) {
  const shell = document.getElementById("subtitleProgressShell");
  const fill = document.getElementById("subtitleProgressFill");
  const label = document.getElementById("subtitleProgressText");
  if (!shell || !fill || !label) return;
  shell.classList.toggle("show", show);
  fill.style.width = `${Math.max(0, Math.min(percent, 100))}%`;
  label.textContent = text || "";
}

function startSubtitlePseudoProgress() {
  let percent = 8;
  setSubtitleProgress(true, percent, t("tool.vttSubtitle.progress.extract"));
  if (state.subtitleProgressTimer) clearInterval(state.subtitleProgressTimer);
  state.subtitleProgressTimer = setInterval(() => {
    percent = Math.min(percent + (percent < 60 ? 12 : percent < 85 ? 5 : 1), 92);
    setSubtitleProgress(true, percent, percent < 45 ? t("tool.vttSubtitle.progress.extractOnly") : percent < 80 ? t("tool.vttSubtitle.progress.transcribe") : t("tool.vttSubtitle.progress.render"));
  }, 900);
}

function finishSubtitlePseudoProgress(success) {
  if (state.subtitleProgressTimer) clearInterval(state.subtitleProgressTimer);
  state.subtitleProgressTimer = null;
  setSubtitleProgress(true, 100, success ? t("tool.vttSubtitle.progress.success") : t("tool.vttSubtitle.progress.fail"));
}

function setBurnProgress(show, percent, text) {
  const shell = document.getElementById("burnProgressShell");
  const fill = document.getElementById("burnProgressFill");
  const label = document.getElementById("burnProgressText");
  if (!shell || !fill || !label) return;
  shell.classList.toggle("show", show);
  fill.style.width = `${Math.max(0, Math.min(percent, 100))}%`;
  label.textContent = text || "";
}

function startBurnPseudoProgress() {
  let percent = 6;
  setBurnProgress(true, percent, t("tool.videoSubtitleBurn.progress.start"));
  if (state.burnProgressTimer) clearInterval(state.burnProgressTimer);
  state.burnProgressTimer = setInterval(() => {
    percent = Math.min(percent + (percent < 35 ? 10 : percent < 70 ? 7 : percent < 88 ? 3 : 1), 94);
    setBurnProgress(true, percent, percent < 35 ? t("tool.videoSubtitleBurn.progress.upload") : percent < 70 ? t("tool.videoSubtitleBurn.progress.subtitle") : percent < 88 ? t("tool.videoSubtitleBurn.progress.burn") : t("tool.videoSubtitleBurn.progress.finish"));
  }, 900);
}

function finishBurnPseudoProgress(success) {
  if (state.burnProgressTimer) clearInterval(state.burnProgressTimer);
  state.burnProgressTimer = null;
  setBurnProgress(true, 100, success ? t("tool.videoSubtitleBurn.progress.success") : t("tool.videoSubtitleBurn.progress.fail"));
}

async function handleToolSubmit(event) {
  event.preventDefault();
  const file = state.selectedVideoFile || document.getElementById("videoFile").files?.[0];
  if (!file) {
    showModal({ title: t("tool.videoCompress.modal.noFile.title"), message: t("tool.videoCompress.modal.noFile.message"), actions: [{ label: t("common.gotIt"), variant: "ghost" }] });
    return;
  }
  const formData = new FormData();
  formData.set("file", file);
  formData.set("mode", state.selectedVideoMode);
  setSubmitting(true);
  try {
    const payload = await submitVideoCompress(formData);
    renderResult(payload);
    const message = payload.outcome === "smaller"
      ? t("tool.videoCompress.toast.done.smaller")
      : payload.outcome === "larger"
        ? t("tool.videoCompress.toast.done.larger")
        : t("tool.videoCompress.toast.done.same");
    toast({ title: t("tool.videoCompress.toast.done.title"), message });
  } catch (error) {
    console.error(error);
    showModal({ title: t("tool.videoCompress.modal.fail.title"), message: toUserMessage(error, "videoCompress"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  } finally {
    await loadToolRuns();
    setSubmitting(false);
  }
}

async function handleSubtitleSubmit(event) {
  event.preventDefault();
  const file = state.selectedSubtitleFile || document.getElementById("subtitleVideoFile").files?.[0];
  if (!file) {
    showModal({ title: t("tool.vttSubtitle.modal.noFile.title"), message: t("tool.vttSubtitle.modal.noFile.message"), actions: [{ label: t("common.gotIt"), variant: "ghost" }] });
    return;
  }
  const formData = new FormData();
  formData.set("file", file);
  formData.set("language", state.selectedSubtitleLanguage);
  setSubtitleSubmitting(true);
  startSubtitlePseudoProgress();
  try {
    const payload = await submitVttSubtitle(formData);
    finishSubtitlePseudoProgress(true);
    renderSubtitleResult(payload);
    toast({ title: t("tool.vttSubtitle.toast.done.title"), message: t("tool.vttSubtitle.toast.done.message") });
  } catch (error) {
    console.error(error);
    finishSubtitlePseudoProgress(false);
    showModal({ title: t("tool.vttSubtitle.modal.fail.title"), message: toUserMessage(error, "vttSubtitle"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  } finally {
    await loadToolRuns();
    setSubtitleSubmitting(false);
  }
}

async function handleBurnSubmit(event) {
  event.preventDefault();
  const file = state.selectedBurnFile || document.getElementById("burnVideoFile").files?.[0];
  if (!file) {
    showModal({ title: t("tool.videoSubtitleBurn.modal.noFile.title"), message: t("tool.videoSubtitleBurn.modal.noFile.message"), actions: [{ label: t("common.gotIt"), variant: "ghost" }] });
    return;
  }
  const formData = new FormData();
  formData.set("file", file);
  formData.set("language", state.selectedBurnLanguage);
  setBurnSubmitting(true);
  startBurnPseudoProgress();
  try {
    const payload = await submitVideoSubtitleBurn(formData);
    finishBurnPseudoProgress(true);
    renderBurnedVideoResult(payload);
    toast({ title: t("tool.videoSubtitleBurn.toast.done.title"), message: t("tool.videoSubtitleBurn.toast.done.message") });
  } catch (error) {
    console.error(error);
    finishBurnPseudoProgress(false);
    showModal({ title: t("tool.videoSubtitleBurn.modal.fail.title"), message: toUserMessage(error, "videoSubtitleBurn"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  } finally {
    await loadToolRuns();
    setBurnSubmitting(false);
  }
}

async function handleDownload() {
  if (!state.latestResult) return;
  try {
    await downloadBlob(state.latestResult.downloadUrl, `compressed-${state.latestResult.originalName.replace(/\.[^.]+$/, "") || "video"}.mp4`);
  } catch {
    showModal({ title: t("tool.videoCompress.modal.downloadFail.title"), message: t("tool.videoCompress.modal.downloadFail.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

async function handleSubtitleDownload() {
  if (!state.latestSubtitleResult) return;
  try {
    await downloadBlob(state.latestSubtitleResult.downloadUrl, `${state.latestSubtitleResult.originalName.replace(/\.[^.]+$/, "") || "subtitle"}.vtt`);
  } catch {
    showModal({ title: t("tool.vttSubtitle.modal.downloadFail.title"), message: t("tool.vttSubtitle.modal.downloadFail.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

async function handleBurnDownload() {
  if (!state.latestBurnedVideoResult) return;
  try {
    await downloadBlob(state.latestBurnedVideoResult.downloadUrl, `burned-${state.latestBurnedVideoResult.originalName.replace(/\.[^.]+$/, "") || "video"}.mp4`);
  } catch {
    showModal({ title: t("tool.videoSubtitleBurn.modal.downloadFail.title"), message: t("tool.videoSubtitleBurn.modal.downloadFail.message"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

function toolLabel(toolType) {
  const tool = getTool(toolType);
  return tool ? tool.title : toolType;
}

async function downloadRunArtifact(downloadUrl) {
  try {
    await downloadBlob(downloadUrl, "hagsyn-tool-result");
  } catch (error) {
    showModal({ title: t("tool.videoCompress.modal.downloadFail.title"), message: toUserMessage(error, "downloadArtifact"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

function renderToolRunHistory() {
  const root = document.getElementById("toolRunHistory");
  if (!root) return;
  if (!state.toolRuns.length) {
    root.innerHTML = `<div class="empty">${t("tools.history.empty")}</div>`;
    return;
  }
  root.innerHTML = state.toolRuns.map((run) => `<div class="roadline"><div><strong>${esc(t("tools.history.item", { tool: toolLabel(run.toolType), status: run.status }))}</strong><div class="helper">${esc(run.inputFileName || t("tools.history.noFile"))} · ${formatDateTime(run.startedAt)} · ${run.durationMs ?? "-"} ms</div>${run.errorMessage ? `<div class="helper">${esc(toHistoryMessage(run.errorMessage, run.toolType))}</div>` : ""}</div>${run.downloadUrl ? `<button class="button ghost" type="button" onclick="downloadRunArtifact('${esc(run.downloadUrl)}')">${t("common.downloadResult")}</button>` : `<span class="status-badge wait">${t("tools.history.noDownload")}</span>`}</div>`).join("");
}

async function loadToolRuns() {
  try {
    state.toolRuns = await fetchToolRuns(8);
  } catch (error) {
    console.error(error);
    state.toolRuns = [];
  }
  renderToolRunHistory();
}

async function fetchCurrentUser() {
  const token = getAuthToken();
  if (!token) {
    state.authUser = null;
    state.authChecked = true;
    return null;
  }
  try {
    const user = await apiRequest("/api/auth/me");
    setAuthSession({ token, user });
    return user;
  } catch {
    clearAuthSession();
    return null;
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData.entries());
  try {
    const result = await authJson("/api/auth/login", payload);
    setAuthSession({ token: result.token, user: result.user });
    syncUserIdentity();
    toast({ title: t("auth.loginSuccess.title"), message: t("auth.loginSuccess.message") });
    await show("dashboard");
  } catch (error) {
    showModal({ title: t("auth.loginFail.title"), message: toUserMessage(error, "login"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData.entries());
  try {
    const result = await authJson("/api/auth/register", payload);
    setAuthSession({ token: result.token, user: result.user });
    syncUserIdentity();
    toast({ title: t("auth.registerSuccess.title"), message: t("auth.registerSuccess.message") });
    await show("dashboard");
  } catch (error) {
    showModal({ title: t("auth.registerFail.title"), message: toUserMessage(error, "register"), actions: [{ label: t("common.close"), variant: "ghost" }] });
  }
}

function bindAuthView() {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const goRegisterButton = document.getElementById("goRegisterButton");
  const goLoginButton = document.getElementById("goLoginButton");
  const passwordToggleButtons = document.querySelectorAll("[data-password-toggle]");
  if (loginForm) loginForm.addEventListener("submit", handleLoginSubmit);
  if (registerForm) registerForm.addEventListener("submit", handleRegisterSubmit);
  if (goRegisterButton) goRegisterButton.addEventListener("click", () => show("register"));
  if (goLoginButton) goLoginButton.addEventListener("click", () => show("login"));
  passwordToggleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.passwordToggle || "");
      if (!input) return;
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      button.classList.toggle("active", !showing);
      button.setAttribute("aria-label", showing ? t("auth.showPassword") : t("auth.hidePassword"));
      button.setAttribute("title", showing ? t("auth.showPassword") : t("auth.hidePassword"));
    });
  });
}

function bindVideoWorkspace() {
  const form = document.getElementById("uploadForm");
  const resetButton = document.getElementById("resetButton");
  const downloadButton = document.getElementById("downloadButton");
  const fileInput = document.getElementById("videoFile");
  const modeInputs = document.querySelectorAll('input[name="mode"]');
  if (form) form.addEventListener("submit", handleToolSubmit);
  modeInputs.forEach((input) => input.addEventListener("change", () => {
    state.selectedVideoMode = input.value;
  }));
  if (resetButton) resetButton.addEventListener("click", () => {
    form.reset();
    state.selectedVideoMode = "balanced";
    setSelectedVideoFile(null);
    resetResult();
    syncVideoFileState();
    toast({ title: t("tool.videoCompress.toast.reset.title"), message: t("tool.videoCompress.toast.reset.message") });
  });
  if (downloadButton) downloadButton.addEventListener("click", handleDownload);
  if (fileInput) fileInput.addEventListener("change", () => {
    setSelectedVideoFile(fileInput.files?.[0] || null);
    syncVideoFileState();
  });
  if (state.latestResult) renderResult(state.latestResult); else resetResult();
  syncVideoFileState();
}

function bindSubtitleWorkspace() {
  const form = document.getElementById("subtitleUploadForm");
  const resetButton = document.getElementById("subtitleResetButton");
  const downloadButton = document.getElementById("subtitleDownloadButton");
  const fileInput = document.getElementById("subtitleVideoFile");
  const languageInputs = document.querySelectorAll('#subtitleUploadForm input[name="language"]');
  if (form) form.addEventListener("submit", handleSubtitleSubmit);
  languageInputs.forEach((input) => input.addEventListener("change", () => {
    state.selectedSubtitleLanguage = input.value;
  }));
  if (resetButton) resetButton.addEventListener("click", () => {
    form.reset();
    state.selectedSubtitleLanguage = "auto";
    setSelectedSubtitleFile(null);
    resetSubtitleResult();
    syncSubtitleFileState();
    toast({ title: t("tool.vttSubtitle.toast.reset.title"), message: t("tool.vttSubtitle.toast.reset.message") });
  });
  if (downloadButton) downloadButton.addEventListener("click", handleSubtitleDownload);
  if (fileInput) fileInput.addEventListener("change", () => {
    setSelectedSubtitleFile(fileInput.files?.[0] || null);
    syncSubtitleFileState();
  });
  if (state.latestSubtitleResult) renderSubtitleResult(state.latestSubtitleResult); else resetSubtitleResult();
  syncSubtitleFileState();
}

function bindBurnWorkspace() {
  const form = document.getElementById("burnUploadForm");
  const resetButton = document.getElementById("burnResetButton");
  const downloadButton = document.getElementById("burnDownloadButton");
  const fileInput = document.getElementById("burnVideoFile");
  const languageInputs = document.querySelectorAll('#burnUploadForm input[name="language"]');
  if (form) form.addEventListener("submit", handleBurnSubmit);
  languageInputs.forEach((input) => input.addEventListener("change", () => {
    state.selectedBurnLanguage = input.value;
  }));
  if (resetButton) resetButton.addEventListener("click", () => {
    form.reset();
    state.selectedBurnLanguage = "auto";
    setSelectedBurnFile(null);
    resetBurnedVideoResult();
    syncBurnFileState();
    toast({ title: t("tool.videoSubtitleBurn.toast.reset.title"), message: t("tool.videoSubtitleBurn.toast.reset.message") });
  });
  if (downloadButton) downloadButton.addEventListener("click", handleBurnDownload);
  if (fileInput) fileInput.addEventListener("change", () => {
    setSelectedBurnFile(fileInput.files?.[0] || null);
    syncBurnFileState();
  });
  if (state.latestBurnedVideoResult) renderBurnedVideoResult(state.latestBurnedVideoResult); else resetBurnedVideoResult();
  syncBurnFileState();
}

const renderers = {
  login: async () => {
    document.getElementById("view").innerHTML = renderAuthView({ mode: "login" });
    bindAuthView();
  },
  register: async () => {
    document.getElementById("view").innerHTML = renderAuthView({ mode: "register" });
    bindAuthView();
  },
  dashboard: () => { document.getElementById("view").innerHTML = renderDashboardView(getTools().length); },
  nodes: () => { document.getElementById("view").innerHTML = renderNodesView(); },
  graph: () => { document.getElementById("view").innerHTML = renderGraphView(); },
  roadmaps: () => { document.getElementById("view").innerHTML = renderRoadmapsView(); },
  tools: async () => {
    const activeTool = getTool(state.toolRoute);
    const workspaceHeader = activeTool ? `<div class="section-title"><div><h2>${esc(t("tools.workspace.opened", { title: activeTool.title }))}</h2><span class="helper">${t("common.workspaceInTools")}</span></div><button class="button ghost" id="toolWorkspaceCloseButton" type="button" onclick="closeToolWorkspace()">${t("tools.workspace.close")}</button></div>` : "";
    const workspaceMarkup = !activeTool
      ? ""
      : activeTool.id === "video-compress"
        ? renderVideoWorkspace(activeTool, state.selectedVideoMode)
        : activeTool.id === "vtt-subtitle"
          ? renderSubtitleWorkspace(activeTool, state.selectedSubtitleLanguage)
          : renderBurnWorkspace(activeTool, state.selectedBurnLanguage);
    document.getElementById("view").innerHTML = renderToolsView({ tools: getTools(), activeTool, workspaceHeader, workspaceMarkup });
    if (activeTool?.id === "video-compress") bindVideoWorkspace();
    if (activeTool?.id === "vtt-subtitle") bindSubtitleWorkspace();
    if (activeTool?.id === "video-subtitle-burn") bindBurnWorkspace();
    await loadToolRuns();
  },
};

async function show(page, toolId = "") {
  closeMobileNav();
  state.current = pages.includes(page) || isAuthRoute(page) ? page : "dashboard";
  state.toolRoute = state.current === "tools" ? toolId : "";
  if (!state.authChecked) {
    await fetchCurrentUser();
  }
  if (!state.authUser && !isAuthRoute(state.current)) {
    state.current = "login";
    state.toolRoute = "";
  }
  if (state.authUser && isAuthRoute(state.current)) {
    state.current = "dashboard";
    state.toolRoute = "";
  }
  syncRoute(state.current, state.toolRoute);
  renderChrome();
  document.querySelectorAll(".nav button").forEach((button) => button.classList.toggle("active", button.dataset.page === state.current));
  setPageMeta();
  updateShellForRoute();
  await renderers[state.current]();
}

function closeToolWorkspace() {
  show("tools");
}

function openTool(toolId) {
  show("tools", toolId);
}

function showToolInfo(toolId) {
  const tool = getTool(toolId);
  if (!tool) return;
  showModal({
    title: tool.title,
    message: t("tools.info.message", { summary: tool.summary, modes: tool.modes.join(" / ") }),
    actions: [
      { label: t("common.close"), variant: "ghost" },
      { label: t("common.enterTool"), handler: () => openTool(toolId) },
    ],
  });
}

Object.assign(window, {
  API,
  applyTheme,
  closeModal,
  closeStoragePolicyPanel,
  closeToolWorkspace,
  downloadRunArtifact,
  handleLogout,
  isAdminUser,
  loadStoragePolicySettings,
  openStoragePolicyPanel,
  openTool,
  runManualStorageCleanup,
  runModalAction,
  saveStoragePolicySettings,
  setAppLocale,
  showAccountInfo,
  showSettingsInfo,
  showToolInfo,
});

window.addEventListener("hashchange", () => {
  const route = parseRoute();
  show(route.page, route.toolId);
});
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.modalState) closeModal();
  if (event.key === "Escape" && state.userMenuOpen) setUserMenu(false);
  if (event.key === "Escape" && state.storagePolicyPanelOpen) closeStoragePolicyPanel();
  if (event.key === "Escape" && state.mobileNavOpen) closeMobileNav();
});
window.addEventListener("resize", () => {
  if (window.innerWidth > 760) closeMobileNav();
});

document.getElementById("userMenuButton").addEventListener("click", toggleUserMenu);
document.getElementById("mobileNavToggle").addEventListener("click", toggleMobileNav);
document.getElementById("mobileNavClose").addEventListener("click", closeMobileNav);
document.getElementById("mobileNavScrim").addEventListener("click", closeMobileNav);
document.getElementById("adminSettingsEntry").addEventListener("click", openStoragePolicyPanel);
document.getElementById("closeStoragePolicyPanel").addEventListener("click", closeStoragePolicyPanel);
document.getElementById("settingsPanelScrim").addEventListener("click", closeStoragePolicyPanel);
document.getElementById("storagePolicyForm").addEventListener("submit", saveStoragePolicySettings);
document.getElementById("manualCleanupButton").addEventListener("click", runManualStorageCleanup);
document.getElementById("reloadStoragePolicyButton").addEventListener("click", loadStoragePolicySettings);
document.addEventListener("click", (event) => {
  const button = document.getElementById("userMenuButton");
  const menu = document.getElementById("userMenu");
  if (!state.userMenuOpen || !button || !menu) return;
  if (button.contains(event.target) || menu.contains(event.target)) return;
  setUserMenu(false);
});

renderChrome();
applyTheme(state.activeTheme);
show(state.current, state.toolRoute);
