import { t } from "../i18n/index.js";

const TECHNICAL_MESSAGE_PATTERNS = [
  /traceback/i,
  /exception/i,
  /stack/i,
  /ffmpeg/i,
  /ffprobe/i,
  /connecterror/i,
  /runtimeerror/i,
  /sqlalchemy/i,
  /non-zero exit status/i,
  /subtitle burn failed/i,
  /video compression failed/i,
];

function normalizeMessage(value) {
  if (typeof value !== "string") return "";
  return value.trim().replace(/^"+|"+$/g, "");
}

function looksTechnical(message) {
  return TECHNICAL_MESSAGE_PATTERNS.some((pattern) => pattern.test(message));
}

function toolContextFromType(toolType) {
  if (toolType === "video-compress") return "videoCompress";
  if (toolType === "vtt-subtitle") return "vttSubtitle";
  if (toolType === "video-subtitle-burn") return "videoSubtitleBurn";
  return "default";
}

function fallbackKeyForContext(context) {
  if (context === "login") return "auth.loginFail.message";
  if (context === "register") return "auth.registerFail.message";
  if (context === "videoCompress") return "tool.videoCompress.modal.fail.message";
  if (context === "vttSubtitle") return "tool.vttSubtitle.modal.fail.message";
  if (context === "videoSubtitleBurn") return "tool.videoSubtitleBurn.modal.fail.message";
  if (context === "downloadArtifact") return "common.error.artifactMissing";
  return "common.error.generic";
}

function resolveKnownKey(message, status, context) {
  const normalized = normalizeMessage(message);
  if (!normalized) return status === 0 ? "common.error.network" : null;
  if (/invalid username or password/i.test(normalized)) return "auth.loginFail.invalid";
  if (/username already exists/i.test(normalized)) return "auth.registerFail.usernameTaken";
  if (/phone already exists/i.test(normalized)) return "auth.registerFail.phoneTaken";
  if (/unsupported video format/i.test(normalized)) {
    if (context === "videoCompress") return "tool.videoCompress.error.unsupportedFormat";
    if (context === "vttSubtitle") return "tool.vttSubtitle.error.unsupportedFormat";
    if (context === "videoSubtitleBurn") return "tool.videoSubtitleBurn.error.unsupportedFormat";
    return "common.error.unsupportedVideoFormat";
  }
  if (/speech recognition dependency is unavailable/i.test(normalized) || /TRANSCRIBER_NOT_AVAILABLE/i.test(normalized)) {
    if (context === "videoSubtitleBurn") return "tool.videoSubtitleBurn.error.serviceUnavailable";
    return "tool.vttSubtitle.error.serviceUnavailable";
  }
  if (/WHISPER_MODEL_NOT_READY/i.test(normalized) || /模型.*未准备好/i.test(normalized)) {
    if (context === "videoSubtitleBurn") return "tool.videoSubtitleBurn.error.modelNotReady";
    return "tool.vttSubtitle.error.modelNotReady";
  }
  if (/compressed file not found/i.test(normalized)) return "tool.videoCompress.modal.downloadFail.message";
  if (/subtitle file not found/i.test(normalized)) return "tool.vttSubtitle.modal.downloadFail.message";
  if (/burned video file not found/i.test(normalized)) return "tool.videoSubtitleBurn.modal.downloadFail.message";
  if (/invalid or missing token/i.test(normalized)) return "common.error.unauthorized";
  if (/admin access required/i.test(normalized)) return "common.error.forbidden";
  if (status === 401) return context === "login" ? "auth.loginFail.invalid" : "common.error.unauthorized";
  if (status === 403) return "common.error.forbidden";
  if (status === 404) return "common.error.artifactMissing";
  if (status === 409 && context === "register") return "auth.registerFail.message";
  if (status >= 500) return fallbackKeyForContext(context);
  return null;
}

export function toUserMessage(error, context = "default") {
  const status = Number(error?.status || 0);
  const detail = normalizeMessage(error?.detail || error?.message || "");
  const knownKey = resolveKnownKey(detail, status, context);
  if (knownKey) return t(knownKey);
  if (status === 0) return t("common.error.network");
  if (detail && !looksTechnical(detail) && detail.length <= 120) return detail;
  return t(fallbackKeyForContext(context));
}

export function toHistoryMessage(message, toolType) {
  const normalized = normalizeMessage(message);
  if (!normalized) return "";
  if (!looksTechnical(normalized)) {
    const key = resolveKnownKey(normalized, 0, toolContextFromType(toolType));
    return key ? t(key) : normalized;
  }
  return t(fallbackKeyForContext(toolContextFromType(toolType)));
}
