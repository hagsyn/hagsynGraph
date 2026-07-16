import assert from "node:assert/strict";

const fakeStorage = new Map();
const localStorage = {
  getItem(key) {
    return fakeStorage.has(key) ? fakeStorage.get(key) : null;
  },
  setItem(key, value) {
    fakeStorage.set(key, String(value));
  },
  removeItem(key) {
    fakeStorage.delete(key);
  },
};

globalThis.localStorage = localStorage;
globalThis.document = {
  documentElement: {
    lang: "zh-CN",
    setAttribute(name, value) {
      this[name] = value;
    },
  },
};
globalThis.window = globalThis;
Object.defineProperty(globalThis, "navigator", {
  configurable: true,
  value: { language: "zh-CN" },
});

const { DEFAULT_LOCALE, resolveInitialLocale, getLocale, setLocale, t } = await import("../assets/js/i18n/index.js");

function resetEnv(language = "zh-CN") {
  fakeStorage.clear();
  globalThis.navigator.language = language;
  globalThis.document.documentElement.lang = DEFAULT_LOCALE;
}

try {
  resetEnv("zh-TW");
  assert.equal(resolveInitialLocale(), "zh-CN", "zh locales should resolve to zh-CN");

  resetEnv("en-US");
  assert.equal(resolveInitialLocale(), "en", "non-zh locales should resolve to en");

  resetEnv("en-US");
  localStorage.setItem("hagsyn_locale", "zh-CN");
  assert.equal(resolveInitialLocale(), "zh-CN", "stored locale should take precedence");

  resetEnv("en-US");
  localStorage.setItem("hagsyn_locale", "invalid");
  assert.equal(resolveInitialLocale(), "en", "invalid stored locale should fall back to browser locale");

  resetEnv("zh-CN");
  setLocale("en");
  assert.equal(getLocale(), "en", "setLocale should update current locale");
  assert.equal(localStorage.getItem("hagsyn_locale"), "en", "setLocale should persist locale");
  assert.equal(globalThis.document.documentElement.lang, "en", "setLocale should sync document lang");

  resetEnv("en-US");
  setLocale("zh-CN");
  assert.equal(t("nav.dashboard"), "Dashboard", "known keys should resolve using current locale");
  assert.equal(t("common.close"), "关闭", "zh-CN copy should be available");
  assert.equal(t("tool.videoCompress.toast.done.title"), "压缩已完成", "zh locale should resolve toast copy");
  assert.equal(
    t("tools.history.item", { tool: "Video Compress", status: "success" }),
    "Video Compress · success",
    "template placeholders should interpolate",
  );
  assert.equal(t("missing.key"), "missing.key", "missing keys should fall back to the key");

  console.log("i18n test passed");
} catch (error) {
  console.error(`i18n test failed: ${error.message}`);
  process.exit(1);
}
