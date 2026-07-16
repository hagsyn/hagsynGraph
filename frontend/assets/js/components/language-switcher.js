export function renderLanguageSwitcherMarkup(locales, activeLocale, getLabel) {
  return locales
    .map(
      (locale) =>
        `<button type="button" class="theme-option ${locale === activeLocale ? "active" : ""}" onclick="setAppLocale('${locale}')" aria-pressed="${locale === activeLocale}">${getLabel(locale)}</button>`,
    )
    .join("");
}
