// Xem / sửa 1 report: ảnh gốc (bấm để zoom) + form dữ liệu. Lưu -> PUT /api/reports/{id} (status = da_sua_tay).
const id = new URLSearchParams(location.search).get("id");
const el = x => document.getElementById(x);
let report;

/** Form từ dữ liệu lồng nhau: object -> fieldset, list -> từng phần tử, lá -> input (giữ kiểu số/chuỗi). */
function fields(v, path) {
  if (Array.isArray(v)) return v.map((x, i) => fields(x, `${path}[${i}]`)).join("");
  if (v && typeof v === "object") {
    const inner = Object.entries(v).map(([k, x]) => fields(x, path ? `${path}.${k}` : k)).join("");
    return path ? `<fieldset><legend>${escHtml(path)}</legend>${inner}</fieldset>` : inner;
  }
  const name = path.split(".").pop();
  return `<label><span title="${escHtml(path)}">${escHtml(name)}</span>
    <input data-path="${escHtml(path)}" data-num="${typeof v === "number"}" value="${escHtml(v)}"></label>`;
}

function readForm() {
  const data = structuredClone(report.data);
  for (const inp of el("form").querySelectorAll("input[data-path]")) {
    const keys = inp.dataset.path.match(/[^.[\]]+/g);
    let o = data;
    keys.slice(0, -1).forEach(k => o = o[k]);
    const raw = inp.value.trim();
    o[keys.at(-1)] = inp.dataset.num === "true" && raw !== "" && !isNaN(Number(raw)) ? Number(raw) : raw;
  }
  return data;
}

function render(r) {
  report = r;
  el("title").textContent = `${LOAI_TEN[r.loai] || r.loai} · ${r.file || "report #" + r.id}`;
  el("meta").innerHTML = `Ngày báo cáo ${escHtml(r.report_date)} · <span class="status-badge ${r.status}">${r.status}</span>
    · ${escHtml(r.provider || "")} / ${escHtml(r.model || "")} · lần 2: ${escHtml(r.model_lan_2 || "—")}`;
  el("warns").innerHTML = r.canh_bao.length
    ? `<div class="warn-box"><b>Cảnh báo</b><ul>${r.canh_bao.map(c => `<li>${escHtml(c)}</li>`).join("")}</ul></div>` : "";
  if (r.image_url) el("viewer").innerHTML = `<img src="${r.image_url}" alt="Ảnh gốc">`;
  el("form").innerHTML = fields(r.data, "");
  el("json").value = JSON.stringify(r.data, null, 2);
  el("raw").textContent = JSON.stringify({ raw_json_1: r.raw_json_1, raw_json_2: r.raw_json_2, attempts: r.attempts }, null, 2);
  el("reocr").disabled = !r.upload_id;
}

async function save(data) {
  el("msg").textContent = "Đang lưu…";
  try {
    render(await api.saveReport(id, data));
    el("msg").textContent = "Đã lưu. Dashboard dùng số liệu mới.";
  } catch (e) {
    el("msg").innerHTML = `<span class="err">${escHtml(e.message)}</span>`;
  }
}

el("viewer").addEventListener("click", () => el("viewer").classList.toggle("zoom"));
el("save").addEventListener("click", () => save(readForm()));
el("save-json").addEventListener("click", () => {
  try { save(JSON.parse(el("json").value)); } catch (e) { el("msg").innerHTML = `<span class="err">JSON lỗi: ${escHtml(e.message)}</span>`; }
});
el("reocr").addEventListener("click", async () => {
  const [provider, ...m] = el("reocr-target").value.split("|");
  try {
    const { job_id } = await api.reocr(id, provider || null, m.join("|") || null);
    el("reocr-msg").textContent = "Đang OCR lại…";
    const wait = async () => {
      const j = await api.job(job_id);
      if (j.status === "done") location.href = `report.html?id=${j.report_id}`;
      else if (j.status === "failed") el("reocr-msg").innerHTML = `<span class="err">${escHtml(j.error)}</span>`;
      else { el("reocr-msg").textContent = "Đang OCR lại · " + (j.progress || "đang chờ"); setTimeout(wait, 2000); }
    };
    wait();
  } catch (e) { el("reocr-msg").innerHTML = `<span class="err">${escHtml(e.message)}</span>`; }
});
el("delete").addEventListener("click", async () => {
  if (!confirm("Xóa report này? Số liệu của nó sẽ biến mất khỏi dashboard.")) return;
  await api.del(`/reports/${id}`);
  location.href = "index.html";
});

(async () => {
  if (!id) return el("title").textContent = "Thiếu ?id= trên đường dẫn";
  try {
    render(await api.report(id));
    const ps = await api.providers();
    el("reocr-target").innerHTML += ps.filter(p => p.state !== "no_key")
      .map(p => `<option value="${escHtml(p.provider + "|" + p.model)}">${escHtml(p.provider + " / " + p.model)}</option>`).join("");
  } catch (e) {
    el("title").textContent = "Không tải được report: " + e.message;
  }
})();
