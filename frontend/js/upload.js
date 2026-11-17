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
        <select class="loai">${LOAI_OPTS}</select>
        <div class="progress" hidden role="progressbar" aria-label="Tiến trình OCR" aria-valuemin="0" aria-valuemax="100"><div class="bar"></div></div>
        <span class="state">Chưa gửi</span><span class="elapsed hint"></span></div></div>
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

/** Thanh tiến trình. kind: busy (đang chạy, có sọc chạy) | done | warn | failed. */
function setProgress(it, pct, kind) {
  const p = it.el.querySelector(".progress");
  p.hidden = false;
  p.className = "progress " + kind;
  p.setAttribute("aria-valuenow", pct);
  p.querySelector(".bar").style.width = pct + "%";
}

/** % ước lượng từ bước backend báo về: nhận diện loại -> OCR lần 1..N -> ghi DB. */
function pctOf(job) {
  if (job.status === "pending") return 5;
  const m = (job.progress || "").match(/lần (\d+)\/(\d+)/);
  if (m) return Math.round(25 + 60 * (m[1] - 1) / m[2] + 10);
  return /nhận diện/.test(job.progress || "") ? 15 : 10;
}

function tickElapsed(it) {
  const s = Math.round((Date.now() - it.t0) / 1000);
  it.el.querySelector(".elapsed").textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Bỏ tên exception ở đầu lỗi backend ("ValueError: ...") cho dễ đọc. */
const niceError = e => String(e || "Lỗi không rõ").replace(/^[A-Za-z]+(Error|Failed|Exception)?: /, "");

/** Thông báo nổi góc phải dưới. kind: ok | warn | fail. Lỗi giữ tới khi đóng, còn lại tự ẩn sau 8s. */
function toast(kind, html) {
  const box = $id("toasts");
  const t = document.createElement("div");
  t.className = "toast " + kind;
  t.setAttribute("role", kind === "fail" ? "alert" : "status");
  t.innerHTML = `<div>${html}</div><button type="button" aria-label="Đóng thông báo">×</button>`;
  t.querySelector("button").onclick = () => t.remove();
  box.append(t);
  while (box.children.length > 4) box.firstElementChild.remove();
  if (kind !== "fail") setTimeout(() => t.remove(), 8000);
}

function finish(it, kind, stateHtml, toastHtml) {
  clearInterval(it.timer);
  tickElapsed(it);
  setProgress(it, 100, kind === "fail" ? "failed" : kind === "warn" ? "warn" : "done");
  setState(it, stateHtml, kind === "fail" ? "failed" : kind === "warn" ? "dup" : "done");
  toast(kind, toastHtml);
}

async function send(it, force = false) {
  const sel = it.el.querySelector(".loai").value;
  const loai = sel === "*" ? $id("loai-all").value : sel;
  it.sent = true;
  it.el.querySelector(".loai").disabled = true;
  it.t0 = Date.now();
  clearInterval(it.timer);
  it.timer = setInterval(() => tickElapsed(it), 1000);
  it.el.querySelector(".result").innerHTML = "";
  setProgress(it, 3, "busy");
  setState(it, "Đang gửi ảnh…");
  try {
    const [r] = await api.upload([it.file], loai, force);
    if (r.duplicate && !r.report_id && r.job_id) return poll(it, r.job_id);  // ảnh trùng còn đang OCR dở: theo dõi luôn job đó
    if (r.duplicate) {
      finish(it, "warn", `Ảnh đã được xử lý trước đó${r.report_id ? ` · <a href="report.html?id=${r.report_id}">xem kết quả cũ</a>` : ""}
        · <button class="btn" data-again>OCR lại</button>`, `<b>${escHtml(it.file.name)}</b><br>Ảnh này đã OCR trước đó, đang hiện kết quả cũ.`);
      it.el.querySelector("[data-again]").onclick = () => send(it, true);
      if (r.report_id) showReport(it, r.report_id);
      return;
    }
    poll(it, r.job_id);
  } catch (e) {
    failed(it, e.message);
  }
}

function failed(it, err) {
  const msg = escHtml(niceError(err));
  finish(it, "fail", "✕ Thất bại", `<b>OCR thất bại: ${escHtml(it.file.name)}</b><br>${msg}`);
  it.el.querySelector(".result").innerHTML = `<div class="err-box"><b>Không đọc được ảnh này.</b> ${msg}
    <br><button class="btn" data-retry>Thử lại</button> <span class="hint">Có thể chọn đúng loại ảnh ở ô bên cạnh tên file rồi thử lại.</span></div>`;
  it.el.querySelector(".loai").disabled = false;
  it.el.querySelector("[data-retry]").onclick = () => send(it, true);
}

async function poll(it, jobId) {
  const job = await api.job(jobId).catch(e => ({ status: "failed", error: "Mất kết nối tới server: " + e.message }));
  if (job.status === "pending" || job.status === "running") {
    setProgress(it, pctOf(job), "busy");
    setState(it, job.status === "pending" ? "Đang chờ tới lượt" : "Đang OCR · " + escHtml(job.progress || ""));
    return setTimeout(() => poll(it, jobId), 2000);
  }
  if (job.status === "failed") return failed(it, job.error);
  const r = await showReport(it, job.report_id).catch(() => null);
  const link = `<a href="report.html?id=${job.report_id}">Xem / Sửa</a>`;
  if (r && r.status === "can_kiem_tra")
    finish(it, "warn", `✓ Xong, cần kiểm tra · ${link}`,
      `<b>${escHtml(it.file.name)}</b><br>OCR xong nhưng có ${r.canh_bao.length} cảnh báo, nên kiểm tra lại số liệu. ${link}`);
  else finish(it, "ok", `✓ Thành công · ${link}`, `<b>${escHtml(it.file.name)}</b><br>OCR thành công (${escHtml(LOAI_TEN[r?.loai] || r?.loai || "")}). ${link}`);
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
  return r;
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
