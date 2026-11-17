// Mọi request tới backend đi qua đây (đường dẫn tương đối, chạy chung domain với FastAPI).
const BASE_URL = "/api";

async function request(method, path, body) {
  const opt = { method, headers: {} };
  if (body instanceof FormData) opt.body = body;
  else if (body !== undefined) { opt.body = JSON.stringify(body); opt.headers["Content-Type"] = "application/json"; }
  const res = await fetch(BASE_URL + path, opt);
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error((data && (typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail))) || res.statusText);
  return data;
}

const api = {
  get: (p) => request("GET", p),
  post: (p, b) => request("POST", p, b),
  put: (p, b) => request("PUT", p, b),
  del: (p) => request("DELETE", p),

  /** Dữ liệu cho dashboard, đúng dạng JSON OCR cũ mà dashboard.js dùng. */
  async dashboardData() {
    const [scada, sorted, capacity, bcr] = await Promise.all(
      ["scada", "dmwcs/sorted", "dmwcs/capacity", "dmwcs/bcr"].map(p => request("GET", "/dashboard/" + p)));
    return { scada, sorted, capacity, bcr };
  },
  upload: (files, loai, force) => {
    const fd = new FormData();
    for (const f of files) fd.append("files", f);
    if (loai) fd.append("loai", loai);
    if (force) fd.append("force", "true");
    return request("POST", "/upload", fd);
  },
  job: (id) => request("GET", `/jobs/${id}`),
  report: (id) => request("GET", `/reports/${id}`),
  saveReport: (id, data) => request("PUT", `/reports/${id}`, data),
  reocr: (id, provider, model) => request("POST", `/reports/${id}/reocr`, { provider, model }),
  providers: () => request("GET", "/system/providers"),
};

const LOAI_TEN = { scada: "SCADA", dmwcs_sorted: "DMWCS Sorted", dmwcs_capacity: "DMWCS Capacity", dmwcs_bcr_rate: "DMWCS BCR rate" };
const escHtml = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// Nút sáng/tối trên header. Chưa chọn thì theo Windows; đã chọn thì nhớ trong localStorage (đọc ở <head> mỗi trang).
const ICON_SUN = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
const ICON_MOON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
const isDark = () => {
  const t = document.documentElement.dataset.theme;
  return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
};
function syncThemeBtn() {
  const b = document.getElementById("theme-btn");
  if (!b) return;
  const label = isDark() ? "Chuyển sang chế độ sáng" : "Chuyển sang chế độ tối";
  b.innerHTML = isDark() ? ICON_SUN : ICON_MOON;
  b.setAttribute("aria-label", label);
  b.title = label;
}
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("theme-btn")?.addEventListener("click", () => {
    const t = isDark() ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("theme", t); } catch (e) {}
    syncThemeBtn();
  });
  syncThemeBtn();
});
