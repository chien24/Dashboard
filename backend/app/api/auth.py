"""Đăng nhập bằng 1 tài khoản dùng chung. Phiên = cookie ký HMAC (không lưu server) nên đăng nhập được ở nhiều máy cùng lúc."""
import hashlib
import hmac
import secrets
import time

from fastapi import APIRouter, Body, HTTPException, Request, Response

from app import config

router = APIRouter(prefix="/api/auth", tags=["auth"])
COOKIE = "ocr_session"
MAX_AGE = 7 * 24 * 3600
# Không đặt SESSION_SECRET thì ký bằng chính tài khoản: đổi mật khẩu là mọi phiên cũ hết hạn.
_KEY = hashlib.sha256((config.SESSION_SECRET or f"{config.AUTH_USER}:{config.AUTH_PASSWORD}").encode()).digest()
# shortcut: đếm sai mật khẩu theo IP trong RAM (mất khi restart, sau reverse proxy mọi người chung 1 IP); cần chặt hơn thì chuyển sang proxy/fail2ban.
_fails: dict[str, list[float]] = {}
MAX_FAILS, LOCK_S = 5, 300


def _sign(exp: int) -> str:
    return hmac.new(_KEY, str(exp).encode(), hashlib.sha256).hexdigest()


def is_logged_in(request: Request) -> bool:
    exp, _, sig = (request.cookies.get(COOKIE) or "").partition(".")
    return exp.isdigit() and int(exp) > time.time() and hmac.compare_digest(sig, _sign(int(exp)))


@router.post("/login")
def login(request: Request, response: Response, username: str = Body(...), password: str = Body(...)):
    ip = request.client.host if request.client else "?"
    recent = [t for t in _fails.get(ip, []) if t > time.time() - LOCK_S]
    if len(recent) >= MAX_FAILS:
        raise HTTPException(429, "Sai mật khẩu quá nhiều lần, thử lại sau 5 phút")
    ok = secrets.compare_digest(username.encode(), config.AUTH_USER.encode()) & \
        secrets.compare_digest(password.encode(), config.AUTH_PASSWORD.encode())
    if not ok:
        _fails[ip] = recent + [time.time()]
        raise HTTPException(401, "Sai tài khoản hoặc mật khẩu")
    _fails.pop(ip, None)
    exp = int(time.time()) + MAX_AGE
    response.set_cookie(COOKIE, f"{exp}.{_sign(exp)}", max_age=MAX_AGE, httponly=True, samesite="lax",
                        secure=request.url.scheme == "https")
    return {"logged_in": True, "username": config.AUTH_USER}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE)
    return {"logged_in": False}


@router.get("/me")
def me(request: Request):
    return {"logged_in": is_logged_in(request)}
