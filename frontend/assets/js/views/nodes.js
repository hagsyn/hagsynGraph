import { t } from "../i18n/index.js";

export function renderNodesView() {
  return `
    <div class="knowledge-shell">
      <div class="card">
        <div class="section-title"><h2>${t("nodes.title")}</h2><span class="status-badge wait">${t("common.status.wait")}</span></div>
        <div class="helper">${t("nodes.helper")}</div>
        <div class="toolbar" style="margin-top:16px">
          <input placeholder="${t("nodes.search.placeholder")}" />
          <select><option>${t("nodes.filter.type.all")}</option><option>${t("nodes.filter.type.tool")}</option><option>${t("nodes.filter.type.scene")}</option><option>${t("nodes.filter.type.experience")}</option><option>${t("nodes.filter.type.issue")}</option><option>${t("nodes.filter.type.template")}</option><option>${t("nodes.filter.type.resource")}</option></select>
          <select><option>${t("nodes.filter.status.all")}</option><option>${t("nodes.filter.status.pending")}</option><option>${t("nodes.filter.status.organized")}</option><option>${t("nodes.filter.status.reused")}</option></select>
          <button class="button ghost" type="button">${t("nodes.create")}</button>
        </div>
      </div>
      <div class="knowledge-grid">
        <div class="card">
          <div class="section-title"><h2>${t("nodes.list.title")}</h2><span class="helper">${t("nodes.list.count")}</span></div>
          <div class="list-shell">
            <div class="list-row header"><span>${t("nodes.list.name")}</span><span>${t("nodes.list.type")}</span><span>${t("nodes.list.source")}</span><span>${t("nodes.list.updatedAt")}</span><span>${t("nodes.list.status")}</span></div>
            <div class="empty">${t("nodes.empty")}</div>
          </div>
        </div>
        <div class="preview-panel">
          <div class="card">
            <div class="section-title"><h2>${t("nodes.preview.title")}</h2></div>
            <div class="preview-box"><strong>${t("nodes.preview.emptyTitle")}</strong><div class="helper" style="margin-top:6px">${t("nodes.preview.emptyHelper")}</div></div>
          </div>
          <div class="card">
            <div class="section-title"><h2>${t("nodes.sources.title")}</h2></div>
            <div class="mini-list">
              <div class="mini-item"><strong>${t("nodes.sources.tool")}</strong><span>${t("nodes.sources.toolSummary")}</span></div>
              <div class="mini-item"><strong>${t("nodes.sources.scene")}</strong><span>${t("nodes.sources.sceneSummary")}</span></div>
              <div class="mini-item"><strong>${t("nodes.sources.resource")}</strong><span>${t("nodes.sources.resourceSummary")}</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
}
