"""Kiểm tra số học (mục 5 đặc tả). Chỉ trả danh sách cảnh báo, KHÔNG sửa số.

Cảnh báo dòng BCR bắt đầu bằng 'BCR <số>:' để dashboard gắn ⚠ đúng cột.
"""
from datetime import date, datetime, timedelta

TOL = 0.1  # sai số cho phép với phần trăm
LY_DO_REJECT = ("no_read", "no_post_office", "no_chute")


def _iso(s, cls=datetime):
    try:
        return cls.fromisoformat(str(s).strip())
    except ValueError:
        return None


def _thoi_gian(d: dict, nhan: str) -> list[str]:
    tu, den = _iso(d["thoi_gian_tu"]), _iso(d["thoi_gian_den"])
    if not (tu and den):
        return [f"{nhan} sai định dạng: '{d['thoi_gian_tu']}' - '{d['thoi_gian_den']}'"]
    if tu >= den:
        return [f"{nhan}: mốc đầu {d['thoi_gian_tu']} không nhỏ hơn mốc cuối {d['thoi_gian_den']}"]
    return []


def validate_scada(d: dict) -> list[str]:
    errs = []
    goi, bt, tl = d["so_luong_goi_theo_luoi"], d["so_buu_kien_bat_thuong"], d["ty_le_bat_thuong"]
    if goi and abs(bt / goi * 100 - tl) > TOL:
        errs.append(f"Số lượng bưu kiện bất thường / Số lượng gói theo lưới = {bt}/{goi} = {bt / goi * 100:.2f}%, "
                    f"khác Tỷ lệ bất thường {tl}%")
    if goi > d["so_luong_da_quet"]:
        errs.append(f"Số lượng gói theo lưới {goi} > Số lượng đã quét {d['so_luong_da_quet']}")
    pb = d["phan_bo_bat_thuong"]
    if bt and pb:
        for x in pb:
            if abs(x["so_luong"] / bt * 100 - x["ty_le"]) > TOL:
                errs.append(f"'{x['loai']}': {x['so_luong']} / {bt} = {x['so_luong'] / bt * 100:.2f}%, "
                            f"khác tỷ lệ {x['ty_le']}% trên chú thích")
        # Tổng % > 100 là BÌNH THƯỜNG (1 bưu kiện thuộc nhiều loại). Dưới 100 thì thiếu loại; đúng 100,00% khi
        # có >= 2 loại là dấu hiệu model chỉnh số cho tròn (đã gặp ở ảnh Inbound 03/11).
        tong = sum(x["ty_le"] for x in pb)
        if tong < 100 - TOL:
            errs.append(f"Tổng tỷ lệ chú thích 'Phân bổ loại bất thường' = {tong:.2f}% < 100%: thiếu loại hoặc đọc sai")
        elif len(pb) > 1 and abs(tong - 100) < 0.005:
            errs.append("Nghi ngờ: tổng tỷ lệ chú thích đúng 100,00% (thường > 100% vì các loại chồng nhau), "
                        "đối chiếu lại với ảnh")
    a, b = _iso(d["cong_suat_max_tu"]), _iso(d["cong_suat_max_den"])
    if not (a and b) or abs((b - a) - timedelta(minutes=59)) > timedelta(minutes=1):
        errs.append(f"Khung giờ công suất MAX {d['cong_suat_max_tu']} → {d['cong_suat_max_den']} không phải 59 phút")
    return errs + _thoi_gian(d, "Thời gian quét")


def validate_capacity(d: dict) -> list[str]:
    tu, den = _iso(d["tu_ngay"], date), _iso(d["den_ngay"], date)
    if not (tu and den):
        return [f"Ô ngày sai định dạng: '{d['tu_ngay']}', '{d['den_ngay']}'"]
    if tu > den:
        return [f"Ngày thứ nhất {tu} sau ngày thứ hai {den}"]
    can_co = [tu + timedelta(days=i) for i in range((den - tu).days + 1)]
    diem = d["cong_suat_theo_ngay"]
    ngay = [_iso(p["ngay"], date) for p in diem]
    errs = []
    if len(ngay) != len(can_co):
        errs.append(f"Có {len(ngay)} điểm có nhãn số nhưng từ {tu} đến {den} có {len(can_co)} ngày")
    if thieu := [str(x) for x in can_co if x not in ngay]:
        errs.append("Thiếu nhãn số cho ngày: " + ", ".join(thieu))
    if ngoai := [p["ngay"] for p, x in zip(diem, ngay) if x not in can_co]:
        errs.append("Ngày sai định dạng hoặc ngoài khoảng đã chọn: " + ", ".join(ngoai))
    if trung := sorted({str(x) for x in ngay if x and ngay.count(x) > 1}):
        errs.append("Ngày bị trùng: " + ", ".join(trung))
    if am := [p["ngay"] for p in diem if p["cong_suat"] <= 0]:
        errs.append("Công suất <= 0 ở ngày: " + ", ".join(am))
    return errs


def validate_sorted(d: dict) -> list[str]:
    errs = []
    s = d["correct_chute"] + d["pda"] + d["reject_chute"]
    if s != d["total"]:
        errs.append(f"CorrectChute + PDA + RejectChute = {s}, khác Total {d['total']}")
    r = sum(d[k]["so_luong"] for k in LY_DO_REJECT)
    if r != d["reject_chute"]:
        errs.append(f"NoRead + NoPostOffice + NoChute (dòng 1) = {r}, khác RejectChute {d['reject_chute']}")
    if d["reject_chute"]:
        for k in LY_DO_REJECT:
            pct = d[k]["so_luong"] / d["reject_chute"] * 100
            if abs(pct - d[k]["ty_le"]) > TOL:
                errs.append(f"{k}: {d[k]['so_luong']} / RejectChute = {pct:.2f}%, khác {d[k]['ty_le']}%")
    if d["total"]:
        pct = (d["correct_chute"] + d["pda"]) / d["total"] * 100
        if abs(pct - d["pie_correct_pct"]) > TOL:
            errs.append(f"(CorrectChute + PDA) / Total = {pct:.2f}%, khác nhãn 'Correct' {d['pie_correct_pct']}%")
    if abs(d["pie_correct_pct"] + d["pie_reject_pct"] - 100) > TOL:
        errs.append(f"Correct {d['pie_correct_pct']}% + Reject {d['pie_reject_pct']}% khác 100%")
    return errs + _thoi_gian(d, "Ô thời gian")


def validate_bcr_rate(d: dict) -> list[str]:
    rows, errs = d["bcr"], []
    if not rows:
        errs.append("Không đọc được dòng BCR nào: ảnh có đúng màn hình Hours&BcrRate không?")
    so = [r["bcr_no"] for r in rows]
    if trung := sorted({x for x in so if so.count(x) > 1}):
        errs.append("BCR_NO bị trùng: " + ", ".join(map(str, trung)))
    for r in rows:
        n = f"BCR {r['bcr_no']}:"
        if r["success"] + r["failed"] != r["total"]:
            errs.append(f"{n} SUCCESS + FAILED = {r['success'] + r['failed']}, khác TOTAL {r['total']}")
        if not 0 <= r["rate"] <= 100:
            errs.append(f"{n} RATE {r['rate']}% ngoài khoảng 0–100")
        if r["total"] and abs(r["success"] / r["total"] * 100 - r["rate"]) > TOL:
            errs.append(f"{n} SUCCESS / TOTAL = {r['success'] / r['total'] * 100:.2f}%, khác RATE {r['rate']}%")
    return errs + _thoi_gian(d, "Ô thời gian")


VALIDATORS = {"scada": validate_scada, "dmwcs_capacity": validate_capacity,
              "dmwcs_sorted": validate_sorted, "dmwcs_bcr_rate": validate_bcr_rate}


def number_leaves(v, path: str = "") -> dict:
    """Mọi giá trị số trong JSON lồng nhau -> {đường dẫn: số}, ví dụ 'phan_bo_bat_thuong[3].so_luong'."""
    if isinstance(v, bool):
        return {}
    if isinstance(v, (int, float)):
        return {path: v}
    if isinstance(v, dict):
        kids = ((f"{path}.{k}" if path else k, x) for k, x in v.items())
    elif isinstance(v, list):
        kids = ((f"{path}[{i}]", x) for i, x in enumerate(v))
    else:
        return {}
    return {p: n for kp, x in kids for p, n in number_leaves(x, kp).items()}


def diff_numbers(a: dict, b: dict) -> list[str]:
    """Trường số khác nhau giữa 2 lần đọc, dạng 'đường_dẫn: lần1 / lần2' ('—' = không có ở lần đó)."""
    na, nb = number_leaves(a), number_leaves(b)
    return [f"{p}: {na.get(p, '—')} / {nb.get(p, '—')}" for p in dict.fromkeys([*na, *nb]) if na.get(p) != nb.get(p)]
