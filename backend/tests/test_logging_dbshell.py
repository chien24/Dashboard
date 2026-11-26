"""Ghi log ra file theo ngày, scripts/logs.py, scripts/dbshell.py và cổng đăng nhập của lệnh terminal."""
import io
import logging
import sys
from datetime import datetime
from pathlib import Path

import pytest

from app import config, logging_setup, terminal

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dbshell  # noqa: E402
import logs  # noqa: E402


@pytest.fixture
def creds(monkeypatch):
    """Tài khoản giả + stdin như chạy qua pipe; trả hàm đặt 2 dòng tên/mật khẩu sẽ nhập."""
    monkeypatch.setattr(config, "AUTH_USER", "admin")
    monkeypatch.setattr(config, "AUTH_PASSWORD", "đúng-mk")
    monkeypatch.setattr(terminal.time, "sleep", lambda s: None)
    return lambda user="admin", pw="đúng-mk": monkeypatch.setattr(sys, "stdin", io.StringIO(f"{user}\n{pw}\n"))


@pytest.fixture
def log_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "LOG_DIR", tmp_path)
    return tmp_path


def test_terminal_tu_choi_khi_sai_mat_khau(creds, caplog):
    creds(pw="sai")
    with caplog.at_level(logging.INFO, "terminal"), pytest.raises(SystemExit) as e:
        terminal.start("dbshell.py")
    assert e.value.code == 1
    assert "đăng nhập sai" in caplog.text and "sai" not in caplog.text.replace("đăng nhập sai", "")  # không ghi mật khẩu
    creds()
    with caplog.at_level(logging.INFO, "terminal"):
        terminal.start("dbshell.py")
    assert "đăng nhập đúng" in caplog.text


def test_terminal_tu_choi_khi_chua_dat_tai_khoan(creds, monkeypatch):
    creds()
    monkeypatch.setattr(config, "AUTH_PASSWORD", None)
    with pytest.raises(SystemExit) as e:
        terminal.start("logs.py")
    assert "AUTH_PASSWORD" in str(e.value.code)


def test_dbshell_chi_doc(clean_db, creds, capsys):
    creds()
    dbshell.main(["info"])
    out = capsys.readouterr().out
    assert "File:" in out and "Báo cáo: 0" in out
    creds()
    with pytest.raises(SystemExit) as e:
        dbshell.main(["sql", "DELETE FROM jobs"])
    assert "readonly" in str(e.value.code)
    creds()
    dbshell.main(["sql", "SELECT 'Tàng Kinh Các' AS ten"])
    assert "Tàng Kinh Các" in capsys.readouterr().out
    creds(pw="sai")
    with pytest.raises(SystemExit):  # sai mật khẩu: không chạy lệnh
        dbshell.main(["tables"])
    assert "reports" not in capsys.readouterr().out


def test_logs_loc_theo_muc_va_chu(log_dir, creds, capsys):
    logging_setup.log_file().write_text(
        "2026-11-26 09:00:00 INFO worker: Job 1 bắt đầu\n"
        "2026-11-26 09:00:05 ERROR worker: Job 1 lỗi\nTraceback (most recent call last):\n  File x\n"
        "2026-11-26 09:01:00 INFO auth: Đăng nhập thành công\n", encoding="utf-8")
    creds()
    logs.main(["--level", "warning"])
    assert capsys.readouterr().out == "2026-11-26 09:00:05 ERROR worker: Job 1 lỗi\nTraceback (most recent call last):\n  File x\n"
    creds()
    logs.main(["--grep", "đăng nhập", "-n", "5"])
    assert capsys.readouterr().out.strip() == "2026-11-26 09:01:00 INFO auth: Đăng nhập thành công"
    creds()
    logs.main(["--list"])
    assert logging_setup.log_file().name in capsys.readouterr().out


def test_file_log_theo_ngay_va_xoa_file_cu(log_dir, monkeypatch):
    monkeypatch.setattr(config, "LOG_RETENTION_DAYS", 35)
    old = log_dir / "backend-2026-01-01.log"
    old.write_text("cũ", encoding="utf-8")
    day = {"v": datetime(2026, 11, 26, 9)}
    monkeypatch.setattr(logging_setup, "now", lambda: day["v"])
    h = logging_setup.DailyFile()
    h.setFormatter(logging_setup.FMT)
    try:
        assert not old.exists()                                          # quá 35 ngày: xóa
        h.emit(logging.makeLogRecord({"msg": "hôm nay", "levelname": "INFO", "name": "t"}))
        day["v"] = datetime(2026, 11, 27, 0, 1)
        h.emit(logging.makeLogRecord({"msg": "hôm sau", "levelname": "INFO", "name": "t"}))
    finally:
        h.close()
    assert "hôm nay" in (log_dir / "backend-2026-11-26.log").read_text(encoding="utf-8")
    assert "hôm sau" in (log_dir / "backend-2026-11-27.log").read_text(encoding="utf-8")
