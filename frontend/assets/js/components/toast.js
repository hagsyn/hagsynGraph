import { esc } from "../utils/format.js";

export function renderToastMarkup({ title, message, type }, id) {
  return `<div class="toast ${type}" id="${id}"><strong>${esc(title)}</strong><div class="helper">${esc(message)}</div></div>`;
}
