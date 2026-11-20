// Mọi request tới backend đi qua đây (đường dẫn tương đối, chạy chung domain với FastAPI).
const BASE_URL = "/api";

async function request(method, path, body, signal) {
  const opt = { method, headers: {}, signal };
  if (body instanceof FormData) opt.body = body;
  else if (body !== undefined) { opt.body = JSON.stringify(body); opt.headers["Content-Type"] = "application/json"; }
  const res = await fetch(BASE_URL + path, opt);
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const d = data && data.detail;  // chuỗi, hoặc object {message, ...} (vd đăng nhập sai: fails / retry_after)
    const msg = typeof d === "string" ? d : (d && d.message) || (d && JSON.stringify(d)) || res.statusText;
    throw Object.assign(new Error(msg), { status: res.status, detail: d });
  }
  return data;
}

const api = {
  get: (p) => request("GET", p),
  post: (p, b) => request("POST", p, b),
  put: (p, b) => request("PUT", p, b),
  del: (p) => request("DELETE", p),

  /** Đã đăng nhập chưa: hỏi server 1 lần mỗi trang, các trang await api.authed trước khi tải dữ liệu. */
  authed: fetch(BASE_URL + "/auth/me").then(r => r.json()).then(d => !!d.logged_in).catch(() => false),
  login: (username, password) => request("POST", "/auth/login", { username, password }),
  logout: () => request("POST", "/auth/logout"),

  /** Dữ liệu cho dashboard, đúng dạng JSON OCR cũ mà dashboard.js dùng. Chưa đăng nhập: rỗng (dashboard hiện ô trống). */
  async dashboardData() {
    if (!await api.authed) return { scada: [], sorted: [], capacity: [], bcr: [] };
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
  saveReport: (id, data, updatedAt) => request("PUT", `/reports/${id}?updated_at=${encodeURIComponent(updatedAt)}`, data),
  reocr: (id, provider, model) => request("POST", `/reports/${id}/reocr`, { provider, model }),
  providers: () => request("GET", "/system/providers"),
  chat: (message, conversationId, signal) => request("POST", "/chat", { message, conversation_id: conversationId ?? null }, signal),
  conversation: (id) => request("GET", `/chat/conversations/${id}`),
  conversations: () => request("GET", "/chat/conversations"),
  chatUsage: () => request("GET", "/chat/usage"),
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
// Footer dùng chung cho mọi trang (chèn bằng JS để không phải chép HTML vào từng trang).
const MAP_URL = "https://maps.app.goo.gl/Rrd8YQa3xhNANA6b9";
const SUPPORT_EMAIL = "chiencodedao@gmail.com";
const ICON = {
  pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
  user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
  up: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>',
};
const FOOTER = `<footer class="site-foot">
  <div class="foot-in">
    <div class="foot-brand">
      <img src="../img/logo_viettel_post.webp" alt="Viettel Post" width="93" height="36">
      <p class="foot-name">Viettel Post CNKT 3</p>
      <p class="foot-sub">Phòng Kỹ thuật · Chi nhánh Khai thác 3</p>
      <a class="foot-line" href="${MAP_URL}" target="_blank" rel="noopener">${ICON.pin}<span>Xem địa chỉ trên Google Maps</span></a>
    </div>
    <div class="foot-col">
      <h4>Gặp Kiếp Nạn</h4>
      <p class="foot-line">${ICON.user}<span>Cầu cứu Chấp Sự Khoa (Khoa Tôn giả) · Trấn Thủ Phòng Kỹ Thuật - Thiên Cơ Điện</span></p>
      <p class="foot-hint">Truyền Âm Phù khi hệ thống nghịch loạn hoặc đứt đoạn linh mạch:</p>
      <a class="foot-line" href="mailto:${SUPPORT_EMAIL}">${ICON.mail}<span>${SUPPORT_EMAIL}</span></a>
    </div>
    <div class="foot-col">
      <h4>Dẫn Lộ Bàn</h4>
      <a href="index.html">Thiên Cơ Các</a><a href="upload.html">Truyền Pháp Ảnh</a><a href="history.html">Tàng Kinh Các</a><a href="chat.html">Vấn Đạo Đài</a>
    </div>
  </div>
  <div class="foot-bottom">
    <span>© ${new Date().getFullYear()} Viettel Post CNKT 3 · Phòng Kỹ thuật · OCR Dashboard</span>
    <button class="to-top" id="to-top" type="button" aria-label="Lên đầu trang" title="Lên đầu trang">${ICON.up}</button>
  </div>
</footer>`;

// Nút Đăng nhập / Đăng xuất trên header + hộp thoại đăng nhập (1 tài khoản dùng chung).
const LOGIN_DLG = `<dialog class="login-dlg" id="login-dlg" aria-labelledby="login-h">
  <form id="login-form">
    <h2 id="login-h">Nhập Môn</h2>
    <label>Tài khoản<input name="username" autocomplete="username" required></label>
    <label>Mật khẩu<input name="password" type="password" autocomplete="current-password" required></label>
    <div role="alert"><p class="err" id="login-err"></p><p class="login-hint" id="login-hint"></p></div>
    <div class="login-actions"><button class="btn" type="button" id="login-cancel">Hủy</button>
      <button class="btn primary" type="submit">Nhập Môn</button></div>
  </form>
</dialog>`;
const LOGIN_FAIL = "Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!";
// Câu phụ cho lần sai thứ 2, 3, 4... (theo thứ tự, càng về sau càng nặng lời)
const FAIL_HINTS = [
  "Linh lực bất định, niệm chú sai bét! Đồ nhi ngoan, ngươi đang mượn cớ để được sư tôn gõ đầu đúng không?",
  "Kẻ trí nhớ kém như ngươi mà cũng đòi nghịch thiên phá trận ư? Về Tàng Kinh Các chép lại một vạn lần khẩu quyết đi!",
  "Nhập sai thêm lần nữa, bản tọa sẽ lột sạch tiên tịch, đày ngươi xuống phàm trần nuôi heo suốt ba kiếp đấy!",
  "Nghịch tử, ngươi đang thử thách sự kiên nhẫn của Thiên Đạo đấy à? Hồn phách chuẩn bị chịu đòn roi lôi kiếp đi!",
  "Vi phạm thiên quy nhiều lần, nguyên thần của ngươi xem ra không muốn giữ nữa rồi!",
];
/** Câu phụ theo số lần đã sai (server đếm): lần 1, lần 2..6 (FAIL_HINTS), lần áp chót. */
function failHint(fails, max) {
  if (fails === 1) return `Nghịch thiên cải mệnh? Ta cho ngươi ${max - 1} lần giãy giụa nữa!`;
  if (fails === max - 1) return "Thiên uy khó phạm, ngươi chỉ còn duy nhất một lần cuối!";
  return FAIL_HINTS[fails - 2] || "";
}
/** Sai quá số lần: nhốt ở trang phong ấn tới khi hết khóa (server báo số giây còn lại). */
function goJail(seconds) {
  const until = Date.now() + (seconds || 300) * 1000;
  try { localStorage.setItem("jail_until", until); } catch (e) {}
  location.replace("jail.html?until=" + until);
}

/** Thông báo nổi góc phải dưới (dùng chung mọi trang). kind: ok | warn | fail. Lỗi giữ tới khi đóng, còn lại tự ẩn sau 8s. */
function toast(kind, html) {
  let box = document.getElementById("toasts");
  if (!box) {
    box = Object.assign(document.createElement("div"), { id: "toasts" });
    box.setAttribute("aria-live", "polite");
    document.body.append(box);
  }
  const t = document.createElement("div");
  t.className = "toast " + kind;
  t.setAttribute("role", kind === "fail" ? "alert" : "status");
  t.innerHTML = `<div>${html}</div><button type="button" aria-label="Đóng thông báo">×</button>`;
  t.querySelector("button").onclick = () => t.remove();
  box.append(t);
  while (box.children.length > 4) box.firstElementChild.remove();
  if (kind !== "fail") setTimeout(() => t.remove(), 8000);
}
/** Đăng nhập / đăng xuất xong phải reload để tải lại dữ liệu: giữ thông báo qua lần reload rồi mới hiện. */
function reloadWithToast(kind, text) {
  try { sessionStorage.setItem("flash", JSON.stringify([kind, text])); } catch (e) {}
  location.reload();
}
function showFlash() {
  try {
    const f = JSON.parse(sessionStorage.getItem("flash") || "null");
    sessionStorage.removeItem("flash");
    if (f) toast(f[0], escHtml(f[1]));
  } catch (e) {}
}

async function initAuth() {
  const theme = document.getElementById("theme-btn");
  if (!theme) return;
  const btn = Object.assign(document.createElement("button"), { type: "button", className: "auth-btn" });
  theme.before(btn);
  if (await api.authed) {
    btn.textContent = "Xuất Môn";
    btn.onclick = async () => { await api.logout().catch(() => {}); reloadWithToast("ok", "Xuất Môn thành công. Hẹn ngày tái ngộ!"); };
    return;
  }
  btn.textContent = "Nhập Môn";
  document.body.insertAdjacentHTML("beforeend", LOGIN_DLG);
  const dlg = document.getElementById("login-dlg"), form = document.getElementById("login-form");
  const err = document.getElementById("login-err"), hint = document.getElementById("login-hint");
  const say = (a, b = "") => { err.textContent = a; hint.textContent = b; };
  btn.onclick = () => { say(""); dlg.showModal(); };
  document.getElementById("login-cancel").onclick = () => dlg.close();
  form.addEventListener("submit", async e => {
    e.preventDefault();
    say("");
    try {
      await api.login(form.username.value.trim(), form.password.value);
      reloadWithToast("ok", "Nhập Môn thành công. Chào mừng đạo hữu!");
    } catch (x) {
      if (x.status === 429) return goJail(x.detail && x.detail.retry_after);
      if (x.status === 401 && x.detail && x.detail.fails) say(LOGIN_FAIL, failHint(x.detail.fails, x.detail.max_fails));
      else say(x.message);  // lỗi mạng / server
      form.password.select();
    }
  });
}

// Logo Thiên Đạo: sao 8 cánh + vòng xoáy + khung kim loại có cánh. SVG nhúng thẳng để đổi màu theo sáng/tối (token --logo-* trong base.css).
const LOGO_THIEN_DAO = `<svg class="welcome-logo" viewBox="0 0 120 120" width="136" height="136" role="img" aria-label="Logo Thiên Đạo">
  <defs>
    <linearGradient id="wl-metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#aeb7c4"/><stop offset=".6" stop-color="#eef1f5"/><stop offset="1" stop-color="#5f6879"/>
    </linearGradient>
    <radialGradient id="wl-core" cx="50%" cy="45%" r="60%">
      <stop offset="0" style="stop-color: var(--logo-core)"/><stop offset="1" style="stop-color: var(--logo-core-2)"/>
    </radialGradient>
    <radialGradient id="wl-star" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#bfe8ff"/><stop offset="1" style="stop-color: var(--logo-swirl)"/>
    </radialGradient>
    <filter id="wl-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g fill="url(#wl-metal)" stroke="#3b4658" stroke-width=".6">
    <path d="M6 58l13-5v10z"/><path d="M114 58l-13-5v10z"/><path d="M60 4l-4.5 10h9z"/>
  </g>
  <circle cx="60" cy="58" r="40" fill="url(#wl-core)"/>
  <g class="wl-swirl" fill="none" stroke-linecap="round" filter="url(#wl-glow)">
    <path d="M28 44A34 34 0 0 1 94 48" style="stroke: var(--logo-swirl)" stroke-width="2.6"/>
    <path d="M92 74A34 34 0 0 1 27 70" style="stroke: var(--logo-accent)" stroke-width="2.2"/>
    <path d="M40 27A32 32 0 0 1 84 32" style="stroke: var(--logo-swirl)" stroke-width="1.2" opacity=".6"/>
    <path d="M84 88A32 32 0 0 1 36 87" style="stroke: var(--logo-swirl)" stroke-width="1.2" opacity=".5"/>
  </g>
  <g fill="#ffffff"><circle cx="38" cy="38" r=".9"/><circle cx="84" cy="40" r="1.1"/><circle cx="44" cy="80" r=".8"/><circle cx="80" cy="76" r=".9"/><circle cx="70" cy="34" r=".7"/></g>
  <circle cx="60" cy="58" r="44" fill="none" stroke="url(#wl-metal)" stroke-width="5"/>
  <circle cx="60" cy="58" r="40.5" fill="none" style="stroke: var(--logo-accent)" stroke-width="1" opacity=".8"/>
  <path d="M60 40l3 15 15 3-15 3-3 15-3-15-15-3 15-3z" style="fill: var(--logo-accent)" opacity=".85" transform="rotate(45 60 58)"/>
  <path d="M60 30l1.9 23.4 8-5.3-5.3 8L88 58l-23.4 1.9 5.3 8-8-5.3L60 86l-1.9-23.4-8 5.3 5.3-8L32 58l23.4-1.9-5.3-8 8 5.3z"
        fill="url(#wl-star)" style="stroke: var(--logo-star-edge)" stroke-width=".8" stroke-linejoin="round" filter="url(#wl-glow)"/>
  <g fill="url(#wl-metal)" stroke="#3b4658" stroke-width=".6" stroke-linejoin="round">
    <path d="M60 116C51 106 41 98 20 93c13-1 22 0 29 3-8-7-15-14-19-25 9 9 18 17 30 25z"/>
    <path d="M60 116C69 106 79 98 100 93c-13-1-22 0-29 3 8-7 15-14 19-25-9 9-18 17-30 25z"/>
  </g>
</svg>`;
// Popup chào mừng: chỉ hiện lần đầu mở web trong phiên (sessionStorage), reload hay chuyển trang không hiện lại.
const WELCOME = `<dialog class="welcome-dlg" id="welcome-dlg" aria-labelledby="welcome-h" aria-describedby="welcome-p" tabindex="-1">
  <button class="welcome-x" type="button" data-close aria-label="Đóng">✕</button>
  ${LOGO_THIEN_DAO}
  <h2 id="welcome-h">Chào mừng bạn đến với hệ thống Thiên Đạo</h2>
  <p id="welcome-p">Chào mừng bạn đã gia nhập hệ thống giám sát và vận hành Thiên Đạo. Hãy cùng khám phá và tối ưu hóa hiệu suất ngay hôm nay!</p>
  <div class="welcome-actions"><button class="welcome-go" type="button" data-close>Bắt đầu ngay</button>
    <button class="welcome-skip" type="button" data-close>Bỏ qua</button></div>
</dialog>`;
function showWelcome() {
  try {
    if (sessionStorage.getItem("welcomed")) return;
    sessionStorage.setItem("welcomed", "1");
  } catch (e) { return; }  // trình duyệt chặn storage: không hiện, tránh hiện lại mỗi lần reload
  document.body.insertAdjacentHTML("beforeend", WELCOME);
  const dlg = document.getElementById("welcome-dlg");
  dlg.querySelectorAll("[data-close]").forEach(b => b.onclick = () => dlg.close());
  dlg.querySelector(".welcome-go").onclick = async () => {  // "Bắt đầu ngay": chưa đăng nhập thì mở luôn hộp đăng nhập
    dlg.close();
    if (!await api.authed) document.querySelector(".auth-btn")?.click();
  };
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });  // bấm ra nền tối thì đóng
  dlg.addEventListener("close", () => dlg.remove());
  dlg.showModal();
  dlg.focus();  // focus vào popup chứ không vào nút X (tránh viền focus ngay khi mở); Tab vẫn đi tới các nút
}

document.addEventListener("DOMContentLoaded", () => {
  document.body.insertAdjacentHTML("beforeend", FOOTER);
  initAuth();
  showWelcome();
  showFlash();
  document.getElementById("to-top").addEventListener("click", () =>
    scrollTo({ top: 0, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }));
  document.getElementById("theme-btn")?.addEventListener("click", () => {
    const t = isDark() ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("theme", t); } catch (e) {}
    syncThemeBtn();
  });
  syncThemeBtn();
});
