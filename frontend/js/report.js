// Xem / sửa 1 report: ảnh gốc (bấm để zoom) + form dữ liệu. Lưu -> PUT /api/reports/{id} (status = da_sua_tay).
// "Thêm giá trị" thêm 1 dòng vào danh sách của report; "OCR Version" = mọi lần OCR của ảnh, quay về bản nào cũng được.
const id = new URLSearchParams(location.search).get("id");
const el = x => document.getElementById(x);
let report, cur;  // cur = dữ liệu đang hiện trên form (có thể đã thêm / bớt dòng, chưa lưu)

// Danh sách thêm dòng được, và dòng mẫu khi danh sách đang rỗng. Sorted không có danh sách.
const LIST = {
  scada: ["phan_bo_bat_thuong", { loai: "", so_luong: 0, ty_le: 0 }],
  dmwcs_capacity: ["cong_suat_theo_ngay", { ngay: "", cong_suat: 0 }],
  dmwcs_bcr_rate: ["bcr", { bcr_no: 0, total: 0, success: 0, failed: 0, rate: 0 }],
};

/** Form từ dữ liệu lồng nhau: object -> fieldset, list -> từng phần tử (có nút xóa dòng), lá -> input (giữ kiểu số/chuỗi). */
function fields(v, path, del) {
  if (Array.isArray(v)) return v.map((x, i) => fields(x, `${path}[${i}]`, [path, i])).join("");
  if (v && typeof v === "object") {
    const inner = Object.entries(v).map(([k, x]) => fields(x, path ? `${path}.${k}` : k)).join("");
    const x = del ? ` <button class="row-x" type="button" data-del="${escHtml(del[0])}" data-i="${del[1]}">Xóa dòng</button>` : "";
    return path ? `<fieldset data-path="${escHtml(path)}"><legend>${escHtml(path)}${x}</legend>${inner}</fieldset>` : inner;
  }
  const name = path.split(".").pop();
  return `<label><span title="${escHtml(path)}">${escHtml(name)}</span>
    <input data-path="${escHtml(path)}" data-num="${typeof v === "number"}" value="${escHtml(v)}"></label>`;
}

function readForm() {
  const data = structuredClone(cur);
  for (const inp of el("form").querySelectorAll("input[data-path]")) {
    const keys = inp.dataset.path.match(/[^.[\]]+/g);
    let o = data;
    keys.slice(0, -1).forEach(k => o = o[k]);
    const raw = inp.value.trim();
    o[keys.at(-1)] = inp.dataset.num === "true" && raw !== "" && !isNaN(Number(raw)) ? Number(raw) : raw;
  }
  return data;
}

function renderForm(data) {
  cur = data;
  el("form").innerHTML = fields(data, "");
}

const when = s => s ? `${s.slice(8, 10)}/${s.slice(5, 7)} ${s.slice(11, 16)}` : "";

function renderVersions(r) {
  const vs = r.versions || [];
  const key = v => `${v.report_id}:${v.lan}`;  // khớp ocr_dang_dung của backend
  const sua = vs.length && !vs.some(v => key(v) === r.ocr_dang_dung)
    ? `<p class="hint">Đang dùng: <b>bản sửa tay</b> (số đã được sửa, không trùng lần OCR nào bên dưới).</p>` : "";
  el("versions").innerHTML = sua + (vs.length ? vs.map((v, i) => `<div class="ver">
      <div class="ver-head"><b>OCR lần ${i + 1}</b>
        <span class="hint">${escHtml(when(v.created_at))}${v.report_id !== r.id ? ` · report #${+v.report_id}` : ""}</span>
        ${key(v) === r.ocr_dang_dung ? `<span class="status-badge ok">Đang dùng</span>` : ""}
        <button class="btn" type="button" data-ver="${i}">Dùng bản này</button></div>
      <details><summary>Xem JSON</summary><pre class="raw">${escHtml(JSON.stringify(v.data, null, 2))}</pre></details>
    </div>`).join("") : `<p class="hint">Không có bản OCR nào (report import từ JSON).</p>`);
}

function render(r) {
  report = r;
  el("title").textContent = `${LOAI_TEN[r.loai] || r.loai} · ${r.file || "report #" + r.id}`;
  el("meta").innerHTML = `Ngày báo cáo ${escHtml(r.report_date)} · <span class="status-badge ${escHtml(r.status)}">${escHtml(r.status)}</span>
    · ${escHtml(r.provider || "")} / ${escHtml(r.model || "")} · lần 2: ${escHtml(r.model_lan_2 || "—")}`;
  el("warns").innerHTML = r.canh_bao.length
    ? `<div class="warn-box"><b>Cảnh báo</b><ul>${r.canh_bao.map(c => `<li>${escHtml(c)}</li>`).join("")}</ul></div>` : "";
  if (r.image_url) el("viewer").innerHTML = `<img src="${escHtml(r.image_url)}" alt="Ảnh gốc">`;
  renderForm(structuredClone(r.data));
  renderVersions(r);
  el("add-row").hidden = !LIST[r.loai];
  el("reocr").disabled = !r.upload_id;
}

async function save(data, done = "Đã lưu. Dashboard dùng số liệu mới.", ocrVersion = null) {
  el("msg").textContent = "Đang lưu…";
  try {
    render(await api.saveReport(id, data, report.updated_at, ocrVersion));
    el("msg").textContent = done;
  } catch (e) {
    el("msg").innerHTML = `<span class="err">${escHtml(e.message)}</span>`;
  }
}

el("viewer").addEventListener("click", () => el("viewer").classList.toggle("zoom"));
el("save").addEventListener("click", () => save(readForm()));

el("add-row").addEventListener("click", () => {
  const [key, tpl] = LIST[report.loai];
  const data = readForm(), list = data[key] || (data[key] = []);
  // dòng mới theo dòng đầu (số -> 0, chữ -> rỗng), danh sách rỗng thì theo mẫu
  const row = list.length ? Object.fromEntries(Object.entries(list[0]).map(([k, v]) => [k, typeof v === "number" ? 0 : ""])) : { ...tpl };
  list.push(row);
  renderForm(data);
  const box = el("form").querySelector(`fieldset[data-path="${key}[${list.length - 1}]"]`);
  box.scrollIntoView({ block: "center" });
  box.querySelector("input").focus();
  el("msg").textContent = "Đã thêm 1 dòng. Điền giá trị rồi bấm Lưu.";
});

el("form").addEventListener("click", e => {
  const b = e.target.closest("[data-del]");
  if (!b) return;
  const data = readForm();
  data[b.dataset.del].splice(+b.dataset.i, 1);
  renderForm(data);
  el("msg").textContent = "Đã bỏ 1 dòng. Bấm Lưu để lưu lại.";
});

el("versions").addEventListener("click", e => {
  const b = e.target.closest("[data-ver]");
  if (!b) return;
  const n = +b.dataset.ver + 1;
  if (!confirm(`Thay số liệu đang dùng bằng OCR lần ${n}? Số đang có (kể cả phần đã sửa tay) sẽ bị thay.`)) return;
  const v = report.versions[n - 1];
  save(structuredClone(v.data), `Đã quay về OCR lần ${n}. Dashboard dùng số liệu này.`, `${v.report_id}:${v.lan}`);
});

el("reocr").addEventListener("click", async () => {
  el("reocr").disabled = true;
  try {
    const { job_id } = await api.reocr(id, null, null);
    el("msg").textContent = "Đang OCR lại…";
    const wait = async () => {
      const j = await api.job(job_id);
      if (j.status === "done") location.href = `report.html?id=${j.report_id}`;
      else if (j.status === "failed") { el("msg").innerHTML = `<span class="err">${escHtml(j.error)}</span>`; el("reocr").disabled = false; }
      else { el("msg").textContent = "Đang OCR lại · " + (j.progress || "đang chờ"); setTimeout(wait, 2000); }
    };
    wait();
  } catch (e) {
    el("msg").innerHTML = `<span class="err">${escHtml(e.message)}</span>`;
    el("reocr").disabled = false;
  }
});

el("delete").addEventListener("click", async () => {
  if (!confirm("Xóa report này? Số liệu của nó sẽ biến mất khỏi dashboard.")) return;
  await api.del(`/reports/${id}`);
  location.href = "index.html";
});

(async () => {
  if (!id) return el("title").textContent = "Thiếu ?id= trên đường dẫn";
  if (!await api.authed) {
    el("title").textContent = "Chưa nhập môn, không thể xem / sửa report";
    ["save", "add-row", "reocr", "delete"].forEach(k => el(k).disabled = true);
    return;
  }
  try {
    render(await api.report(id));
  } catch (e) {
    el("title").textContent = "Không tải được report: " + e.message;
  }
})();
