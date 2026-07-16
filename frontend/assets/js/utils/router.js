export function parseRoute() {
  const value = (location.hash || "#dashboard").replace(/^#/, "");
  const [page = "dashboard", toolId = ""] = value.split("/");
  return { page, toolId };
}

export function syncRoute(page, toolId = "") {
  const hash = toolId ? `#${page}/${toolId}` : `#${page}`;
  if (location.hash !== hash) history.replaceState(null, "", hash);
}
