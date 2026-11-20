// Dashboard HT1/HT2: logic giữ nguyên từ HTML mẫu, dữ liệu lấy từ API (js/api.js).
(async () => {
const RAW = await api.dashboardData();

// ---------------------------------------------------------------- tiện ích
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const has = v => v !== null && v !== undefined && Number.isFinite(v);
const DASH = "—";
const fInt = v => has(v) ? Math.round(v).toLocaleString("vi-VN") : DASH;
const fDec = (v, d = 2) => has(v) ? v.toLocaleString("vi-VN", { minimumFractionDigits: d, maximumFractionDigits: d }) : DASH;
const fPct = v => has(v) ? fDec(v * 100) + "%" : DASH;
const fH = v => has(v) ? fDec(v) + " h" : DASH;
const fAxis = v => v.toLocaleString("vi-VN", { maximumFractionDigits: 1 }); // nhãn trục: 7,5 thay vì làm tròn thành 8
const dm = d => d.slice(8, 10) + "/" + d.slice(5, 7);
const dayOf = s => s.slice(0, 10);
function daysBetween(a, b) {
  const out = [];
  for (let t = Date.parse(a + "T00:00:00Z"); t <= Date.parse(b + "T00:00:00Z"); t += 864e5) out.push(new Date(t).toISOString().slice(0, 10));
  return out;
}
const addDays = (d, n) => new Date(Date.parse(d + "T00:00:00Z") + n * 864e5).toISOString().slice(0, 10);
const sum = (arr, f) => arr.length ? arr.reduce((s, x) => s + f(x), 0) : null;

// Chuẩn hoá chịu lỗi font: bỏ dấu, chữ thường, bỏ '?'
const norm = s => s.replace(/đ/g, "d").replace(/Đ/g, "D").normalize("NFD").replace(/[̀-ͯ]/g, "")
  .toLowerCase().replace(/\?/g, "").replace(/\s+/g, " ").trim();
// Loại bất thường đã được backend chuẩn hóa (abnormal_types.json). REJECT HT1 = Không Có Mã Vạch + Yêu cầu ống dẫn thất bại (Q1)
const DUNG = { NO_BARCODE: "REJECT", CHUTE_REQUEST_FAILED: "REJECT", UNKNOWN: "không nhận ra – bổ sung abnormal_types.json" };
// Tên dây chuyền: hiển thị đúng tên OCR đọc được (Q5); khóa bỏ hoa/thường, khoảng trắng để 'CBs2' và 'CBS2' là 1 dây chuyền.
// Thứ tự cố định = màu cố định.
const LINE_ORDER = ["outbound", "inbound", "cbs21stlayer", "cbs12stlayer"];
const LINE_COLOR = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)"];
const lineOf = raw => ({ key: norm(raw).replace(/ /g, ""), ten: raw.trim() });

// ---------------------------------------------------------------- dữ liệu
const H1 = RAW.scada.map(r => {
  const pb = r.phan_bo_bat_thuong.map(x => ({ ...x, key: x.loai_key, ten: x.loai_vi, dung: DUNG[x.loai_key] || "tham khảo" }));
  const pick = k => pb.filter(x => x.key === k).reduce((s, x) => s + x.so_luong, 0); // loại vắng mặt trên biểu đồ tròn = 0 (Q8)
  const all = r.so_luong_da_quet, noread = pick("NO_BARCODE"), ongdan = pick("CHUTE_REQUEST_FAILED"), reject = noread + ongdan;
  const line = lineOf(r.day_chuyen);
  return { r, pb, day: dayOf(r.thoi_gian_tu), line, all, noread, ongdan, reject, correct: all - reject,
           rate: all ? reject / all : null, max: r.cong_suat_cao_nhat_1h, hours: r.cong_suat_cao_nhat_1h ? all / r.cong_suat_cao_nhat_1h : null };
});
const LINES = [...new Map(H1.map(x => [x.line.key, x.line])).values()]
  .sort((a, b) => (LINE_ORDER.indexOf(a.key) + 99) % 99 - (LINE_ORDER.indexOf(b.key) + 99) % 99 || a.ten.localeCompare(b.ten));
const lineColor = k => LINE_COLOR[LINE_ORDER.indexOf(k)] || "var(--muted)";

// Công suất AVG: backend đã giữ đúng 1 giá trị mỗi ngày (ảnh có khoảng truy vấn mới nhất, khác giá trị thì cảnh báo ở report)
const CAP = new Map(RAW.capacity.map(c => [c.ngay, { avg: c.cong_suat, rec: c }]));
const SORTED = new Map(RAW.sorted.map(r => [dayOf(r.thoi_gian_tu), r]));
const BCR = new Map(RAW.bcr.map(r => [dayOf(r.thoi_gian_tu), r])); // ngày -> báo cáo Hours&BcrRate

// Biểu đồ cột Scanner của 1 ngày: trục Y cố định 0–100%, mỗi BCR_NO một màu cố định.
// shortcut: chỉ 6 màu đạt kiểm tra mù màu theo thứ tự này; BCR 7 trở lên dùng màu xám, cần thêm thì chọn lại bảng màu.
const BCR_COLOR = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)", "var(--s7)", "var(--s6)"];
const fRate = v => v.toLocaleString("vi-VN", { maximumFractionDigits: 2 });
function bcrChart(host, rec) {
  const rows = rec.bcr, warns = n => rec.canh_bao.filter(s => s.startsWith(`BCR ${n}:`));
  const W = Math.max(300, host.clientWidth || 640), H = 240, L = 44, R = 12, T = 24, B = 30, pw = W - L - R, ph = H - T - B;
  const y = v => T + ph - Math.min(Math.max(v, 0), 100) / 100 * ph, band = pw / rows.length, w = Math.min(56, band * .55);
  let g = "";
  for (let k = 0; k <= 4; k++) g += `<line x1="${L}" x2="${W - R}" y1="${y(k * 25)}" y2="${y(k * 25)}" stroke="${k ? "var(--grid)" : "var(--axis)"}"/>`
    + `<text x="${L - 6}" y="${y(k * 25) + 4}" text-anchor="end">${k * 25}%</text>`;
  rows.forEach((r, i) => {
    const cx = L + band * (i + .5), c = BCR_COLOR[r.bcr_no - 1] || "var(--muted)", warn = warns(r.bcr_no).length ? "⚠ " : "";
    g += `<path d="${topRounded(cx - w / 2, y(r.rate), w, y(0) - y(r.rate), 4)}" fill="${c}"/>`
       + `<text x="${cx}" y="${y(r.rate) - 6}" text-anchor="middle" style="fill:var(--ink-2);font-weight:600">${warn}${fRate(r.rate)}</text>`
       + `<text x="${cx}" y="${H - 10}" text-anchor="middle">Scanner ${r.bcr_no}</text>`
       + `<rect class="hit" data-i="${i}" x="${L + band * i}" y="${T}" width="${band}" height="${ph}" fill="transparent"/>`;
  });
  host.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img">${g}</svg>`
    + `<p class="note">Thông tin tham khảo · báo cáo ${esc(rec.thoi_gian_tu + " → " + rec.thoi_gian_den)}</p>`
    + `<div class="tbl-wrap"><table><thead><tr><th class="l">BCR_NO</th><th>TOTAL</th><th>SUCCESS</th><th>FAILED</th><th>RATE</th></tr></thead><tbody>`
    + rows.map(r => `<tr><td class="l">${r.bcr_no}${warns(r.bcr_no).length ? ` <span class="badge" title="${esc(warns(r.bcr_no).join("\n"))}">⚠</span>` : ""}</td>`
      + `<td>${fInt(r.total)}</td><td>${fInt(r.success)}</td><td>${fInt(r.failed)}</td><td>${fDec(r.rate)}%</td></tr>`).join("")
    + `</tbody></table></div>`;
  host.querySelectorAll(".hit").forEach(el => {
    const r = rows[+el.dataset.i], c = BCR_COLOR[r.bcr_no - 1] || "var(--muted)";
    el.addEventListener("mousemove", e => showTip(e, `Scanner ${r.bcr_no}`, [[c, "RATE", fDec(r.rate) + "%"],
      ["transparent", "TOTAL", fInt(r.total)], ["transparent", "SUCCESS", fInt(r.success)], ["transparent", "FAILED", fInt(r.failed)],
      ...warns(r.bcr_no).map(s => ["transparent", "⚠", s.replace(/^BCR \d+: /, "")])]));
    el.addEventListener("mouseleave", hideTip);
  });
}
function h2Day(d) {
  const s = SORTED.get(d), avg = CAP.get(d)?.avg ?? null;
  return { day: d, s, avg, all: s?.total ?? null, correct: s ? s.correct_chute + s.pda : null, pda: s?.pda ?? null, reject: s?.reject_chute ?? null,
           rate: s && s.total ? s.reject_chute / s.total : null, hours: s && has(avg) ? s.total / avg : null };
}

// ---------------------------------------------------------------- biểu đồ SVG
const tip = $("tip");
function showTip(e, title, rows) {
  tip.innerHTML = `<b>${esc(title)}</b>` + rows.map(([c, n, v]) => `<div><span><i style="background:${c}"></i>${esc(n)}</span><span>${esc(v)}</span></div>`).join("");
  tip.style.display = "block";
  const x = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8), y = Math.min(e.clientY + 14, innerHeight - tip.offsetHeight - 8);
  tip.style.left = x + "px"; tip.style.top = y + "px";
}
const hideTip = () => tip.style.display = "none";
function niceMax(v) {
  if (!(v > 0)) return 1;
  const p = 10 ** Math.floor(Math.log10(v)), n = v / p;
  return [1, 1.2, 1.6, 2, 2.4, 3, 4, 5, 6, 8, 10].find(s => s >= n) * p; // chia hết cho 4 vạch lưới
}
function topRounded(x, y, w, h, r) {
  r = Math.min(r, w / 2, h);
  return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
}
/** type: "stack" | "group" | "line". series: [{name, color, values[]}] theo từng ngày; null = không có dữ liệu.
 *  label: hàm định dạng nhãn giá trị in trên đầu cột (chỉ cho "group"); bỏ trống = không in nhãn. */
function chart(host, { days, series, type, fmt, selected, onPick, label }) {
  // vẽ đúng bề rộng khung để chữ luôn 11px, không bị phóng to theo khung
  const W = Math.max(300, host.clientWidth || 640), H = 230, L = 52, R = 12, T = 12, B = 30, pw = W - L - R, ph = H - T - B;
  const totals = days.map((_, i) => type === "stack" ? (series.some(s => has(s.values[i])) ? series.reduce((a, s) => a + (s.values[i] || 0), 0) : null) : null);
  const peak = Math.max(0, ...(type === "stack" ? totals.filter(has) : series.flatMap(s => s.values.filter(has))));
  const ymax = niceMax(peak * 1.08), y = v => T + ph - v / ymax * ph, band = pw / days.length;
  let g = "";
  for (let k = 0; k <= 4; k++) {
    const v = ymax * k / 4;
    g += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="${k ? "var(--grid)" : "var(--axis)"}" stroke-width="1"/>`
       + `<text x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${esc(fmt(v, true))}</text>`;
  }
  const step = Math.ceil(days.length / 10);
  days.forEach((d, i) => {
    const cx = L + band * (i + .5);
    if (d === selected) g += `<rect x="${L + band * i}" y="${T}" width="${band}" height="${ph}" fill="var(--wash)"/>`;
    if (i % step === 0) g += `<text x="${cx}" y="${H - 10}" text-anchor="middle">${dm(d)}</text>`;
    const any = series.some(s => has(s.values[i]));
    if (!any) { g += `<text x="${cx}" y="${y(0) - 6}" text-anchor="middle">${DASH}</text>`; return; }
    if (type === "stack") {
      const w = Math.min(40, band * .6); let base = 0;
      const drawn = series.filter(s => has(s.values[i]) && s.values[i] > 0);
      drawn.forEach((s, j) => {
        const v = s.values[i], top = y(base + v), h = y(base) - top - (j ? 2 : 0); // 2px khe giữa các đoạn
        g += j === drawn.length - 1 ? `<path d="${topRounded(cx - w / 2, top, w, Math.max(h, 0), 4)}" fill="${s.color}"/>`
                                    : `<rect x="${cx - w / 2}" y="${top}" width="${w}" height="${Math.max(h, 0)}" fill="${s.color}"/>`;
        base += v;
      });
    } else if (type === "group") {
      const n = series.length, w = Math.min(18, band * .8 / n), x0 = cx - (w * n + 2 * (n - 1)) / 2;
      series.forEach((s, j) => {
        const v = s.values[i]; if (!has(v)) return;
        g += `<path d="${topRounded(x0 + j * (w + 2), y(v), w, y(0) - y(v), 4)}" fill="${s.color}"/>`;
        if (label) g += `<text x="${x0 + j * (w + 2) + w / 2}" y="${y(v) - 6}" text-anchor="middle" style="fill:var(--ink-2);font-weight:600">${esc(label(v))}</text>`;
      });
    }
  });
  if (type === "line") for (const s of series) {
    let seg = [];
    const flush = () => { if (seg.length > 1) g += `<polyline points="${seg.join(" ")}" fill="none" stroke="${s.color}" stroke-width="2" stroke-linejoin="round"/>`; seg = []; };
    days.forEach((d, i) => { const v = s.values[i]; if (has(v)) seg.push(`${L + band * (i + .5)},${y(v)}`); else flush(); });
    flush();
    days.forEach((d, i) => { const v = s.values[i]; if (has(v)) g += `<circle cx="${L + band * (i + .5)}" cy="${y(v)}" r="4" fill="${s.color}" stroke="var(--surface)" stroke-width="2"/>`; });
  }
  days.forEach((d, i) => g += `<rect class="hit" data-i="${i}" x="${L + band * i}" y="${T}" width="${band}" height="${ph}" fill="transparent" style="cursor:pointer"/>`);
  const legend = series.length > 1 ? `<div class="legend">${series.map(s => `<span><i style="background:${s.color}"></i>${esc(s.name)}</span>`).join("")}</div>` : "";
  host.innerHTML = legend + `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img">${g}</svg>`;
  host.querySelectorAll(".hit").forEach(el => {
    const i = +el.dataset.i;
    el.addEventListener("mousemove", e => {
      const rows = series.map(s => [s.color, s.name, has(s.values[i]) ? fmt(s.values[i]) : DASH]);
      if (type === "stack" && series.length > 1) rows.push(["transparent", "Tổng", has(totals[i]) ? fmt(totals[i]) : DASH]);
      showTip(e, "Ngày " + dm(days[i]), rows);
    });
    el.addEventListener("mouseleave", hideTip);
    if (onPick) el.addEventListener("click", () => onPick(days[i]));
  });
}

// ---------------------------------------------------------------- khối dùng chung
const withPct = (v, p) => fInt(v) + (has(v) && has(p) ? ` <span class="pct">(${fPct(p)})</span>` : "");
const tile = (k, v, d = "") => `<div class="tile"><div class="k">${esc(k)}</div><div class="v">${v}</div>${d ? `<div class="d">${d}</div>` : ""}</div>`;
function warnBadge(list) {
  if (!list.length) return `<span class="badge ok" title="Không có cảnh báo">✓ 0</span>`;
  return `<span class="badge" title="${esc(list.join("\n"))}">⚠ ${list.length}</span>`;
}
const warnList = r => r.canh_bao || [];
function table(el, head, rows) {
  el.innerHTML = `<thead><tr>${head.map((h, i) => `<th class="${i < 2 ? "l" : ""}">${esc(h)}</th>`).join("")}</tr></thead>`
    + `<tbody>${rows.map(r => `<tr>${r.map((c, i) => `<td class="${i < 2 ? "l" : ""}">${c}</td>`).join("")}</tr>`).join("")}</tbody>`;
}
document.querySelectorAll("[data-csv]").forEach(b => b.addEventListener("click", () => {
  const t = $(b.dataset.csv);
  const csv = [...t.rows].map(tr => [...tr.cells].map(td => `"${td.innerText.replace(/"/g, '""')}"`).join(",")).join("\r\n");
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(new Blob(["﻿" + csv], { type: "text/csv" })), download: b.dataset.csv + ".csv" });
  a.click(); URL.revokeObjectURL(a.href);
}));
document.querySelectorAll(".tabs button").forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll(".tabs button").forEach(x => x.setAttribute("aria-selected", x === b));
  $("ht1").hidden = b.dataset.tab !== "ht1"; $("ht2").hidden = b.dataset.tab !== "ht2";
  renderH1(); renderH2(); // tab vừa hiện mới đo được bề rộng
}));
function initRange(prefix, allDays, render) {
  // Mặc định: lùi về ngày có dữ liệu cũ nhất để không cắt mất báo cáo cũ hơn (vd capacity 05–10/11 khi Scanner là 15/11),
  // ít nhất 7 ngày, nhiều nhất 35 ngày (dữ liệu chỉ giữ 35 ngày)
  const sorted = allDays.length ? allDays.sort() : [new Date().toISOString().slice(0, 10)], last = sorted.at(-1), first = sorted[0];
  const from = [first, addDays(last, -6)].sort()[0];
  $(prefix + "-to").value = last; $(prefix + "-from").value = from < addDays(last, -34) ? addDays(last, -34) : from;
  [prefix + "-from", prefix + "-to"].forEach(id => $(id).addEventListener("change", () => { st[prefix].kpi = null; render(); }));
}
const st = { h1: { kpi: null }, h2: { kpi: null } };
function rangeDays(prefix) {
  let a = $(prefix + "-from").value, b = $(prefix + "-to").value;
  if (!a || !b) return [];
  if (a > b) [a, b] = [b, a];
  return daysBetween(a, b).slice(-35);
}

// ---------------------------------------------------------------- HT1
$("h1-line").innerHTML = `<option value="all">Tất cả</option>` + LINES.map(l => `<option value="${esc(l.key)}">${esc(l.ten)}</option>`).join("");
function renderH1() {
  const days = rangeDays("h1"), sel = $("h1-line").value;
  const inSel = x => sel === "all" || x.line.key === sel;
  const recs = H1.filter(x => days.includes(x.day) && inSel(x));
  const kpiDay = st.h1.kpi && days.includes(st.h1.kpi) ? st.h1.kpi : (recs.map(x => x.day).sort().at(-1) || days.at(-1));
  const today = recs.filter(x => x.day === kpiDay);
  $("h1-day").textContent = `Chỉ số ngày ${kpiDay ? dm(kpiDay) + "/" + kpiDay.slice(0, 4) : DASH} · ${sel === "all" ? "Tất cả dây chuyền" : LINES.find(l => l.key === sel).ten}`;
  const S = f => sum(today, f);
  const perLine = (f, fmt) => `<ul>${today.map(x => `<li><span>${esc(x.line.ten)}</span><b>${fmt(f(x))}</b></li>`).join("")}</ul>`;
  const one = today.length === 1 ? today[0] : null;
  const rate = today.length && S(x => x.all) ? S(x => x.reject) / S(x => x.all) : null;
  $("h1-kpis").innerHTML =
      tile("ALL", fInt(S(x => x.all)), "Số lượng đã quét")
    + tile("CORRECT", withPct(S(x => x.correct), has(rate) ? 1 - rate : null), "ALL − REJECT · tỷ lệ = 100% − tỷ lệ REJECT")
    + tile("REJECT", withPct(S(x => x.reject), rate), `Không có mã vạch ${fInt(S(x => x.noread))} · Yêu cầu ống dẫn thất bại ${fInt(S(x => x.ongdan))}`)
    + (one || !today.length ? tile("Công suất MAX", fInt(one?.max), one ? `${one.r.cong_suat_max_tu.slice(11, 16)}–${one.r.cong_suat_max_den.slice(11, 16)}` : "")
                            : tile("Công suất MAX", fInt(S(x => x.max)), `Tổng MAX của ${today.length} dây chuyền (mỗi dây chuyền đạt MAX ở khung giờ khác nhau)` + perLine(x => x.max, fInt)))
    + (one || !today.length ? tile("Thời gian sử dụng", fH(one?.hours), "ALL / MAX, ước tính")
                            : tile("Thời gian sử dụng", fH(S(x => x.hours)), `Tổng giờ chạy của ${today.length} dây chuyền` + perLine(x => x.hours, fH)));

  const byDay = f => days.map(d => { const a = recs.filter(x => x.day === d); return a.length ? sum(a, f) : null; });
  const onPick = d => { st.h1.kpi = d; renderH1(); };
  chart($("h1-c1"), { days, type: "stack", fmt: fInt, selected: kpiDay, onPick, series: [
    { name: "CORRECT", color: "var(--s1)", values: byDay(x => x.correct) },
    { name: "REJECT", color: "var(--s2)", values: byDay(x => x.reject) }] });
  chart($("h1-c2"), { days, type: "stack", fmt: fInt, selected: kpiDay, onPick, series: [
    { name: "Không có mã vạch", color: "var(--s7)", values: byDay(x => x.noread) },
    { name: "Yêu cầu ống dẫn thất bại", color: "var(--s5)", values: byDay(x => x.ongdan) }] });
  const m = $("h1-metric").value;
  const mfmt = { all: fInt, reject: fInt, rate: (v, axis) => axis ? fDec(v * 100, 1) + "%" : fPct(v), max: fInt, hours: (v, axis) => axis ? fAxis(v) : fH(v) }[m];
  chart($("h1-c3"), { days, type: "group", fmt: mfmt, selected: kpiDay, onPick, series: LINES.map(l => ({
    name: l.ten, color: lineColor(l.key),
    values: days.map(d => H1.find(x => x.day === d && x.line.key === l.key)?.[m] ?? null) })) });

  const rows = [];
  for (const d of [...days].reverse()) for (const l of LINES) {
    const x = recs.find(x => x.day === d && x.line.key === l.key);
    if (x) rows.push([dm(d), esc(l.ten), fInt(x.all), fInt(x.correct), fInt(x.reject), fInt(x.noread), fInt(x.ongdan), fPct(x.rate),
      fInt(x.max), `${x.r.cong_suat_max_tu.slice(11, 16)}–${x.r.cong_suat_max_den.slice(11, 16)}`, fH(x.hours), warnBadge(warnList(x.r))]);
  }
  if (!rows.length) rows.push([DASH, "Không có dữ liệu trong khoảng ngày đã chọn", ...Array(10).fill("")]);
  table($("h1-table"), ["Ngày", "Dây chuyền", "ALL", "CORRECT", "REJECT", "Không có mã vạch", "Yêu cầu ống dẫn thất bại", "Tỷ lệ REJECT", "Công suất MAX", "Khung giờ MAX", "Thời gian sử dụng", "Cảnh báo"], rows);

}
initRange("h1", H1.map(x => x.day), renderH1);
["h1-line", "h1-metric"].forEach(id => $(id).addEventListener("change", renderH1));
renderH1();

// ---------------------------------------------------------------- HT2
function renderH2() {
  const days = rangeDays("h2"), D = days.map(h2Day);
  // Mặc định: ngày gần nhất có báo cáo Sorted (có ALL/CORRECT/REJECT); không có thì ngày gần nhất có dữ liệu bất kỳ
  const latest = D.filter(x => x.s).at(-1)?.day || D.filter(x => has(x.avg)).at(-1)?.day || days.at(-1);
  const kpiDay = st.h2.kpi && days.includes(st.h2.kpi) ? st.h2.kpi : latest;
  const k = h2Day(kpiDay || "");
  $("h2-day").textContent = `Chỉ số ngày ${kpiDay ? dm(kpiDay) + "/" + kpiDay.slice(0, 4) : DASH} · máy CBS`;
  $("h2-kpis").innerHTML =
      tile("ALL", fInt(k.all), "Total")
    + tile("CORRECT", withPct(k.correct, has(k.rate) ? 1 - k.rate : null),
           k.s ? `CorrectChute ${fInt(k.s.correct_chute)} + PDA ${fInt(k.pda)}` : "CorrectChute + PDA")
    + tile("REJECT", withPct(k.reject, k.rate), "RejectChute")
    + tile("Công suất AVG", has(k.avg) ? fDec(k.avg) : DASH, "bưu kiện/giờ · báo cáo Capacity")
    + tile("Thời gian sử dụng", fH(k.hours), "ALL / AVG");
  const onPick = d => { st.h2.kpi = d; renderH2(); };
  const v = f => D.map(f);
  chart($("h2-c1"), { days, type: "stack", fmt: fInt, selected: kpiDay, onPick, series: [
    { name: "CORRECT – CorrectChute", color: "var(--s1)", values: v(x => x.s?.correct_chute ?? null) },
    { name: "CORRECT – PDA", color: "var(--s3)", values: v(x => x.pda) },
    { name: "REJECT", color: "var(--s2)", values: v(x => x.reject) }] });
  chart($("h2-c2"), { days, type: "stack", fmt: fInt, selected: kpiDay, onPick, series: [
    { name: "NoRead", color: "var(--s7)", values: v(x => x.s?.no_read.so_luong ?? null) },
    { name: "NoPostOffice", color: "var(--s5)", values: v(x => x.s?.no_post_office.so_luong ?? null) },
    { name: "NoChute", color: "var(--s4)", values: v(x => x.s?.no_chute.so_luong ?? null) }] });
  chart($("h2-c3"), { days, type: "line", fmt: (n, axis) => axis ? fInt(n) : fDec(n), selected: kpiDay, onPick,
    series: [{ name: "Công suất AVG", color: "var(--s1)", values: v(x => x.avg) }] });
  // Scanner: theo ngày đang chọn như các biểu đồ khác; ngày đó không có dữ liệu BCR thì lấy ngày mới nhất trong khoảng lọc có BCR
  const bcrDay = BCR.has(kpiDay) ? kpiDay : [...days].reverse().find(d => BCR.has(d));
  const fullDate = d => d ? `${dm(d)}/${d.slice(0, 4)}` : DASH;
  if (bcrDay) {
    $("h2-bcr-title").textContent = `Tỷ lệ đọc thành công của từng Scanner ngày ${fullDate(bcrDay)}`;
    bcrChart($("h2-c4"), BCR.get(bcrDay));
    if (bcrDay !== kpiDay)
      $("h2-c4").insertAdjacentHTML("afterbegin", `<p class="note">Ngày ${fullDate(kpiDay)} chưa có dữ liệu Scanner, đang hiện ngày gần nhất có dữ liệu.</p>`);
  } else {
    $("h2-bcr-title").textContent = "Tỷ lệ đọc thành công của từng Scanner";
    $("h2-c4").innerHTML = `<p class="hint">Chưa có dữ liệu Scanner ngày ${fullDate(days.at(-1))}</p>`;
  }
  chart($("h2-c5"), { days, type: "group", fmt: (n, axis) => axis ? fAxis(n) : fH(n), selected: kpiDay, onPick, label: fRate,
    series: [{ name: "Thời gian sử dụng", color: "var(--s1)", values: v(x => x.hours) }] });

  const rows = [...D].reverse().filter(x => x.s || has(x.avg)).map(x => {
    const cap = CAP.get(x.day);
    const w = [...(x.s ? warnList(x.s) : []), ...(cap?.rec.canh_bao || []), ...(cap?.warn ? [cap.warn] : [])];
    return [dm(x.day), x.s ? "Sorted + Capacity" : "Chỉ Capacity", fInt(x.all), fInt(x.correct), fInt(x.pda), fInt(x.reject),
      has(x.rate) ? fPct(1 - x.rate) : DASH, fPct(x.rate), has(x.avg) ? fDec(x.avg) : DASH, fH(x.hours), warnBadge(w)];
  });
  if (!rows.length) rows.push([DASH, "Không có dữ liệu trong khoảng ngày đã chọn", ...Array(9).fill("")]);
  table($("h2-table"), ["Ngày", "Nguồn", "ALL", "CORRECT", "trong đó PDA", "REJECT", "Tỷ lệ CORRECT", "Tỷ lệ REJECT", "Công suất AVG (bưu kiện/giờ)", "Thời gian sử dụng", "Cảnh báo"], rows);
}
initRange("h2", [...SORTED.keys(), ...CAP.keys(), ...BCR.keys()], renderH2);
renderH2();
if (location.hash === "#ht2") document.querySelector('[data-tab="ht2"]').click(); // mở thẳng tab HT2
let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => { renderH1(); renderH2(); }, 150); });
})().catch(e => {
  document.querySelector("main").prepend(Object.assign(document.createElement("p"), { className: "err", textContent: "Không tải được dữ liệu: " + e.message }));
});
