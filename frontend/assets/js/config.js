const isLocalDevHost = ["127.0.0.1", "localhost"].includes(window.location.hostname);
const defaultApiOrigin = isLocalDevHost || window.location.protocol === "file:"
  ? "http://127.0.0.1:8000"
  : window.location.origin;
const storedApiOrigin = localStorage.getItem("hagsyn_api");
const shouldIgnoreStoredLocalOrigin = isLocalDevHost && storedApiOrigin && storedApiOrigin !== "http://127.0.0.1:8000";

if (shouldIgnoreStoredLocalOrigin) {
  localStorage.removeItem("hagsyn_api");
}

export const API = shouldIgnoreStoredLocalOrigin ? defaultApiOrigin : (storedApiOrigin || defaultApiOrigin);
export const pages = ["dashboard", "tools", "nodes", "graph", "roadmaps"];
export const themes = {
  midnight: { labelKey: "theme.midnight", swatch: "linear-gradient(135deg,#6d7cff,#9b6bff)" },
  graphite: { labelKey: "theme.graphite", swatch: "linear-gradient(135deg,#7c8cff,#4fd1c5)" },
  pearl: { labelKey: "theme.pearl", swatch: "linear-gradient(135deg,#4f46e5,#0f766e)" },
};
export const tools = [
  {
    id: "video-compress",
    titleKey: "tool.videoCompress.title",
    statusKey: "common.status.available",
    summaryKey: "tool.videoCompress.summary",
    tags: ["mp4", "mov", "m4v", "ffmpeg"],
    detailKey: "tool.videoCompress.detail",
    modeKeys: [
      "tool.videoCompress.mode.balanced.label",
      "tool.videoCompress.mode.smaller.label",
      "tool.videoCompress.mode.quality.label",
    ],
  },
  {
    id: "vtt-subtitle",
    titleKey: "tool.vttSubtitle.title",
    statusKey: "common.status.available",
    summaryKey: "tool.vttSubtitle.summary",
    tags: ["vtt", "subtitle", "speech-to-text"],
    detailKey: "tool.vttSubtitle.detail",
    modeKeys: [
      "tool.vttSubtitle.language.auto.label",
      "tool.vttSubtitle.language.zh.label",
      "tool.vttSubtitle.language.en.label",
    ],
  },
  {
    id: "video-subtitle-burn",
    titleKey: "tool.videoSubtitleBurn.title",
    statusKey: "common.status.available",
    summaryKey: "tool.videoSubtitleBurn.summary",
    tags: ["subtitle-burn", "video", "ffmpeg"],
    detailKey: "tool.videoSubtitleBurn.detail",
    modeKeys: [
      "tool.videoSubtitleBurn.language.auto.label",
      "tool.videoSubtitleBurn.language.zh.label",
      "tool.videoSubtitleBurn.language.en.label",
    ],
  },
];
