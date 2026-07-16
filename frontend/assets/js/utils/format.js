export function esc(value) {
  return String(value ?? "").replace(/[&<>"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char]));
}

export function formatBytes(bytes) {
  if (!Number.isFinite(bytes)) return "-";
  const units = ["B", "KB", "MB", "GB"];
  let value = Math.abs(bytes);
  let index = 0;
  while (value >= 1024 && index < units.length - 1) {
    value /= 1024;
    index += 1;
  }
  const prefix = bytes < 0 ? "-" : "";
  return `${prefix}${value.toFixed(value >= 100 || index === 0 ? 0 : 1)} ${units[index]}`;
}

export function formatDateTime(value) {
  if (!value) return "尚未执行";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "尚未执行";
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
}
