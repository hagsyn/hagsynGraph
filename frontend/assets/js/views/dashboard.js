import { t } from "../i18n/index.js";

export function renderDashboardView(toolCount) {
  return `
    <div class="grid stats">
      ${[
        [t("dashboard.stats.modules"), 5],
        [t("dashboard.stats.tools"), toolCount],
        [t("dashboard.stats.subtitleTools"), 2],
        [t("dashboard.stats.knowledge"), 0],
      ].map(([label, value]) => `<div class="card stat"><div class="num">${value}</div><div class="label">${label}</div></div>`).join("")}
    </div>
    <div class="dashboard-grid">
      <div class="stack">
        <div class="card">
          <div class="section-title"><h2>${t("dashboard.overview.title")}</h2><span class="status-badge live">MVP</span></div>
          <div class="helper">${t("dashboard.overview.helper")}</div>
          <div class="section-title"><h2>${t("dashboard.capabilities.title")}</h2><span class="helper">${t("dashboard.capabilities.tag")}</span></div>
          <div class="roadline"><div><strong>${t("tool.videoCompress.title")} ${t("common.workspaceInTools")}</strong><div class="helper">${t("tool.videoCompress.summary")}</div></div><span class="status-badge live">${t("common.status.available")}</span></div>
          <div class="roadline"><div><strong>${t("tool.vttSubtitle.title")} ${t("common.workspaceInTools")}</strong><div class="helper">${t("tool.vttSubtitle.summary")}</div></div><span class="status-badge live">${t("common.status.available")}</span></div>
          <div class="roadline"><div><strong>${t("tool.videoSubtitleBurn.title")} ${t("common.workspaceInTools")}</strong><div class="helper">${t("tool.videoSubtitleBurn.summary")}</div></div><span class="status-badge live">${t("common.status.available")}</span></div>
          <div class="roadline"><div><strong>${t("dashboard.capabilities.knowledgeTitle")}</strong><div class="helper">${t("dashboard.capabilities.knowledgeSummary")}</div></div><span class="status-badge wait">${t("common.status.wait")}</span></div>
        </div>
        <div class="card">
          <div class="section-title"><h2>${t("dashboard.backlog.title")}</h2><span class="helper">${t("common.backlog")}</span></div>
          <div class="todo-list">
            <div class="todo-item"><strong>${t("dashboard.backlog.contentTitle")}</strong><span>${t("dashboard.backlog.contentSummary")}</span></div>
            <div class="todo-item"><strong>${t("dashboard.backlog.fileTitle")}</strong><span>${t("dashboard.backlog.fileSummary")}</span></div>
            <div class="todo-item"><strong>${t("dashboard.backlog.knowledgeTitle")}</strong><span>${t("dashboard.backlog.knowledgeSummary")}</span></div>
          </div>
        </div>
      </div>
      <div class="stack">
        <div class="card">
          <div class="section-title"><h2>${t("dashboard.moduleStatus.title")}</h2><span class="helper">Status</span></div>
          <div class="roadline"><div><strong>Dashboard</strong><div class="helper">${t("dashboard.moduleStatus.dashboardSummary")}</div></div><span class="status-badge live">${t("common.status.live")}</span></div>
          <div class="roadline"><div><strong>Tools</strong><div class="helper">${t("dashboard.moduleStatus.toolsSummary")}</div></div><span class="status-badge live">${t("common.status.live")}</span></div>
          <div class="roadline"><div><strong>Nodes / Graph / Roadmaps</strong><div class="helper">${t("dashboard.moduleStatus.knowledgeSummary")}</div></div><span class="status-badge plan">${t("common.status.plan")}</span></div>
        </div>
        <div class="card">
          <div class="section-title"><h2>${t("dashboard.next.title")}</h2><span class="helper">${t("common.action")}</span></div>
          <div class="signal-list">
            <div class="signal-item"><strong>${t("tool.vttSubtitle.title")}</strong><span>${t("dashboard.next.subtitle1")}</span></div>
            <div class="signal-item"><strong>${t("nav.nodes")}</strong><span>${t("dashboard.next.subtitle2")}</span></div>
            <div class="signal-item"><strong>${t("nav.roadmaps")}</strong><span>${t("dashboard.next.subtitle3")}</span></div>
          </div>
        </div>
      </div>
    </div>`;
}
