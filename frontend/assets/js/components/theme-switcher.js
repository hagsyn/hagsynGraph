import { t } from "../i18n/index.js";

export function renderThemeSwitcherMarkup(themes, activeTheme) {
  return Object.entries(themes)
    .map(
      ([key, theme]) =>
        `<button type="button" class="theme-option ${key === activeTheme ? "active" : ""}" onclick="applyTheme('${key}')" aria-pressed="${key === activeTheme}"><span class="theme-swatch" style="background:${theme.swatch}"></span>${t(theme.labelKey)}</button>`,
    )
    .join("");
}
