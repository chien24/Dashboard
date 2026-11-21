// Trang Thời gian sử dụng: đọc file Excel (.xlsx) ngay trên trình duyệt, cộng cột F dạng "1h33m40s".
// .xlsx là file zip: đọc central directory rồi giải nén bằng DecompressionStream (không cần thư viện).

async function unzip(buf) {
  const v = new DataView(buf), files = {};
  let e = buf.byteLength - 22;
  while (e >= 0 && v.getUint32(e, true) !== 0x06054b50) e--;
  if (e < 0) throw new Error("Không phải file .xlsx hợp lệ");
  let p = v.getUint32(e + 16, true);
  for (let i = v.getUint16(e + 10, true); i > 0; i--) {
    const method = v.getUint16(p + 10, true), size = v.getUint32(p + 20, true);
    const nLen = v.getUint16(p + 28, true), local = v.getUint32(p + 42, true);
    const name = new TextDecoder().decode(new Uint8Array(buf, p + 46, nLen));
    const start = local + 30 + v.getUint16(local + 26, true) + v.getUint16(local + 28, true);
    files[name] = { method, data: new Uint8Array(buf, start, size) };
    p += 46 + nLen + v.getUint16(p + 30, true) + v.getUint16(p + 32, true);
  }
  return async name => {
    const f = files[name];
    if (!f) return null;
    const raw = f.method === 8 ? new Blob([f.data]).stream().pipeThrough(new DecompressionStream("deflate-raw")) : new Blob([f.data]).stream();
    return new DOMParser().parseFromString(await new Response(raw).text(), "application/xml");
  };
}

/** Trả về các dòng [cột A, cột F] của sheet đầu tiên (bỏ dòng tiêu đề). */
async function readRows(buf) {
  const xml = await unzip(buf);
  const sst = await xml("xl/sharedStrings.xml");
  const strings = sst ? [...sst.getElementsByTagName("si")].map(si => si.textContent) : [];
  const sheet = await xml("xl/worksheets/sheet1.xml");
  if (!sheet) throw new Error("Không tìm thấy sheet1 trong file");
  const cell = c => {
    const t = c.getAttribute("t"), val = c.getElementsByTagName("v")[0]?.textContent ?? "";
    return t === "s" ? strings[+val] ?? "" : t === "inlineStr" ? c.textContent : val;
  };
  return [...sheet.getElementsByTagName("row")].slice(1).map(row => {
    const r = {};
    for (const c of row.getElementsByTagName("c")) r[c.getAttribute("r").replace(/\d+/, "")] = cell(c).trim();
    return [r.A || "", r.F || ""];
  });
}

// Giống công thức Excel: thiếu h/m/s thì coi là 0. Trả null nếu không đúng dạng.
function toSec(s) {
  const m = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/i.exec(s.replace(/\s+/g, ""));
  return m && s ? (+m[1] || 0) * 3600 + (+m[2] || 0) * 60 + (+m[3] || 0) : null;
}
const fmtSec = t => `${Math.floor(t / 3600)}h${Math.floor(t % 3600 / 60)}m${t % 60}s`;

console.assert(toSec("1h33m40s") === 5620 && toSec("2m9s") === 129 && toSec("10s") === 10 && toSec("5m") === 300 && toSec("abc") === null && toSec("") === null);
console.assert(fmtSec(5620) === "1h33m40s" && fmtSec(0) === "0h0m0s");

/** Cộng cột F của một file: tổng, theo thiết bị (Map tên → {t, n}), các ô sai dạng. */
function summarize(name, rows) {
  const s = { name, total: 0, n: 0, devs: new Map(), bad: [] };
  rows.forEach(([dev, dur], i) => {
    if (!dur) return;
    const t = toSec(dur);
    if (t === null) return s.bad.push(`dòng ${i + 2}: "${dur}"`);
    const d = s.devs.get(dev) || { t: 0, n: 0 };
    d.t += t; d.n++; s.total += t; s.n++;
    s.devs.set(dev, d);
  });
  return s;
}

// ---------------------------------------------------------------- biểu đồ SVG (style .legend, svg text lấy từ dashboard.css)
const COLORS = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)", "var(--s5)", "var(--s6)", "var(--s7)"];
const fmtShort = t => `${Math.floor(t / 3600)}h${String(Math.floor(t % 3600 / 60)).padStart(2, "0")}m`;
const shortName = n => n.replace(/\.xlsx$/i, "");
function niceMax(v) {
  if (!(v > 0)) return 1;
  const p = 10 ** Math.floor(Math.log10(v)), n = v / p;
  return [1, 1.2, 1.6, 2, 2.4, 3, 4, 5, 6, 8, 10].find(s => s >= n) * p;
}

/** Cột ngang theo thiết bị. rows: [[tên, [giây theo từng file]]]; nhiều file thì xếp chồng mỗi file một màu. */
function hbar(host, rows, names) {
  const W = Math.max(300, host.clientWidth || 640), L = 92, R = 64, bh = 18, gap = 8, pw = W - L - R;
  const max = Math.max(1, ...rows.map(([, v]) => v.reduce((a, b) => a + b, 0)));
  let g = "";
  rows.forEach(([dev, vals], i) => {
    const y = i * (bh + gap), sum = vals.reduce((a, b) => a + b, 0);
    let x = L;
    g += `<text x="${L - 8}" y="${y + 13}" text-anchor="end">${escHtml(dev || "(trống)")}</text>`;
    vals.forEach((v, j) => {
      const w = pw * v / max;
      if (w > 0) g += `<rect x="${x}" y="${y}" width="${Math.max(w - (vals.length > 1 ? 1 : 0), 1)}" height="${bh}" rx="3" fill="${COLORS[j]}"><title>${escHtml(dev)} · ${escHtml(shortName(names[j]))}: ${fmtSec(v)}</title></rect>`;
      x += w;
    });
    g += `<text x="${x + 6}" y="${y + 13}" style="fill:var(--ink-2);font-weight:600">${fmtShort(sum)}</text>`;
  });
  const legend = names.length > 1 ? `<div class="legend">${names.map((n, j) => `<span><i style="background:${COLORS[j]}"></i>${escHtml(shortName(n))}</span>`).join("")}</div>` : "";
  const H = rows.length * (bh + gap);
  host.innerHTML = legend + `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Thời gian sử dụng theo thiết bị">${g}</svg>`;
}

/** Cột đứng: tổng giờ của từng file. */
function vbar(host, files) {
  const W = Math.max(300, host.clientWidth || 640), H = 240, L = 48, R = 12, T = 22, B = 30, pw = W - L - R, ph = H - T - B;
  const ymax = niceMax(Math.max(...files.map(f => f.total)) / 3600 * 1.08), y = h => T + ph - h / ymax * ph, band = pw / files.length;
  let g = "";
  for (let k = 0; k <= 4; k++) {
    const v = ymax * k / 4;
    g += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="${k ? "var(--grid)" : "var(--axis)"}"/><text x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${+v.toFixed(1)}h</text>`;
  }
  files.forEach((f, i) => {
    const cx = L + band * (i + .5), w = Math.min(56, band * .6), h = f.total / 3600;
    g += `<rect x="${cx - w / 2}" y="${y(h)}" width="${w}" height="${y(0) - y(h)}" rx="4" fill="${COLORS[i]}"><title>${escHtml(f.name)}: ${fmtSec(f.total)}</title></rect>`
       + `<text x="${cx}" y="${y(h) - 6}" text-anchor="middle" style="fill:var(--ink-2);font-weight:600">${fmtShort(f.total)}</text>`
       + `<text x="${cx}" y="${H - 10}" text-anchor="middle">${escHtml(shortName(f.name))}</text>`;
  });
  host.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Tổng thời gian theo file">${g}</svg>`;
}

// ---------------------------------------------------------------- trang
const out = document.getElementById("tg-out");
let last = [];  // chỉ giữ trong bộ nhớ: reload trang là mất
const byName = (a, b) => a.localeCompare(b, "vi", { numeric: true });

function drawCharts() {
  if (!last.length) return;
  // shortcut: quá 7 file thì hết màu riêng, gộp thành 1 màu; cần phân biệt hơn thì thêm màu vào COLORS.
  const many = last.length > COLORS.length;
  const names = many ? ["Tất cả file"] : last.map(f => f.name);
  const devs = [...new Set(last.flatMap(f => [...f.devs.keys()]))].sort(byName);
  const rows = devs.map(d => [d, many ? [last.reduce((a, f) => a + (f.devs.get(d)?.t || 0), 0)] : last.map(f => f.devs.get(d)?.t || 0)]);
  hbar(document.getElementById("ch-dev"), rows, names);
  const chFile = document.getElementById("ch-file");
  if (chFile) vbar(chFile, last);
}

function render(files, errors) {
  const total = files.reduce((a, f) => a + f.total, 0), n = files.reduce((a, f) => a + f.n, 0);
  const devCount = new Set(files.flatMap(f => [...f.devs.keys()])).size;
  const tile = (k, v, d) => `<div class="tile"><div class="k">${k}</div><div class="v">${v}</div><div class="d">${d}</div></div>`;
  const cards = files.map(f => `<section class="card tg-file">
    <div class="card-head"><h2>${escHtml(f.name)}</h2><span class="tg-total">Tổng: <b>${fmtSec(f.total)}</b> · ${f.n} dòng</span></div>
    ${f.bad.length ? `<div class="warn-box">Bỏ qua ${f.bad.length} ô không đúng dạng thời gian:<ul>${f.bad.map(b => `<li>${escHtml(b)}</li>`).join("")}</ul></div>` : ""}
    <details${files.length === 1 ? " open" : ""}><summary>Chi tiết theo thiết bị</summary>
    <table><thead><tr><th>Thiết bị (cột A)</th><th>Số lần</th><th>Thời gian</th></tr></thead>
    <tbody>${[...f.devs].sort((a, b) => byName(a[0], b[0])).map(([dev, d]) => `<tr><td>${escHtml(dev || "(trống)")}</td><td>${d.n}</td><td>${fmtSec(d.t)}</td></tr>`).join("")}</tbody></table></details>
  </section>`).join("");
  out.innerHTML = errors + (files.length ? `
    <div class="kpis">
      ${tile("Tổng thời gian sử dụng", fmtSec(total), files.length > 1 ? `Cộng ${files.length} file` : escHtml(files[0].name))}
      ${tile("Số lần chạy", n.toLocaleString("vi-VN"), "Số ô cột F đã cộng")}
      ${tile("Số thiết bị", devCount, "Khác nhau ở cột A")}
      ${tile("Trung bình mỗi thiết bị", fmtSec(Math.round(total / Math.max(devCount, 1))), files.length > 1 ? "Cộng mọi file" : "")}
    </div>
    <div class="grid2">
      <section class="card"><div class="card-head"><h2>Thời gian theo thiết bị</h2></div><div id="ch-dev"></div></section>
      ${files.length > 1 ? `<section class="card"><div class="card-head"><h2>Tổng thời gian theo file</h2></div><div id="ch-file"></div></section>` : ""}
    </div>` + cards : "");
  drawCharts();
}

async function handle(list) {
  if (!list.length) return;
  out.innerHTML = `<p class="hint">Đang đọc ${list.length} file…</p>`;
  const files = [];
  let errors = "";
  for (const f of [...list].sort((a, b) => byName(a.name, b.name))) {
    try { files.push(summarize(f.name, await readRows(await f.arrayBuffer()))); }
    catch (e) { errors += `<div class="err-box">${escHtml(f.name)}: ${escHtml(e.message)}</div>`; }
  }
  last = files;
  render(files, errors);
}

const pick = document.getElementById("pick"), drop = document.getElementById("drop");
pick.addEventListener("change", () => { handle([...pick.files]); pick.value = ""; });
drop.addEventListener("dragover", e => { e.preventDefault(); drop.classList.add("over"); });
drop.addEventListener("dragleave", () => drop.classList.remove("over"));
drop.addEventListener("drop", e => { e.preventDefault(); drop.classList.remove("over"); handle([...e.dataTransfer.files].filter(f => /\.xlsx$/i.test(f.name))); });
let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(drawCharts, 150); });
