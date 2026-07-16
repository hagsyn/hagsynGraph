import { esc, formatDateTime } from "../utils/format.js";
import { t } from "../i18n/index.js";

export function renderCleanupActivityMarkup(entries) {
  if (!entries.length) {
    return {
      html: `<div class="empty">${esc(t("settings.activity.empty"))}</div>`,
      lastRun: t("common.status.notRunYet"),
    };
  }
  return {
    html: entries.map((entry) => `<div class="activity-item"><strong>${esc(entry.title)}</strong><span>${esc(entry.message)}</span></div>`).join(""),
    lastRun: formatDateTime(entries[0].timestamp),
  };
}
