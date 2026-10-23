. (Join-Path $PSScriptRoot 'common.ps1')

Write-Host ''
Write-Host '   医院门诊挂号平台 · 运行状态' -ForegroundColor Cyan
Write-Host '   --------------------------------' -ForegroundColor DarkGray

$service = Get-DbService
if (-not $service) {
    Write-Note 'MySQL 服务：未安装或服务名不匹配'
} elseif ($service.Status -eq 'Running') {
    $portText = if (Test-PortOpen 3306) { '端口 3306 已监听' } else { '端口 3306 未监听' }
    Write-Ok "MySQL 服务：运行中（$($service.Name)，$portText）"
} else {
    Write-Note "MySQL 服务：已停止（$($service.Name)）"
}

$backend = Get-BackendProcesses
if ($backend -and (Test-PortOpen 8080)) {
    Write-Ok "后端进程：运行中（PID $($backend[0].Id)，端口 8080）"
    if (Get-BackendHealthy) {
        Write-Ok "接口自检：正常（$BackendUrl）"
    } else {
        Write-Note '接口自检：端口在监听，但接口未返回 200'
    }
} elseif (Test-PortOpen 8080) {
    Write-Note '8080 端口被其他程序占用'
} else {
    Write-Step '后端进程：未运行'
}

$tunnel = Get-NgrokTunnel
if ($tunnel) {
    Write-Ok "ngrok 隧道：$($tunnel.public_url) → $($tunnel.config.addr)"
} else {
    $ngrokProcesses = Get-NgrokProcesses
    if ($ngrokProcesses.Count -gt 0) {
        Write-Note 'ngrok 进程在运行，但隧道尚未就绪'
    } else {
        Write-Step 'ngrok 隧道：未运行'
    }
}

$lan = Get-LanAddress
if ($lan) { Write-Dim "局域网地址：http://${lan}:8080" }
Write-Dim '运行日志：logs\backend.out.log、logs\ngrok.out.log'
Write-Host ''
