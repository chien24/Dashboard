@echo off
title OCR Dashboard - Backend (dong cua so nay = tat web)

if not exist "%~dp0backend\app\main.py" (
  echo [LOI] File .bat phai nam trong thu muc goc cua project
  echo       ^(cung cho voi thu muc backend va frontend^).
  echo       Vi tri hien tai: %~dp0
  pause
  exit /b
)

cd /d "%~dp0backend"

rem Thu tu: .venv cua project, roi "py" (Python launcher, khong can kich hoat conda), roi "python"
set "PY=python"
where py >nul 2>nul && set "PY=py"
if exist "%~dp0.venv\Scripts\python.exe" set "PY=%~dp0.venv\Scripts\python.exe"
echo Dang dung Python: %PY%

"%PY%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000

echo.
echo === Backend da dung. Chup man hinh noi dung o tren gui lai ===
pause
