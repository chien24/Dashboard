// Nút chat nổi góc phải dưới (mọi trang trừ Vấn Đạo Đài): khung nhỏ chỉ để hỏi nhanh.
// Không tải lịch sử; dùng chung hội thoại với trang chat.html nên lịch sử xem ở Vấn Đạo Đài. Cần api.js nạp trước.
(() => {
  const CONV_KEY = "chat_conversation_id";
  // Icon: nền đỏ thương hiệu + viền kim loại như logo Thiên Đạo, bong bóng chat có sao 4 cánh (hỏi Thiên Đạo).
  const ICON = `<svg viewBox="0 0 64 64" width="60" height="60" aria-hidden="true">
    <defs>
      <radialGradient id="cw-bg" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#ff4d6d"/><stop offset=".55" stop-color="#ee0033"/><stop offset="1" stop-color="#9e0022"/></radialGradient>
      <linearGradient id="cw-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#b9c1cc"/><stop offset=".65" stop-color="#f1f3f6"/><stop offset="1" stop-color="#6b7485"/></linearGradient>
      <linearGradient id="cw-star" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff5c77"/><stop offset="1" stop-color="#c8002b"/></linearGradient>
    </defs>
    <circle cx="32" cy="32" r="29" fill="url(#cw-bg)"/>
    <circle cx="32" cy="32" r="29.5" fill="none" stroke="url(#cw-metal)" stroke-width="3"/>
    <path d="M26 18h12a9 9 0 0 1 9 9v4a9 9 0 0 1-9 9H28l-8 6 1.6-7.4A9 9 0 0 1 17 31v-4a9 9 0 0 1 9-9z" fill="#fff"/>
    <path d="M32 21.5c.8 5 2.5 6.7 7.5 7.5-5 .8-6.7 2.5-7.5 7.5-.8-5-2.5-6.7-7.5-7.5 5-.8 6.7-2.5 7.5-7.5z" fill="url(#cw-star)"/>
    <circle cx="40.5" cy="22.5" r="1.3" fill="#ee0033"/><circle cx="23.5" cy="35" r="1" fill="#ee0033" opacity=".7"/>
    <path d="M48 11.5c.4 2.2 1.1 2.9 3.3 3.3-2.2.4-2.9 1.1-3.3 3.3-.4-2.2-1.1-2.9-3.3-3.3 2.2-.4 2.9-1.1 3.3-3.3z" fill="#fff"/>
  </svg>`;
  const HTML = `<button class="cw-fab" id="cw-fab" type="button" aria-label="Mở hỏi đáp dữ liệu" title="Hỏi đáp dữ liệu"
      aria-expanded="false" aria-controls="cw-panel">${ICON}</button>
    <section class="cw-panel" id="cw-panel" role="dialog" aria-labelledby="cw-title" hidden>
      <header class="cw-head">
        <h2 id="cw-title">Vấn Đạo Đài</h2>
        <a href="chat.html">Xem lịch sử</a>
        <button class="cw-x" id="cw-x" type="button" aria-label="Đóng khung chat">✕</button>
      </header>
      <div class="cw-log" id="cw-log" aria-live="polite">
        <p class="cw-msg bot">Hỏi nhanh số liệu HT1 (SCADA) và HT2 (DMWCS). VD: “Tỷ lệ REJECT HT2 hôm qua?”</p>
      </div>
      <form class="cw-form" id="cw-form">
        <label class="visually-hidden" for="cw-msg">Câu hỏi</label>
        <textarea id="cw-msg" rows="2" maxlength="1000" placeholder="Nhập câu hỏi…" required></textarea>
        <button class="btn primary" id="cw-send" type="submit">Gửi</button>
      </form>
    </section>`;

  function init() {
    if (document.getElementById("cw-fab")) return;
    document.body.insertAdjacentHTML("beforeend", HTML);
    const $ = id => document.getElementById(id);
    const fab = $("cw-fab"), panel = $("cw-panel"), log = $("cw-log"), form = $("cw-form"), input = $("cw-msg"), send = $("cw-send");
    let busy = false;

    const open = on => {
      panel.hidden = !on;
      fab.setAttribute("aria-expanded", on);
      (on ? input : fab).focus();
    };
    const add = (cls, html) => {
      const p = document.createElement("div");
      p.className = "cw-msg " + cls;
      p.innerHTML = html;
      log.append(p);
      log.scrollTop = log.scrollHeight;
      return p;
    };
    const convId = () => { try { return +localStorage.getItem(CONV_KEY) || null; } catch (e) { return null; } };

    async function ask(text) {
      text = text.trim();
      if (!text || busy) return;
      if (!await api.authed) {
        add("bot", "Bạn cần Nhập Môn (nút ở góc trên bên phải) trước khi hỏi.");
        return;
      }
      busy = true;
      send.disabled = true;
      add("user", escHtml(text));
      input.value = "";
      const wait = add("bot busy", "Đang truy vấn…");
      try {
        // hội thoại cũ đã bị xóa theo hạn lưu trữ: bắt đầu hội thoại mới
        const r = await api.chat(text, convId()).catch(e => {
          if (e.status !== 404) throw e;
          try { localStorage.removeItem(CONV_KEY); } catch (x) {}
          return api.chat(text, null);
        });
        try { localStorage.setItem(CONV_KEY, r.conversation_id); } catch (e) {}
        const warns = (r.warnings || []).map(w => `<li>${escHtml(w)}</li>`).join("");
        const choices = (r.lua_chon || []).map(c => `<button class="btn" type="button" data-cw="${escHtml(c)}">${escHtml(c)}</button>`).join("");
        wait.className = "cw-msg bot" + (r.loai === "loi" ? " err" : "");
        wait.innerHTML = escHtml(r.answer || "")
          + (warns ? `<ul class="cw-warn">${warns}</ul>` : "")
          + (choices ? `<div class="cw-choices">${choices}</div>` : "")
          + ((r.rows || []).length ? `<a class="cw-more" href="chat.html">Xem bảng kết quả và SQL</a>` : "");
      } catch (e) {
        wait.className = "cw-msg bot err";
        wait.textContent = e.status === 401 ? "Phiên đăng nhập đã hết, hãy Nhập Môn lại." : "Không gửi được câu hỏi: " + e.message;
      } finally {
        busy = false;
        send.disabled = false;
        log.scrollTop = log.scrollHeight;
      }
    }

    fab.onclick = () => open(panel.hidden);
    $("cw-x").onclick = () => open(false);
    panel.addEventListener("keydown", e => { if (e.key === "Escape") open(false); });
    form.addEventListener("submit", e => { e.preventDefault(); ask(input.value); });
    input.addEventListener("keydown", e => {
      if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(input.value); }
    });
    log.addEventListener("click", e => { const b = e.target.closest("[data-cw]"); if (b) ask(b.dataset.cw); });
  }

  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();
