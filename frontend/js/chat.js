// Trang hỏi đáp dữ liệu: gửi câu hỏi tới POST /api/chat, hiện câu trả lời + cảnh báo + bảng.
// Bên trái: mọi cuộc trò chuyện của tài khoản chung (mọi máy). Mỗi máy nhớ cuộc đang mở của mình (localStorage).
const $ = id => document.getElementById(id);
const log = $("log"), form = $("composer"), input = $("msg"), sendBtn = $("send"), cancelBtn = $("cancel");
const CONV_KEY = "chat_conversation_id";
const SAMPLES = [
  "Hôm qua HT2 sorted tổng bao nhiêu kiện, tỷ lệ REJECT bao nhiêu %?",
  "Công suất AVG 7 ngày gần nhất thế nào?",
  "Dây chuyền nào có tỷ lệ bất thường cao nhất tuần này?",
  "BCR nào có rate thấp nhất hôm qua?",
  "Máng nào xuất hiện trong NoChute nhiều nhất 2 tuần qua?",
  "Tuần này có report nào cần kiểm tra không?",
];
const MAX_SHOWN = 200;
let convId = null, pending = null;

const store = {
  get() { try { return +localStorage.getItem(CONV_KEY) || null; } catch (e) { return null; } },
  set(v) { try { v ? localStorage.setItem(CONV_KEY, v) : localStorage.removeItem(CONV_KEY); } catch (e) {} },
};
const fmtCell = v => v === null || v === undefined ? "—"
  : typeof v === "number" ? v.toLocaleString("vi-VN", { maximumFractionDigits: 2 }) : String(v);

function bubble(role, html) {
  const el = document.createElement("article");
  el.className = "msg " + role;
  el.innerHTML = html;
  log.append(el);
  el.scrollIntoView({ block: "end", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  return el;
}

function tableHtml(cols, rows, rowCount, truncated) {
  if (!cols || !rows || !rows.length) return "";
  const shown = rows.slice(0, MAX_SHOWN);
  const head = cols.map(c => `<th>${escHtml(c)}</th>`).join("");
  const body = shown.map(r => `<tr>${r.map(v => `<td>${escHtml(fmtCell(v))}</td>`).join("")}</tr>`).join("");
  const note = truncated ? `Đang hiển thị ${shown.length} dòng đầu, kết quả còn nhiều dòng hơn.`
    : rows.length < rowCount ? `Đang hiển thị ${rows.length}/${rowCount} dòng đã lưu.` : `${rowCount} dòng`;
  return `<div class="tbl-wrap chat-tbl"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>
    <p class="note">${note}</p>`;
}

function answerHtml(r) {
  const warns = (r.warnings || []).length
    ? `<ul class="chat-warn" aria-label="Cảnh báo dữ liệu">${r.warnings.map(w => `<li>${escHtml(w)}</li>`).join("")}</ul>` : "";
  const choices = (r.lua_chon || []).length
    ? `<div class="choices">${r.lua_chon.map(c => `<button class="btn" type="button" data-choice="${escHtml(c)}">${escHtml(c)}</button>`).join("")}</div>` : "";
  const models = [r.model_sql, r.model_summary].filter(Boolean).join(" · ");
  const meta = models || r.latency_ms ? `<p class="meta">${escHtml(models)}${r.latency_ms ? ` · ${(r.latency_ms / 1000).toFixed(1)} giây` : ""}</p>` : "";
  return `<p class="answer${r.loai === "loi" ? " err" : ""}">${escHtml(r.answer || r.content || "")}</p>${warns}${choices}
    ${tableHtml(r.columns, r.rows, r.row_count, r.truncated)}${meta}`;
}

function setBusy(on) {
  sendBtn.disabled = on;
  cancelBtn.hidden = !on;
  input.readOnly = on;
}

async function ask(text) {
  text = text.trim();
  if (!text || pending) return;
  $("samples").hidden = true;
  bubble("user", `<p>${escHtml(text)}</p>`);
  input.value = "";
  const wait = bubble("bot busy", `<p class="answer">Đang truy vấn…</p>`);
  pending = new AbortController();
  setBusy(true);
  try {
    const r = await api.chat(text, convId, pending.signal);
    convId = r.conversation_id;
    store.set(convId);
    loadList();
    wait.className = "msg bot";
    wait.innerHTML = answerHtml(r);
    loadUsage();
  } catch (e) {
    wait.className = "msg bot";
    if (e.name === "AbortError") wait.innerHTML = `<p class="answer muted">Đã hủy chờ. Câu hỏi vẫn có thể đang chạy ở máy chủ.</p>`;
    else if (e.status === 401) wait.innerHTML = `<p class="answer err">Bạn cần Nhập Môn (đăng nhập) trước khi hỏi.</p>`;
    else wait.innerHTML = `<p class="answer err">Không gửi được câu hỏi: ${escHtml(e.message)}</p>`;
  } finally {
    pending = null;
    setBusy(false);
    input.focus();
  }
}

/** Mở 1 cuộc trò chuyện (của máy này hoặc máy khác); sai / đã bị xóa thì về màn hình trống. */
let openSeq = 0;
async function openConv(id) {
  const my = ++openSeq;  // bấm nhanh 2 cuộc: chỉ hiện cuộc bấm sau
  if (pending) pending.abort();
  log.innerHTML = "";
  $("samples").hidden = true;
  convId = null;
  try {
    const c = await api.conversation(id);
    if (my !== openSeq) return;
    convId = c.conversation_id;
    store.set(convId);
    for (const m of c.messages) {
      if (m.role === "user") bubble("user", `<p>${escHtml(m.content)}</p>`);
      else bubble("bot", answerHtml(m));
    }
    if (!c.messages.length) showSamples();
  } catch (e) {
    store.set(null);  // hội thoại đã bị xóa (quá 30 ngày không dùng) hoặc chưa đăng nhập
    showSamples();
  }
  markActive();
}

async function restore() {
  const id = store.get();
  if (!id) return showSamples();
  await openConv(id);
}

// ---------------------------------------------------------------- danh sách cuộc trò chuyện
const GROUPS = [[0, "Hôm nay"], [1, "Hôm qua"], [7, "7 ngày qua"], [Infinity, "30 ngày qua"]];
function ageDays(s) {
  const d = new Date(s), t = new Date();
  return Math.round((new Date(t.getFullYear(), t.getMonth(), t.getDate()) - new Date(d.getFullYear(), d.getMonth(), d.getDate())) / 864e5);
}
async function loadList() {
  let items;
  try { items = await api.conversations(); } catch (e) { return; }
  const box = $("conv-list");
  if (!items.length) { box.innerHTML = `<p class="hint">Chưa có cuộc trò chuyện nào.</p>`; return; }
  const groups = GROUPS.map(([max, ten]) => [ten, []]);
  for (const it of items) groups[GROUPS.findIndex(([max]) => ageDays(it.updated_at) <= max)][1].push(it);
  box.innerHTML = groups.filter(([, a]) => a.length).map(([ten, a]) => `<div class="conv-group"><h2>${ten}</h2>`
    + a.map(it => `<button class="conv" type="button" data-conv="${+it.conversation_id}" title="${escHtml(it.title)}">${escHtml(it.title)}</button>`).join("")
    + `</div>`).join("");
  markActive();
}
function markActive() {
  document.querySelectorAll(".conv").forEach(b => b.setAttribute("aria-current", +b.dataset.conv === convId));
}

function showSamples() {
  $("sample-list").innerHTML = SAMPLES.map(s => `<button class="btn sample" type="button" data-choice="${escHtml(s)}">${escHtml(s)}</button>`).join("");
  $("samples").hidden = false;
}

async function loadUsage() {
  try {
    const u = await api.chatUsage();
    $("usage").textContent = `Hôm nay: ${u.cau_hoi} câu hỏi, ${u.llm_calls} lượt gọi model, ${(u.tokens || 0).toLocaleString("vi-VN")} token.`;
  } catch (e) { $("usage").textContent = ""; }
}

// ---------------------------------------------------------------- sự kiện
form.addEventListener("submit", e => { e.preventDefault(); ask(input.value); });
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(input.value); }
});
cancelBtn.onclick = () => pending && pending.abort();
document.addEventListener("click", e => {
  const b = e.target.closest("[data-choice]");
  if (b) return ask(b.dataset.choice);
  const c = e.target.closest("[data-conv]");
  if (c && +c.dataset.conv !== convId) { openConv(+c.dataset.conv); toggleSide(false); }
});
function toggleSide(on) {
  $("side").classList.toggle("open", on);
  $("side-toggle").setAttribute("aria-expanded", on);
}
$("side-toggle").onclick = () => toggleSide(!$("side").classList.contains("open"));
$("new-chat").onclick = () => {
  if (pending) pending.abort();
  convId = null;
  store.set(null);
  log.innerHTML = "";
  showSamples();
  markActive();
  toggleSide(false);
  input.focus();
};

(async () => {
  if (!await api.authed) {
    bubble("bot", `<p class="answer">Bạn cần Nhập Môn (nút ở góc trên bên phải) để hỏi đáp dữ liệu.</p>`);
    setBusy(true);
    cancelBtn.hidden = true;
    return;
  }
  await restore();
  loadList();
  loadUsage();
})();
