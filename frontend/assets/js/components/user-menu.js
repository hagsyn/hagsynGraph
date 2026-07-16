import { t } from "../i18n/index.js";

export function applyUserIdentity({ username, role, isAdmin }) {
  const roleText = role === "admin" ? t("userMenu.role.admin") : t("userMenu.role.user");
  const initials = username.slice(0, 2).toUpperCase();
  document.getElementById("userAvatar").textContent = initials || "HA";
  document.getElementById("userName").textContent = username;
  document.getElementById("userRole").textContent = roleText;
  document.getElementById("userMenuName").textContent = username;
  document.getElementById("userMenuDesc").textContent = role === "admin"
    ? t("userMenu.desc.admin")
    : t("userMenu.desc.user");
  const adminEntry = document.getElementById("adminSettingsEntry");
  if (adminEntry) adminEntry.style.display = isAdmin ? "inline-flex" : "none";
}
