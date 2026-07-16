import { messages } from "./messages.js";

export const SUPPORTED_LOCALES = ["zh-CN", "en"];
export const DEFAULT_LOCALE = "zh-CN";
export const LOCALE_STORAGE_KEY = "hagsyn_locale";

let currentLocale = DEFAULT_LOCALE;

function isSupportedLocale(locale) {
  return SUPPORTED_LOCALES.includes(locale);
}

function browserLocaleToSupported(locale) {
  if (!locale) return "en";
  return locale.toLowerCase().startsWith("zh") ? "zh-CN" : "en";
}

function getBrowserLocale() {
  return browserLocaleToSupported(typeof navigator !== "undefined" ? navigator.language : "");
}

export function resolveInitialLocale() {
  const storedLocale = typeof localStorage !== "undefined" ? localStorage.getItem(LOCALE_STORAGE_KEY) : null;
  if (isSupportedLocale(storedLocale)) return storedLocale;
  if (storedLocale && typeof localStorage !== "undefined") {
    localStorage.removeItem(LOCALE_STORAGE_KEY);
  }
  return getBrowserLocale();
}

function syncDocumentLang(locale) {
  if (typeof document !== "undefined" && document.documentElement) {
    document.documentElement.setAttribute("lang", locale);
  }
}

export function getLocale() {
  return currentLocale;
}

export function setLocale(locale) {
  const nextLocale = isSupportedLocale(locale) ? locale : resolveInitialLocale();
  currentLocale = nextLocale;
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(LOCALE_STORAGE_KEY, currentLocale);
  }
  syncDocumentLang(currentLocale);
  return currentLocale;
}

export function t(key, params = {}) {
  const localeMessages = messages[currentLocale] || messages[DEFAULT_LOCALE] || {};
  const fallbackMessages = messages[DEFAULT_LOCALE] || {};
  const template = localeMessages[key] ?? fallbackMessages[key] ?? key;
  return String(template).replace(/\{(\w+)\}/g, (_, name) => (params[name] ?? `{${name}}`));
}

currentLocale = resolveInitialLocale();
syncDocumentLang(currentLocale);
