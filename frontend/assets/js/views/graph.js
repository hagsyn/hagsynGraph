import { t } from "../i18n/index.js";

export function renderGraphView() {
  return `
    <div class="knowledge-shell">
      <div class="card">
        <div class="section-title"><h2>${t("graph.title")}</h2><span class="status-badge wait">${t("common.status.wait")}</span></div>
        <div class="helper">${t("graph.helper")}</div>
      </div>
      <div class="knowledge-grid">
        <div class="stack">
          <div class="card"><div class="section-title"><h2>${t("graph.view.title")}</h2><span class="helper">${t("graph.view.count")}</span></div><div class="empty">${t("graph.view.empty")}</div></div>
          <div class="card"><div class="section-title"><h2>${t("graph.semantics.title")}</h2></div><div class="mini-list"><div class="mini-item"><strong>${t("graph.semantics.apply")}</strong><span>${t("graph.semantics.applySummary")}</span></div><div class="mini-item"><strong>${t("graph.semantics.dependency")}</strong><span>${t("graph.semantics.dependencySummary")}</span></div><div class="mini-item"><strong>${t("graph.semantics.compose")}</strong><span>${t("graph.semantics.composeSummary")}</span></div><div class="mini-item"><strong>${t("graph.semantics.io")}</strong><span>${t("graph.semantics.ioSummary")}</span></div></div></div>
        </div>
        <div class="stack">
          <div class="card"><div class="section-title"><h2>${t("graph.sources.title")}</h2></div><div class="mini-list"><div class="mini-item"><strong>${t("graph.sources.tools")}</strong><span>${t("graph.sources.toolsSummary")}</span></div><div class="mini-item"><strong>${t("graph.sources.nodes")}</strong><span>${t("graph.sources.nodesSummary")}</span></div><div class="mini-item"><strong>${t("graph.sources.scenes")}</strong><span>${t("graph.sources.scenesSummary")}</span></div></div></div>
          <div class="card"><div class="section-title"><h2>${t("graph.status.title")}</h2></div><div class="helper">${t("graph.status.helper")}</div></div>
        </div>
      </div>
    </div>`;
}
