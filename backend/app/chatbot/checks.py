"""Cảnh báo do backend tự kiểm tra từ pham_vi (mục 11), không phụ thuộc LLM."""
from datetime import date, timedelta

from app import config
from app.chatbot import executor
from app.chatbot.context import cutoff

# view -> (view chứa ngày có dữ liệu, tên hiển thị)
SOURCE = {
    "v_scada_summary": ("v_scada_summary", "SCADA (HT1)"),
    "v_scada_abnormal": ("v_scada_summary", "SCADA (HT1)"),
    "v_dmwcs_sorted": ("v_dmwcs_sorted", "Sorted (HT2)"),
    "v_dmwcs_no_chute": ("v_dmwcs_sorted", "Sorted (HT2)"),
    "v_dmwcs_capacity": ("v_dmwcs_capacity", "Capacity (HT2)"),
    "v_dmwcs_bcr": ("v_dmwcs_bcr", "BCR rate (HT2)"),
}
MAX_DAYS_LIST = 10
MAX_RANGE = 62  # khoảng dài hơn thì không liệt kê ngày thiếu


def dm(d) -> str:
    return date.fromisoformat(str(d)[:10]).strftime("%d/%m")


def _q(sql, params=()):
    return executor.run(sql, params)[1]


def scope(pham_vi: dict | None, today: date) -> tuple[date, date, list[str]] | None:
    """(tu, den, views) đã kiểm định dạng; None nếu thiếu/sai."""
    try:
        tu, den = date.fromisoformat(pham_vi["tu_ngay"]), date.fromisoformat(pham_vi["den_ngay"])
    except (TypeError, KeyError, ValueError):
        return None
    views = [v for v in (pham_vi.get("views") or []) if isinstance(v, str)]
    return (min(tu, den), max(tu, den), views)


def before_run(pham_vi: dict | None, today: date) -> tuple[list[str], str | None]:
    """-> (cảnh báo, lời đáp thay cho chạy SQL). Cả khoảng trước mốc retention thì không chạy SQL."""
    s = scope(pham_vi, today)
    if not s:
        return [], None
    tu, den, _ = s
    cut = cutoff(today)
    msg = f"Dữ liệu trước {cut:%d/%m/%Y} đã bị xóa theo chính sách lưu {config.RETENTION_DAYS} ngày"
    if den < cut:
        return [], msg + f", nên không còn số liệu cho {dm(tu)}–{dm(den)}."
    warns = [msg + f"; kết quả chỉ tính từ {dm(cut)}."] if tu < cut else []
    if den > today:
        warns.append(f"Các ngày sau hôm nay ({dm(today)}) chưa có dữ liệu.")
    return warns, None


def missing_days(view: str, tu: date, den: date) -> list[date]:
    have = {r[0] for r in _q(f"SELECT DISTINCT ngay FROM {SOURCE[view][0]} WHERE ngay BETWEEN ? AND ?",
                             (tu.isoformat(), den.isoformat()))}
    return [d for d in (tu + timedelta(days=i) for i in range((den - tu).days + 1)) if d.isoformat() not in have]


def _day_list(days) -> str:
    s = ", ".join(dm(d) for d in days[:MAX_DAYS_LIST])
    return s + (f" và {len(days) - MAX_DAYS_LIST} ngày khác" if len(days) > MAX_DAYS_LIST else "")


def after_run(pham_vi: dict | None, today: date) -> list[str]:
    """Ngày thiếu, report cần kiểm tra, loại UNKNOWN, NoChute bị cắt, ảnh đang OCR."""
    warns = []
    s = scope(pham_vi, today)
    if s:
        tu, den, views = s
        tu, den = max(tu, cutoff(today)), min(den, today)
        rng = (tu.isoformat(), den.isoformat())
        if tu <= den:
            sources = {SOURCE[v] for v in views if v in SOURCE}
            if (den - tu).days < MAX_RANGE:
                for view, label in sorted(sources):
                    if miss := missing_days(view, tu, den):
                        warns.append(f"Chưa có dữ liệu {label} các ngày: {_day_list(miss)}.")
            for v in views:
                if v not in SOURCE:
                    continue
                for ngay, src in _q(f"SELECT DISTINCT t.ngay, q.source_name FROM {v} t JOIN v_report_quality q "
                                    "ON q.report_id = t.report_id WHERE t.trang_thai = 'can_kiem_tra' "
                                    "AND t.ngay BETWEEN ? AND ? ORDER BY t.ngay LIMIT 10", rng):
                    w = f"Report ngày {dm(ngay)} ({src or 'không rõ tên ảnh'}) cần kiểm tra: số có thể sai do lệch giữa 2 lần OCR."
                    if w not in warns:
                        warns.append(w)
            if "v_scada_abnormal" in views and (n := _q(
                    "SELECT COUNT(*) FROM v_scada_abnormal WHERE loai_key = 'UNKNOWN' AND ngay BETWEEN ? AND ?", rng)[0][0]):
                warns.append(f"Có {n} dòng loại bất thường chưa phân loại được (UNKNOWN) trong khoảng này.")
            if {"v_dmwcs_no_chute", "v_dmwcs_sorted"} & set(views):
                cut_days = [r[0] for r in _q("SELECT ngay FROM v_dmwcs_sorted WHERE no_chute_bi_cat = 1 AND ngay BETWEEN ? AND ? "
                                             "ORDER BY ngay", rng)]
                if cut_days:
                    warns.append(f"Danh sách máng NoChute ngày {_day_list(cut_days)} bị cắt trên ảnh, có thể thiếu máng.")
    # shortcut: job chưa OCR xong thì chưa biết ngày báo cáo, nên báo mọi ảnh đang chờ; cần chính xác hơn thì lưu ngày dự kiến lúc upload.
    if n := _q("SELECT COUNT(*) FROM jobs WHERE status IN ('pending', 'running')")[0][0]:
        warns.append(f"Có {n} ảnh đang được OCR, số liệu có thể thay đổi sau ít phút.")
    return warns


def is_empty(rows: list) -> bool:
    """Không có dòng, hoặc mọi giá trị NULL (SUM trên tập rỗng)."""
    return not rows or all(v is None for r in rows for v in r)


def empty_answer(pham_vi: dict | None, today: date, day_chuyen: list) -> str:
    """Kết quả rỗng: phân biệt chưa có ảnh / bộ lọc không khớp. Không bao giờ nói 'bằng 0'."""
    s = scope(pham_vi, today)
    if s:
        tu, den, views = s
        tu2, den2 = max(tu, cutoff(today)), min(den, today)
        sources = sorted({SOURCE[v] for v in views if v in SOURCE})
        if tu2 <= den2 and sources and all(len(missing_days(v, tu2, den2)) == (den2 - tu2).days + 1 for v, _ in sources):
            labels = ", ".join(lbl for _, lbl in sources)
            latest = [f"{lbl}: {dm(r[0][0])}" for v, lbl in sources if (r := _q(f"SELECT MAX(ngay) FROM {v}")) and r[0][0]]
            return (f"Chưa có dữ liệu {labels} cho {dm(tu2)}–{dm(den2)} (chưa có ảnh được OCR cho khoảng này). "
                    + (f"Ngày gần nhất có dữ liệu: {'; '.join(latest)}." if latest else ""))
    hint = ""
    if s and any(v.startswith("v_scada") for v in s[2]) and day_chuyen:
        hint = " Tên dây chuyền đang có: " + ", ".join(t for _, t in day_chuyen) + "."
    return "Không có dòng nào khớp điều kiện của câu hỏi (đã có dữ liệu trong khoảng ngày này)." + hint
