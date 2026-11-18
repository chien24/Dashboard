// Trang Lịch sử: danh sách report (GET /api/reports) theo HT1/HT2, tìm theo tên file, lọc ngày/trạng thái.
// Mở một dòng thì mới tải chi tiết (GET /api/reports/{id}): giá trị gốc, cảnh báo, ảnh đã upload.
const $ = id => document.getElementById(id);
const DASH = "—";
const has = v => v !== null && v !== undefined && Number.isFinite(v);
const fInt = v => has(v) ? Math.round(v).toLocaleString("vi-VN") : DASH;
const fDec = (v, d = 2) => has(v) ? v.toLocaleString("vi-VN", { minimumFractionDigits: d, maximumFractionDigits: d }) : DASH;
const dmy = s => s ? `${s.slice(8, 10)}/${s.slice(5, 7)}/${s.slice(0, 4)}` : DASH;
const dm = s => s ? `${s.slice(8, 10)}/${s.slice(5, 7)}` : DASH;
const hm = s => s ? s.slice(11, 16) : "";
const STATUS = { ok: "OK", can_kiem_tra: "Cần kiểm tra", da_sua_tay: "Đã sửa tay" };
const PAGE = 50;
const st = { tab: location.hash === "#ht2" ? "ht2" : "ht1", ht1: { items: [], total: 0 }, ht2: { items: [], total: 0 } };

// ---------------------------------------------------------------- tải danh sách
function query(he, offset) {
  const p = new URLSearchParams({ he, limit: PAGE, offset });
  for (const k of ["q", "from", "to", "status"]) { const v = $(k).value.trim(); if (v) p.set(k, v); }
  return api.get("/reports?" + p);
}

let seq = 0;  // gõ nhanh: chỉ áp kết quả của lần tìm mới nhất
async function reload() {
  const my = ++seq;
  if (!await api.authed) {  // chưa đăng nhập: danh sách trống, không gọi API
    $("summary").textContent = "Chưa Nhập môn, không thể tra cứu Tàng Kinh Các.";
    render("ht1"); render("ht2");
    return;
  }
  $("summary").textContent = "Đang tìm…";
  try {
    const [a, b] = await Promise.all([query("ht1", 0), query("ht2", 0)]);
    if (my !== seq) return;
    Object.assign(st.ht1, { items: a.items, total: a.total });
    Object.assign(st.ht2, { items: b.items, total: b.total });
  } catch (e) {
    if (my === seq) $("summary").innerHTML = `<span class="err">Không tải được lịch sử: ${escHtml(e.message)}</span>`;
    return;
  }
  const loc = isFiltered();
  // đang tìm mà tab hiện tại trống còn tab kia có kết quả thì chuyển sang tab kia
  if (loc && !st[st.tab].total && st[other(st.tab)].total) selectTab(other(st.tab));
  $("summary").textContent = loc ? `Tìm thấy ${st.ht1.total + st.ht2.total} báo cáo · HT1: ${st.ht1.total} · HT2: ${st.ht2.total}` : "";
  render("ht1"); render("ht2");
}
const other = he => he === "ht1" ? "ht2" : "ht1";
const isFiltered = () => ["q", "from", "to", "status"].some(k => $(k).value.trim());

async function loadMore(he) {
  const r = await query(he, st[he].items.length);
  st[he].items.push(...r.items);
  st[he].total = r.total;
  render(he);
}

// ---------------------------------------------------------------- vẽ danh sách
function title(r) {
  if (r.loai === "scada") return "SCADA · " + (r.day_chuyen || DASH);
  if (r.loai === "dmwcs_sorted") return "Sorted parcels";
  if (r.loai === "dmwcs_capacity") return `Capacity ${dm(r.thoi_gian_tu)} → ${dm(r.report_date)}`;
  return "Scanner (Hours&BcrRate)";
}
function mark(text) {  // tô phần tên file khớp từ khóa
  const q = $("q").value.trim(), s = String(text ?? "");
  const i = q ? s.toLowerCase().indexOf(q.toLowerCase()) : -1;
  return i < 0 ? escHtml(s) : escHtml(s.slice(0, i)) + `<mark>${escHtml(s.slice(i, i + q.length))}</mark>` + escHtml(s.slice(i + q.length));
}
const warnBadge = n => n ? `<span class="badge" title="${n} cảnh báo">⚠ ${n}</span>` : `<span class="badge ok" title="Không có cảnh báo">✓ 0</span>`;

function render(he) {
  const s = st[he], el = $("list-" + he);
  $("c-" + he).textContent = s.total;
  if (!s.items.length) {
    el.innerHTML = `<p class="empty">${isFiltered() ? "Không có báo cáo nào khớp bộ lọc. Thử bỏ bớt điều kiện hoặc bấm <b>Xóa bộ lọc</b>."
                                                    : `Thiên Cơ trống rỗng. Hãy tiến hành <a href="upload.html">Nạp Linh Ảnh</a> để khai phá.`}</p>`;
    return;
  }
  let html = "", day = null;
  for (const r of s.items) {
    if (r.report_date !== day) { day = r.report_date; html += `<h3 class="day">Ngày ${dmy(day)}</h3>`; }
    html += `<details data-id="${r.id}"><summary>
        <b>${escHtml(title(r))}</b>
        <span class="file" title="Tên file đã upload">${mark(r.file)}</span>
        <span class="status-badge ${r.status}">${STATUS[r.status] || escHtml(r.status)}</span>${warnBadge(r.so_canh_bao)}
        ${r.dang_dung ? "" : `<span class="badge old" title="Ảnh mới hơn cùng ca/ngày đã thay báo cáo này trên dashboard">Đã được thay</span>`}
        <span class="meta">upload ${dmy(r.created_at)} ${hm(r.created_at)}</span>
      </summary><div class="body"><p class="hint">Đang tải…</p></div></details>`;
  }
  const left = s.total - s.items.length;
  if (left > 0) html += `<button class="btn more" type="button" data-more="${he}">Tải thêm (còn ${left})</button>`;
  el.innerHTML = html;
  el.querySelectorAll("details").forEach(d => d.addEventListener("toggle", () => d.open && !d.dataset.loaded && openDetail(d)));
  el.querySelector("[data-more]")?.addEventListener("click", () => loadMore(he));
}

// ---------------------------------------------------------------- chi tiết 1 report
const kv = rows => `<div class="kv">${rows.map(([k, v]) => `<span>${escHtml(k)}</span><span>${v}</span>`).join("")}</div>`;
const tbl = (head, rows) => `<div class="tbl-wrap"><table><thead><tr>${head.map((h, i) => `<th class="${i < 2 ? "l" : ""}">${h}</th>`).join("")}</tr></thead>`
  + `<tbody>${rows.map(r => `<tr>${r.map((c, i) => `<td class="${i < 2 ? "l" : ""}">${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
const span = (a, b) => escHtml(`${a ?? DASH} → ${b ?? DASH}`);
const pct = o => o ? `${fInt(o.so_luong)} (${fDec(o.ty_le)}%)` : DASH;

function body(r) {
  const d = r.data || {};
  let main;
  if (r.loai === "scada") {
    main = kv([["Dây chuyền (giá trị gốc)", escHtml(d.day_chuyen)], ["Thời gian quét", span(d.thoi_gian_tu, d.thoi_gian_den)],
              ["Số lượng đã quét", fInt(d.so_luong_da_quet)], ["Số lượng gói theo lưới", fInt(d.so_luong_goi_theo_luoi)],
              ["Số lượng bưu kiện bất thường", fInt(d.so_buu_kien_bat_thuong)], ["Tỷ lệ bất thường", fDec(d.ty_le_bat_thuong) + "%"],
              ["Thời gian quét trung bình", fDec(d.thoi_gian_quet_trung_binh, 4)], ["Công suất cao nhất 1h", fInt(d.cong_suat_cao_nhat_1h)],
              ["Khung giờ công suất MAX", span(d.cong_suat_max_tu, d.cong_suat_max_den)]])
      + tbl(["Loại bất thường (hiển thị)", "Nhãn OCR gốc", "Số lượng", "Tỷ lệ"],
            (r.bat_thuong || []).map(p => [escHtml(p.loai_vi), escHtml(p.loai), fInt(p.so_luong), fDec(p.ty_le) + "%"]))
      + `<p class="note">Tỷ lệ tính trên số bưu kiện bất thường. Tổng có thể > 100% vì một bưu kiện có thể thuộc nhiều loại.</p>`;
  } else if (r.loai === "dmwcs_sorted") {
    main = kv([["Thời gian", span(d.thoi_gian_tu, d.thoi_gian_den)], ["Total", fInt(d.total)], ["CorrectChute", fInt(d.correct_chute)],
               ["PDA", fInt(d.pda)], ["RejectChute", fInt(d.reject_chute)], ["NoRead", pct(d.no_read)],
               ["NoPostOffice", pct(d.no_post_office)], ["NoChute", pct(d.no_chute)], ["SortFailed", fInt(d.sort_failed)],
               ["Biểu đồ tròn DMWCS", `Correct ${fDec(d.pie_correct_pct, 1)}% · Reject ${fDec(d.pie_reject_pct, 1)}%`]])
      + `<b>Máng NoChute</b><div class="chips" style="margin-top:6px">${String(d.no_chute_danh_sach || "").split("/").filter(Boolean)
          .map(c => `<span>${escHtml(c)}</span>`).join("") || DASH}</div>`
      + `<p class="note">Ô trên màn hình DMWCS bị cắt ở mép phải: danh sách chưa đầy đủ, máng cuối có thể thiếu chữ số.</p>`;
  } else if (r.loai === "dmwcs_capacity") {
    main = kv([["Khoảng ngày truy vấn", span(d.tu_ngay, d.den_ngay)],
               ...(d.cong_suat_theo_ngay || []).map(p => [dmy(p.ngay), fDec(p.cong_suat)])]);
  } else {
    main = kv([["Thời gian", span(d.thoi_gian_tu, d.thoi_gian_den)]])
      + tbl(["Scanner", "", "TOTAL", "SUCCESS", "FAILED", "RATE"],
            (d.bcr || []).map(b => [`Scanner ${b.bcr_no}`, "", fInt(b.total), fInt(b.success), fInt(b.failed), fDec(b.rate) + "%"]));
  }
  const info = kv([["Tên file", escHtml(r.file)], ["Upload lúc", `${dmy(r.created_at)} ${hm(r.created_at)}`],
                   ["Model", escHtml(`${r.provider ?? DASH} / ${r.model ?? DASH}`) + (r.model_lan_2 ? ` · lần 2: ${escHtml(r.model_lan_2)}` : "")],
                   ["Trên dashboard", r.dang_dung ? "Đang dùng" : "Đã được thay bằng ảnh mới hơn"]]);
  const img = r.image_url
    ? `<a href="${escHtml(r.image_url)}" target="_blank" rel="noopener" title="Mở ảnh gốc"><img class="thumb" src="${escHtml(r.image_url)}" loading="lazy" alt="Ảnh đã upload: ${escHtml(r.file)}"></a>`
    : `<div class="no-img">Không có ảnh gốc (import từ JSON)</div>`;
  const warns = (r.canh_bao || []).length ? `<b>Cảnh báo</b><ul class="warns">${r.canh_bao.map(w => `<li>${escHtml(w)}</li>`).join("")}</ul>` : "";
  return `<div class="side">${img}${info}<a class="btn" href="report.html?id=${r.id}">Xem / sửa số liệu</a></div><div>${main}${warns}</div>`;
}

async function openDetail(d) {
  d.dataset.loaded = "1";
  const box = d.querySelector(".body");
  try {
    box.innerHTML = body(await api.report(d.dataset.id));
  } catch (e) {
    delete d.dataset.loaded;
    box.innerHTML = `<p class="err">Không tải được chi tiết: ${escHtml(e.message)}</p>`;
  }
}

// ---------------------------------------------------------------- tab + bộ lọc
function selectTab(he) {
  st.tab = he;
  document.querySelectorAll(".tabs button").forEach(b => b.setAttribute("aria-selected", b.dataset.tab === he));
  $("ht1").hidden = he !== "ht1"; $("ht2").hidden = he !== "ht2";
  history.replaceState(null, "", "#" + he);
}
document.querySelectorAll(".tabs button").forEach(b => b.addEventListener("click", () => selectTab(b.dataset.tab)));
let typing;
$("q").addEventListener("input", () => { clearTimeout(typing); typing = setTimeout(reload, 300); });
["from", "to", "status"].forEach(id => $(id).addEventListener("change", reload));
$("reset").addEventListener("click", () => { ["q", "from", "to", "status"].forEach(k => $(k).value = ""); reload(); });
selectTab(st.tab);
reload();
