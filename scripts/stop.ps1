param(
    [switch]$KeepDatabase,
    [switch]$KeepTunnel
)

. (Join-Path $PSScriptRoot 'common.ps1')

Write-Host ''
Write-Host '   医院门诊挂号平台 · 停止服务' -ForegroundColor Cyan
Write-Host '   --------------------------------' -ForegroundColor DarkGray

# 1. 停后端：优先用 PID 文件，同时按命令行兜底
$targets = @()
if (Test-Path $PidFile) {
    $saved = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($saved -and $saved -match '^\d+$') { $targets += [int]$saved }
}
Get-BackendProcesses | ForEach-Object { $targets += $_.Id }
$targets = $targets | Sort-Object -Unique

$stopped = 0
foreach ($processId in $targets) {
    $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($proc -and $proc.ProcessName -eq 'java') {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        $stopped++
    }
}

if ($stopped -gt 0) {
    Write-Ok "后端已停止（$stopped 个进程）"
} else {
    Write-Step '后端未在运行'
}

Remove-Item $PidFile -ErrorAction SilentlyContinue
for ($i = 0; $i -lt 20; $i++) {
    if (-not (Test-PortOpen 8080)) { break }
    Start-Sleep -Milliseconds 300
}

# 2. 停 ngrok 隧道
if ($KeepTunnel) {
    Write-Step '按要求保留 ngrok 隧道'
} else {
    $tunnels = Get-NgrokProcesses
    if ($tunnels.Count -gt 0) {
        foreach ($tunnel in $tunnels) {
            Stop-Process -Id $tunnel.Id -Force -ErrorAction SilentlyContinue
        }
        Write-Ok "ngrok 隧道已停止（$($tunnels.Count) 个进程）"
    } else {
        Write-Step 'ngrok 隧道未在运行'
    }
    Remove-Item $NgrokPidFile -ErrorAction SilentlyContinue
}

# 3. 停数据库
if ($KeepDatabase) {
    Write-Step '按要求保留 MySQL 服务运行'
} else {
    $service = Get-DbService
    if (-not $service) {
        Write-Step '未检测到 MySQL 服务，跳过'
    } elseif ($service.Status -ne 'Running') {
        Write-Step "MySQL 服务 $($service.Name) 已是停止状态"
    } else {
        Write-Step "正在停止 MySQL 服务 $($service.Name) …"
        if (Invoke-ServiceAction $service.Name 'Stop') {
            Write-Ok 'MySQL 已停止'
        } else {
            Write-Note 'MySQL 停止失败（需要管理员权限），可手动在「服务」中停止'
        }
    }
}

Write-Host ''
Write-Ok '已全部停止'
Write-Host ''
