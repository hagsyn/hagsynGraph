import { t } from "../i18n/index.js";

export function renderAuthView({ mode }) {
  const isRegister = mode === "register";
  const passwordField = ({ id, name, autocomplete, labelKey }) => `
    <div class="settings-row auth-row">
      <label for="${id}">${t(labelKey)}</label>
      <div class="password-field">
        <input id="${id}" name="${name}" type="password" autocomplete="${autocomplete}" required />
        <button
          class="password-toggle"
          type="button"
          data-password-toggle="${id}"
          aria-label="${t("auth.showPassword")}"
          title="${t("auth.showPassword")}"
        >
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M2.25 12S5.25 6.75 12 6.75 21.75 12 21.75 12 18.75 17.25 12 17.25 2.25 12 2.25 12Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.6"/>
          </svg>
        </button>
      </div>
    </div>
  `;
  return `
    <section class="auth-shell">
      <div class="auth-hero">
        <div class="auth-hero-inner">
          <section class="auth-intro">
            <div class="auth-brand-mark">${t(isRegister ? "auth.register.brand" : "auth.login.brand")}</div>
            <h1>${t(isRegister ? "auth.register.heroTitle" : "auth.login.heroTitle")}</h1>
            <p>${t(isRegister ? "auth.register.heroText" : "auth.login.heroText")}</p>
            <div class="auth-signal-list">
              <div class="auth-signal">${t(isRegister ? "auth.register.signal.1" : "auth.login.signal.1")}</div>
              <div class="auth-signal">${t(isRegister ? "auth.register.signal.2" : "auth.login.signal.2")}</div>
              <div class="auth-signal">${t(isRegister ? "auth.register.signal.3" : "auth.login.signal.3")}</div>
            </div>
          </section>

          <section class="card auth-card auth-card-panel">
            <div class="auth-card-header auth-card-panel-header">
              <div>
                <div class="auth-eyebrow">${t(isRegister ? "auth.register.eyebrow" : "auth.login.eyebrow")}</div>
                <h2>${t(isRegister ? "auth.register.cardTitle" : "auth.login.cardTitle")}</h2>
              </div>
              <span class="helper auth-status">${t(isRegister ? "auth.register.cardStatus" : "auth.login.cardStatus")}</span>
            </div>

            <form class="form auth-form auth-panel-form" id="${isRegister ? "registerForm" : "loginForm"}">
              ${isRegister ? `
                <div class="settings-row auth-row">
                  <label for="registerUsername">${t("auth.username")}</label>
                  <input id="registerUsername" name="username" type="text" autocomplete="username" required />
                </div>
                <div class="settings-row auth-row">
                  <label for="registerPhone">${t("auth.phone")}</label>
                  <input id="registerPhone" name="phone" type="tel" autocomplete="tel" required />
                </div>
                ${passwordField({ id: "registerPassword", name: "password", autocomplete: "new-password", labelKey: "auth.password" })}
                ${passwordField({ id: "registerConfirmPassword", name: "confirmPassword", autocomplete: "new-password", labelKey: "auth.confirmPassword" })}
              ` : `
                <div class="settings-row auth-row">
                  <label for="loginAccount">${t("auth.account")}</label>
                  <input id="loginAccount" name="account" type="text" autocomplete="username" required />
                </div>
                ${passwordField({ id: "loginPassword", name: "password", autocomplete: "current-password", labelKey: "auth.password" })}
              `}
              <div class="helper auth-helper">${t(isRegister ? "auth.register.helper" : "auth.login.helper")}</div>
              <div class="form-actions auth-actions">
                <button class="button auth-primary" id="${isRegister ? "registerSubmitButton" : "loginSubmitButton"}" type="submit">${t(isRegister ? "auth.register.submit" : "auth.login.submit")}</button>
                <button class="button ghost auth-secondary" id="${isRegister ? "goLoginButton" : "goRegisterButton"}" type="button">${t(isRegister ? "auth.goLogin" : "auth.goRegister")}</button>
              </div>
            </form>
          </section>
        </div>
      </div>
    </section>
  `;
}
