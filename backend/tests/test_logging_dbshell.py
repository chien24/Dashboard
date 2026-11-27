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
import env  # noqa: E402
import fix_upload_paths  # noqa: E402
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


def test_env_sua_bang_terminal(tmp_path, monkeypatch, creds, capsys, caplog):
    from dotenv import dotenv_values

    p = tmp_path / ".env"
    p.write_bytes("# ghi chú\r\nGROQ_API_KEY=bi-mat-123\r\nLOG_LEVEL=INFO\r\n".encode())
    monkeypatch.setattr(env, "env_path", lambda: p)
    run = lambda *a: (creds(), env.main(list(a)))  # noqa: E731

    run("list")
    out = capsys.readouterr().out
    assert "GROQ_API_KEY = (có, 10 ký tự)" in out and "bi-mat" not in out and "LOG_LEVEL = INFO" in out
    run("set", "LOG_LEVEL", "WARNING")
    run("set", "LOG_DIR", "D:/log có dấu cách #1")
    assert p.read_bytes().decode() == ('# ghi chú\r\nGROQ_API_KEY=bi-mat-123\r\nLOG_LEVEL=WARNING\r\n'
                                       'LOG_DIR="D:/log có dấu cách #1"\r\n')  # dòng khác, CRLF, không BOM: giữ nguyên
    assert dotenv_values(p)["LOG_DIR"] == "D:/log có dấu cách #1"
    assert len(list(tmp_path.glob(".env.bak-*"))) >= 1
    with caplog.at_level(logging.INFO, "terminal"):
        run("set", "GROQ_API_KEY", "khoa-moi-456")
    assert "khoa-moi" not in caplog.text and "khoa-moi" not in capsys.readouterr().out and "***" in caplog.text
    assert dotenv_values(p)["GROQ_API_KEY"] == "khoa-moi-456"
    before = p.read_bytes()
    with pytest.raises(SystemExit, match="DEBUG / INFO"):
        run("set", "LOG_LEVEL", "nhieu")
    with pytest.raises(SystemExit, match="8 ký tự"):
        run("set", "AUTH_PASSWORD", "ngan")
    assert p.read_bytes() == before                                      # giá trị sai: không sửa gì
    run("unset", "LOG_DIR")
    assert "LOG_DIR" not in dotenv_values(p)


def test_sua_duong_dan_anh_sau_khi_chuyen_may(clean_db, creds, capsys):
    from app.api.upload import upload_url
    from app.db import SessionLocal
    from app.models import Upload

    old = r"D:\Học\TT\project\dashboard\backend\data\uploads\2026\11\16\abc.jpg"
    want = config.UPLOAD_DIR / "2026" / "11" / "16" / "abc.jpg"
    with SessionLocal() as db:
        db.add_all([Upload(original_name="1.jpg", stored_path=old, sha256="a"),
                    Upload(original_name="x.jpg", stored_path="la/lam.jpg", sha256="b")])
        db.commit()
    creds()
    fix_upload_paths.main([])                                            # chưa --apply: không ghi
    assert "Sẽ sửa 1 dòng · bỏ qua 1" in capsys.readouterr().out
    with SessionLocal() as db:
        assert db.query(Upload).filter_by(sha256="a").one().stored_path == old
    creds()
    fix_upload_paths.main(["--apply"])
    with SessionLocal() as db:
        up = db.query(Upload).filter_by(sha256="a").one()
        assert up.stored_path == str(want)
        assert upload_url(up) == "/uploads/2026/11/16/abc.jpg"           # ảnh cũ hiện lại được
        assert db.query(Upload).filter_by(sha256="b").one().stored_path == "la/lam.jpg"


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
