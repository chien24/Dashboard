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

// Thanh trạng thái provider trên cùng (mọi trang có #providers)
async function renderProviders() {
  const el = document.getElementById("providers");
  if (!el) return;
  try {
    const rows = await api.providers();
    const ten = { active: "sẵn sàng", cooldown: "tạm nghỉ", disabled: "tắt", no_key: "chưa có key" };
    el.innerHTML = rows.map(r => `<span class="pill ${r.state}" title="${escHtml(
      `${r.provider}/${r.model}: ${ten[r.state] || r.state}${r.cooldown_until ? " tới " + r.cooldown_until : ""}${r.last_error ? "\n" + r.last_error : ""}`)}">${
      escHtml(r.provider)} · ${escHtml(r.model.split("/").pop())}</span>`).join("");
  } catch (e) {
    el.textContent = "Không đọc được trạng thái provider";
  }
}
document.addEventListener("DOMContentLoaded", () => { renderProviders(); setInterval(renderProviders, 30000); });
