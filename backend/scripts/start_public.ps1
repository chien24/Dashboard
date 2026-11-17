# Mở app ra Internet qua Vercel: chạy backend + Cloudflare Quick Tunnel, ghi link tunnel mới vào frontend/vercel.json,
# commit + push RIÊNG file đó để Vercel deploy lại. Ctrl+C: tắt cả backend và tunnel.
# Chạy (từ thư mục gốc repo):  powershell -ExecutionPolicy Bypass -File backend\scripts\start_public.ps1
# Lưu ý: file này phải lưu UTF-8 có BOM để Windows PowerShell 5.1 đọc đúng tiếng Việt.

$ErrorActionPreference = "Stop"
$Backend    = Split-Path -Parent $PSScriptRoot
$Root       = Split-Path -Parent $Backend
$VercelJson = Join-Path $Root "frontend\vercel.json"
$VercelUrl  = "https://dashboard-frontend-silk-zeta.vercel.app"
$Port       = 8000
$LogDir     = Join-Path $Backend "data\logs"          # backend/data đã nằm trong .gitignore
$TunnelLog  = Join-Path $LogDir "cloudflared.log"
New-Item -ItemType Directory -Force $LogDir | Out-Null

function First-Existing($paths) { $paths | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1 }
function Cmd($name) { $c = Get-Command $name -ErrorAction SilentlyContinue; if ($c) { $c.Source } }

# Python: ưu tiên .venv, không có thì python trên PATH (vd conda base)
$Py = First-Existing @("$Backend\.venv\Scripts\python.exe", "$Root\.venv\Scripts\python.exe", (Cmd python), (Cmd py))
if (-not $Py) { throw "Không tìm thấy Python. Cài Python hoặc tạo .venv theo README." }

# cloudflared: PATH, không có thì thư mục cài mặc định của winget
$Cf = First-Existing @((Cmd cloudflared), "${env:ProgramFiles(x86)}\cloudflared\cloudflared.exe", "$env:ProgramFiles\cloudflared\cloudflared.exe")
if (-not $Cf) { throw "Chưa cài cloudflared. Chạy: winget install --id Cloudflare.cloudflared" }

if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) {
    throw "Cổng $Port đang bị chiếm (có thể uvicorn đang chạy ở cửa sổ khác). Tắt nó rồi chạy lại."
}

$api = $null; $tunnel = $null
try {
    # a. backend
    Write-Host "[1/4] Chạy backend: $Py -m uvicorn app.main:app --host 127.0.0.1 --port $Port"
    $api = Start-Process -FilePath $Py -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "$Port" `
                         -WorkingDirectory $Backend -NoNewWindow -PassThru
    $ok = $false
    for ($i = 0; $i -lt 60 -and -not $ok; $i++) {
        Start-Sleep -Milliseconds 500
        if ($api.HasExited) { throw "Backend dừng ngay khi khởi động (xem lỗi ở trên)." }
        try { $ok = (Invoke-WebRequest "http://127.0.0.1:$Port/api/system/health" -UseBasicParsing -TimeoutSec 2).StatusCode -eq 200 } catch {}
    }
    if (-not $ok) { throw "Backend không trả lời /api/system/health sau 30 giây." }

    # b. tunnel, lấy link trong log (tối đa 60 giây)
    Write-Host "[2/4] Mở Cloudflare Quick Tunnel (log: $TunnelLog)"
    Remove-Item $TunnelLog -ErrorAction SilentlyContinue
    $tunnel = Start-Process -FilePath $Cf -ArgumentList "tunnel", "--no-autoupdate", "--url", "http://localhost:$Port", "--logfile", "`"$TunnelLog`"" `
                            -WindowStyle Hidden -PassThru
    $url = $null
    for ($i = 0; $i -lt 60 -and -not $url; $i++) {
        Start-Sleep -Seconds 1
        if ($tunnel.HasExited) { throw "cloudflared dừng (xem $TunnelLog)." }
        if (Test-Path $TunnelLog) {
            $m = Select-String -Path $TunnelLog -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com' | Select-Object -First 1
            if ($m) { $url = $m.Matches[0].Value }
        }
    }
    if (-not $url) { throw "Không lấy được link trycloudflare sau 60 giây (xem $TunnelLog)." }
    Write-Host "      Tunnel: $url"

    # c. ghi link vào rewrites, giữ nguyên redirects
    $j = Get-Content $VercelJson -Raw -Encoding UTF8 | ConvertFrom-Json
    $old = $null
    if ($j.rewrites) { $old = ([uri]$j.rewrites[0].destination).GetLeftPart([UriPartial]::Authority) }
    if ($old -eq $url) {
        Write-Host "[3/4] Link tunnel không đổi, không cần cập nhật vercel.json"
    } else {
        $new = [ordered]@{
            redirects = @($j.redirects)
            rewrites  = @(
                [ordered]@{ source = "/api/:path*";     destination = "$url/api/:path*" },
                [ordered]@{ source = "/uploads/:path*"; destination = "$url/uploads/:path*" }
            )
        }
        [IO.File]::WriteAllText($VercelJson, ($new | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding $false))
        Write-Host "[3/4] Đã ghi link mới vào frontend/vercel.json"

        # d. commit + push CHỈ vercel.json (git commit -- <file> bỏ qua mọi thứ khác đang stage)
        $branch = (git -C $Root rev-parse --abbrev-ref HEAD).Trim()
        if ($branch -ne "main") {
            Write-Warning "Đang ở nhánh '$branch', không phải main: không push. Vercel vẫn dùng link cũ."
        } else {
            git -C $Root add -- frontend/vercel.json
            git -C $Root commit -m "chore: cập nhật tunnel URL" -- frontend/vercel.json
            if ($LASTEXITCODE -ne 0) { throw "git commit lỗi." }
            git -C $Root push origin main
            if ($LASTEXITCODE -ne 0) { throw "git push lỗi (có thể nhánh trên GitHub đã có commit mới: chạy 'git pull --rebase' rồi chạy lại)." }
            Write-Host "[4/4] Đã push. Vercel sẽ deploy lại trong khoảng 1 phút."
        }
    }

    # e. giữ 2 tiến trình chạy
    Write-Host ""
    Write-Host "Tunnel : $url"
    Write-Host "Vercel : $VercelUrl"
    Write-Host "Đang chạy. Nhấn Ctrl+C để tắt cả backend và tunnel."
    while (-not $api.HasExited -and -not $tunnel.HasExited) { Start-Sleep -Seconds 2 }
    if ($api.HasExited) { Write-Warning "Backend đã dừng." } else { Write-Warning "Tunnel đã dừng." }
}
finally {
    foreach ($p in @($tunnel, $api)) {
        if ($p -and -not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
    }
    Write-Host "Đã tắt backend và tunnel."
}
