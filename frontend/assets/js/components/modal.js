import { esc } from "../utils/format.js";
import { t } from "../i18n/index.js";

export function renderModalMarkup(modalState) {
  return `<div class="modal-scrim" onclick="closeModal()"></div><section class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle"><div class="modal-header"><div><h2 class="modal-title" id="modalTitle">${esc(modalState.title)}</h2><div class="modal-body">${esc(modalState.message)}</div></div><button type="button" class="icon-button" aria-label="${esc(t("common.close"))}" onclick="closeModal()">✕</button></div><div class="modal-footer">${modalState.actions.map((action,index)=>`<button type="button" class="button ${action.variant||"ghost"}" onclick="runModalAction(${index})">${esc(action.label)}</button>`).join("")}</div></section>`;
}
