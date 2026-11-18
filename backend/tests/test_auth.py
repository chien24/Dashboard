"""Đăng nhập tài khoản dùng chung: chưa đăng nhập thì mọi API dữ liệu / ảnh / upload đều 401; trang HTML vẫn mở được."""
from conftest import client
from fastapi.testclient import TestClient

from app import config
from app.api import auth
from app.main import app


def test_chua_dang_nhap_bi_chan(clean_db):
    c = TestClient(app)
    for method, path in [("get", "/api/reports"), ("get", "/api/dashboard/scada"), ("post", "/api/upload"),
                         ("put", "/api/reports/1"), ("delete", "/api/reports/1"), ("get", "/uploads/2026/x.png"),
                         ("get", "/docs"), ("get", "/openapi.json")]:
        assert getattr(c, method)(path).status_code == 401, path
    assert c.get("/api/system/health").status_code == 200
    assert c.get("/api/auth/me").json() == {"logged_in": False}
    assert c.get("/html/index.html").status_code == 200


def test_dang_nhap_dang_xuat(clean_db):
    c = TestClient(app)
    assert c.post("/api/auth/login", json={"username": config.AUTH_USER, "password": "sai"}).status_code == 401
    auth._fails.clear()
    c = client()
    assert c.get("/api/auth/me").json() == {"logged_in": True}
    r = c.get("/api/reports")
    assert r.status_code == 200 and r.headers["cache-control"] == "private, no-cache"
    assert c.get("/docs").status_code == 200
    c2 = client()  # máy thứ 2 đăng nhập cùng tài khoản, máy 1 vẫn dùng được
    assert c.get("/api/reports").status_code == 200 and c2.get("/api/reports").status_code == 200
    c.post("/api/auth/logout")
    assert c.get("/api/reports").status_code == 401
    c.cookies.set(auth.COOKIE, "9999999999.gia_mao")
    assert c.get("/api/reports").status_code == 401


def test_khoa_sau_nhieu_lan_sai(clean_db, monkeypatch):
    c, sai = TestClient(app), {"username": "x", "password": "y"}
    clock = [1000.0]
    monkeypatch.setattr(auth.time, "time", lambda: clock[0])
    for i in range(1, auth.MAX_FAILS):  # 4 lần đầu: 401 kèm số lần đã sai
        r = c.post("/api/auth/login", json=sai)
        assert r.status_code == 401 and r.json()["detail"]["fails"] == i
        clock[0] += 60
    r = c.post("/api/auth/login", json=sai)  # lần thứ 5: khóa ngay, đủ 5 phút tính từ lúc này
    assert r.status_code == 429 and r.json()["detail"]["retry_after"] == auth.LOCK_S
    clock[0] += auth.LOCK_S - 1  # các lần sai cũ đã quá 5 phút nhưng khóa vẫn còn: đúng mật khẩu cũng bị chặn
    dung = {"username": config.AUTH_USER, "password": config.AUTH_PASSWORD}
    assert c.post("/api/auth/login", json=dung).json()["detail"]["retry_after"] == 1
    clock[0] += 1
    assert c.post("/api/auth/login", json=dung).status_code == 200
    auth._fails.clear(); auth._locked.clear()
