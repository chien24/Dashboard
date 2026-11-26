@echo off
rem Dong goi OCR Dashboard thanh file cai dat cho Windows. Chi chay tren may build (can Python).
rem May nguoi dung KHONG can Python: Python da nam san trong goi.
rem   Ket qua: dist\OCRDashboard-Setup.exe (neu co Inno Setup 6), nguoc lai dist\OCRDashboard-portable.zip
rem   Khong goi .env, data, anh upload, log: cac thu do tao luc chay tren may nguoi dung.
rem   Chay tu dong (agent/CI): set NO_PAUSE=1 truoc khi goi de khong dung lai cho bam phim.
setlocal
cd /d "%~dp0"
title Dong goi OCR Dashboard

set "PY=python"
where py >nul 2>nul && set "PY=py"
set "VENV=%~dp0build\venv"

echo [1/4] Tao moi truong build rieng: %VENV%
if not exist "%VENV%\Scripts\python.exe" (
  "%PY%" -m venv "%VENV%" || goto :err
)
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip >nul || goto :err
"%VENV%\Scripts\python.exe" -m pip install -r ..\requirements.txt -r requirements-build.txt || goto :err
rem Python conda/miniconda de DLL (sqlite3, ffi, expat...) o <base>\Library\bin, khong nam canh .pyd:
rem them vao PATH de PyInstaller tim thay va goi vao, neu khong may nguoi dung se loi "DLL load failed ... _sqlite3"
for /f "delims=" %%b in ('call "%VENV%\Scripts\python.exe" -c "import sys; print(sys.base_prefix)"') do set "BASE=%%b"
if exist "%BASE%\Library\bin" (
  echo     Python conda: them %BASE%\Library\bin vao PATH khi dong goi
  set "PATH=%BASE%\Library\bin;%PATH%"
)

echo [2/4] PyInstaller: dist\OCRDashboard\OCRDashboard.exe
"%VENV%\Scripts\python.exe" -m PyInstaller --noconfirm --clean --distpath dist --workpath build\work ocr_dashboard.spec || goto :err

echo [3/4] Kiem tra nhanh exe
dist\OCRDashboard\OCRDashboard.exe help >nul || goto :err
rem "help" khong dung toi sqlite: kiem tra rieng DLL cua sqlite3 (thieu thi exe khong mo duoc DB)
if not exist "dist\OCRDashboard\_internal\sqlite3.dll" goto :nodll
if exist "dist\OCRDashboard\_internal\.env" goto :leak
if exist "dist\OCRDashboard\_internal\data" goto :leak

echo [4/4] Tao file cai dat
for /f %%v in ('powershell -NoProfile -Command "Get-Date -Format yyyy.MM.dd.HHmm"') do set "VER=%%v"
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if defined ISCC (
  "%ISCC%" /Qp /DAppVersion=%VER% installer.iss || goto :err
  echo.
  echo XONG: %~dp0dist\OCRDashboard-Setup.exe  ^(phien ban %VER%^)
) else (
  echo Khong thay Inno Setup 6 ^(cai: winget install JRSoftware.InnoSetup^) - tao file zip thay the
  powershell -NoProfile -Command "Compress-Archive -Path 'dist\OCRDashboard' -DestinationPath 'dist\OCRDashboard-portable.zip' -Force" || goto :err
  echo.
  echo XONG: %~dp0dist\OCRDashboard-portable.zip  ^(giai nen roi chay OCRDashboard.exe^)
)
if not defined NO_PAUSE pause
exit /b 0

:leak
echo [LOI] Trong goi co .env hoac data: KHONG duoc phat hanh ban nay. Kiem tra lai ocr_dashboard.spec
if not defined NO_PAUSE pause
exit /b 1

:nodll
echo [LOI] Trong goi thieu sqlite3.dll: exe se khong mo duoc database. Kiem tra Python dung de build.
if not defined NO_PAUSE pause
exit /b 1

:err
echo.
echo [LOI] Dong goi that bai o buoc tren. Chup man hinh gui lai.
if not defined NO_PAUSE pause
exit /b 1
