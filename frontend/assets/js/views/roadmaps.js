import { t } from "../i18n/index.js";

export function renderRoadmapsView() {
  return `
    <div class="knowledge-shell">
      <div class="card">
        <div class="section-title"><h2>${t("roadmaps.title")}</h2><span class="status-badge plan">${t("common.status.plan")}</span></div>
        <div class="helper">${t("roadmaps.helper")}</div>
      </div>
      <div class="knowledge-grid">
        <div class="stack">
          <div class="card"><div class="section-title"><h2>${t("roadmaps.types.title")}</h2></div><div class="mini-list"><div class="mini-item"><strong>${t("roadmaps.types.product")}</strong><span>${t("roadmaps.types.productSummary")}</span></div><div class="mini-item"><strong>${t("roadmaps.types.tools")}</strong><span>${t("roadmaps.types.toolsSummary")}</span></div><div class="mini-item"><strong>${t("roadmaps.types.knowledge")}</strong><span>${t("roadmaps.types.knowledgeSummary")}</span></div></div></div>
          <div class="card"><div class="section-title"><h2>${t("roadmaps.conditions.title")}</h2></div><div class="empty">${t("roadmaps.conditions.empty")}</div></div>
        </div>
        <div class="stack">
          <div class="card"><div class="section-title"><h2>${t("roadmaps.preview.title")}</h2></div><div class="preview-box"><strong>${t("roadmaps.preview.emptyTitle")}</strong><div class="helper" style="margin-top:6px">${t("roadmaps.preview.emptyHelper")}</div></div></div>
          <div class="card"><div class="section-title"><h2>${t("roadmaps.status.title")}</h2></div><div class="helper">${t("roadmaps.status.helper")}</div></div>
        </div>
      </div>
    </div>`;
}
