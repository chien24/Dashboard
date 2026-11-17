// Trang upload: chọn nhiều ảnh, gửi từng ảnh (mỗi ảnh có thể chọn loại riêng), poll tiến trình job.
const items = [];  // {file, url, el, loai}
const $id = id => document.getElementById(id);

const LOAI_OPTS = `<option value="*">Theo lựa chọn chung</option><option value="">Tự nhận diện</option>`
  + Object.entries(LOAI_TEN).map(([k, v]) => `<option value="${k}">${v}</option>`).join("");

function addFiles(files) {
  for (const file of files) {
    if (!/\.(jpe?g|png|webp)$/i.test(file.name)) continue;
    const it = { file, url: URL.createObjectURL(file) };
    it.el = document.createElement("div");
    it.el.className = "item";
    it.el.innerHTML = `<img src="${it.url}" alt="">
      <div><div class="item-head"><span class="name">${escHtml(file.name)}</span>
        <select class="loai">${LOAI_OPTS}</select><span class="state">Chưa gửi</span></div></div>
      <div class="result"></div>`;
    items.push(it);
    $id("items").append(it.el);
  }
  $id("start").disabled = !items.some(i => !i.sent);
}

const drop = $id("drop");
drop.addEventListener("dragover", e => { e.preventDefault(); drop.classList.add("over"); });
drop.addEventListener("dragleave", () => drop.classList.remove("over"));
drop.addEventListener("drop", e => { e.preventDefault(); drop.classList.remove("over"); addFiles(e.dataTransfer.files); });
$id("pick").addEventListener("change", e => { addFiles(e.target.files); e.target.value = ""; });
$id("clear").addEventListener("click", () => { items.length = 0; $id("items").innerHTML = ""; $id("start").disabled = true; });

function setState(it, text, cls = "") {
  const s = it.el.querySelector(".state");
  s.className = "state " + cls;
  s.innerHTML = text;
}

async function send(it, force = false) {
  const sel = it.el.querySelector(".loai").value;
  const loai = sel === "*" ? $id("loai-all").value : sel;
  it.sent = true;
  setState(it, "Đang gửi…");
  try {
    const [r] = await api.upload([it.file], loai, force);
    if (r.duplicate) {
      setState(it, `Ảnh đã được xử lý trước đó${r.report_id ? ` · <a href="report.html?id=${r.report_id}">xem kết quả cũ</a>` : ""}
        · <button class="btn" data-again>OCR lại</button>`, "dup");
      it.el.querySelector("[data-again]").onclick = () => send(it, true);
      if (r.report_id) showReport(it, r.report_id);
      return;
    }
    poll(it, r.job_id);
  } catch (e) {
    setState(it, "Lỗi: " + escHtml(e.message), "failed");
  }
}

async function poll(it, jobId) {
  const job = await api.job(jobId).catch(e => ({ status: "failed", error: e.message }));
  if (job.status === "pending") setState(it, "Đang chờ");
  else if (job.status === "running") setState(it, "Đang OCR · " + escHtml(job.progress || ""));
  if (job.status === "pending" || job.status === "running") return setTimeout(() => poll(it, jobId), 2000);
  if (job.status === "failed") return setState(it, "Lỗi: " + escHtml(job.error), "failed");
  setState(it, `Xong · ${escHtml(job.progress || "")} · <a href="report.html?id=${job.report_id}">Xem / Sửa</a>`, "done");
  showReport(it, job.report_id);
  renderProviders();
}

/** Bảng kết quả: cảnh báo tô vàng, trường lệch giữa 2 lần OCR tô đỏ. */
async function showReport(it, id) {
  const r = await api.report(id);
  const lech = new Set(r.canh_bao.filter(c => c.startsWith("Lệch giữa"))
    .map(c => (c.match(/\) ([^:]+):/) || [])[1]).filter(Boolean));
  const rows = Object.entries(flatten(r.data)).map(([k, v]) =>
    `<tr class="${lech.has(k) ? "lech" : ""}"><td class="l">${escHtml(k)}</td><td>${escHtml(v)}</td></tr>`).join("");
  it.el.querySelector(".result").innerHTML =
    `<div class="item-head"><b>${LOAI_TEN[r.loai] || r.loai}</b><span class="status-badge ${r.status}">${r.status}</span>
       <span class="hint">${escHtml(r.provider)} / ${escHtml(r.model)} · lần 2: ${escHtml(r.model_lan_2 || "—")}</span></div>`
    + (r.canh_bao.length ? `<div class="warn-box"><b>Cảnh báo</b><ul>${r.canh_bao.map(c => `<li>${escHtml(c)}</li>`).join("")}</ul></div>` : "")
    + `<details><summary>Dữ liệu đọc được (${lech.size} trường lệch)</summary><div class="tbl-wrap"><table>${rows}</table></div></details>`;
  if (lech.size) it.el.querySelector(".result details").open = true;
}

function flatten(v, p = "", out = {}) {
  if (Array.isArray(v)) v.forEach((x, i) => flatten(x, `${p}[${i}]`, out));
  else if (v && typeof v === "object") for (const [k, x] of Object.entries(v)) flatten(x, p ? `${p}.${k}` : k, out);
  else out[p] = v;
  return out;
}

$id("start").addEventListener("click", async () => {
  $id("start").disabled = true;
  for (const it of items.filter(i => !i.sent)) await send(it);  // gửi lần lượt; backend cũng xử lý tuần tự
});
