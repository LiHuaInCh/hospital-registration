# 公共函数：路径、服务检测、端口、进程与 ngrok 隧道工具
# 由 start.ps1 / stop.ps1 / status.ps1 以 dot-source 方式引入

$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $Root 'backend'
$JarPath = Join-Path $BackendDir 'target\hospital-registration-1.0.0.jar'
$LogDir = Join-Path $Root 'logs'
$PidFile = Join-Path $LogDir 'backend.pid'
$NgrokPidFile = Join-Path $LogDir 'ngrok.pid'
$BackendUrl = 'http://127.0.0.1:8080'
$HealthUrl = 'http://127.0.0.1:8080/api/department/list'

# ngrok 预留的静态域名；换账号或换域名时只改这一行
$NgrokDomain = 'campsite-recount-floss.ngrok-free.dev'

function Write-Step($text) { Write-Host "   $text" }
function Write-Ok($text) { Write-Host "   [OK] $text" -ForegroundColor Green }
function Write-Note($text) { Write-Host "   [!] $text" -ForegroundColor Yellow }
function Write-Bad($text) { Write-Host "   [X] $text" -ForegroundColor Red }
function Write-Dim($text) { Write-Host "   $text" -ForegroundColor DarkGray }

function Test-Admin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-DbService {
    foreach ($name in @('MySQL80', 'MySQL', 'MySQL57', 'MariaDB')) {
        $service = Get-Service -Name $name -ErrorAction SilentlyContinue
        if ($service) { return $service }
    }
    return $null
}

function Test-PortOpen([int]$port) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    return [bool]$conn
}

function Wait-PortOpen([int]$port, [int]$seconds) {
    $deadline = (Get-Date).AddSeconds($seconds)
    while ((Get-Date) -lt $deadline) {
        if (Test-PortOpen $port) { return $true }
        Start-Sleep -Milliseconds 500
    }
    return (Test-PortOpen $port)
}

# 启动/停止 Windows 服务；权限不足时弹一次 UAC 授权
function Invoke-ServiceAction([string]$name, [string]$action) {
    try {
        if ($action -eq 'Start') {
            Start-Service -Name $name -ErrorAction Stop
        } else {
            Stop-Service -Name $name -Force -ErrorAction Stop
        }
        return $true
    } catch {
        if (Test-Admin) { return $false }
        Write-Host '   需要管理员权限，正在弹出授权窗口，请点击「是」…' -ForegroundColor Yellow
        $command = if ($action -eq 'Start') {
            "Start-Service -Name '$name' -ErrorAction Stop"
        } else {
            "Stop-Service -Name '$name' -Force -ErrorAction Stop"
        }
        try {
            $proc = Start-Process -FilePath 'powershell' `
                -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $command) `
                -Verb RunAs -Wait -PassThru -ErrorAction Stop
            return ($proc.ExitCode -eq 0)
        } catch {
            return $false
        }
    }
}

# 找到本项目启动的 java 进程（按命令行匹配 jar 名，避免误杀其他 Java 程序）
function Get-BackendProcesses {
    $result = @()
    Get-CimInstance Win32_Process -Filter "Name='java.exe'" -ErrorAction SilentlyContinue |
        ForEach-Object {
            if ($_.CommandLine -and $_.CommandLine -like '*hospital-registration*') {
                $result += [pscustomobject]@{ Id = [int]$_.ProcessId; CommandLine = $_.CommandLine }
            }
        }
    return $result
}

function Get-BackendHealthy {
    try {
        $resp = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 3 -ErrorAction Stop
        return ($resp.code -eq 200)
    } catch {
        return $false
    }
}

function Get-LanAddress {
    $address = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object {
            $_.IPAddress -notlike '127.*' -and
            $_.IPAddress -notlike '169.254.*' -and
            $_.InterfaceAlias -notlike '*Loopback*'
        } |
        Select-Object -First 1
    if ($address) { return $address.IPAddress }
    return $null
}

function Get-JavaPath {
    $cmd = Get-Command java -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}

# ---------- ngrok 内网穿透 ----------

function Get-NgrokPath {
    $cmd = Get-Command ngrok -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $candidates = @(
        (Join-Path $env:USERPROFILE 'ngrok.exe'),
        (Join-Path $env:LOCALAPPDATA 'ngrok\ngrok.exe'),
        'C:\ngrok\ngrok.exe',
        (Join-Path $env:ProgramFiles 'ngrok\ngrok.exe')
    )
    foreach ($path in $candidates) {
        if ($path -and (Test-Path $path)) { return $path }
    }
    return $null
}

# 查询 ngrok 本地管理接口（4040），返回 https 隧道对象
function Get-NgrokTunnel {
    try {
        $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels' -TimeoutSec 2 -ErrorAction Stop
        return ($resp.tunnels | Where-Object { $_.proto -eq 'https' } | Select-Object -First 1)
    } catch {
        return $null
    }
}

# 只匹配本项目用的 ngrok 进程，避免误杀其他隧道
function Get-NgrokProcesses {
    $result = @()
    Get-CimInstance Win32_Process -Filter "Name='ngrok.exe'" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $cmdline = $_.CommandLine
            if ($cmdline -and ($cmdline -like '*8080*' -or $cmdline -like "*$NgrokDomain*")) {
                $result += [pscustomobject]@{ Id = [int]$_.ProcessId; CommandLine = $cmdline }
            }
        }
    return $result
}

function Start-NgrokTunnel {
    param(
        [string]$NgrokPath,
        [string]$Domain,
        [string]$TunnelLogDir
    )
    New-Item -ItemType Directory -Force -Path $TunnelLogDir | Out-Null
    $outLog = Join-Path $TunnelLogDir 'ngrok.out.log'
    $errLog = Join-Path $TunnelLogDir 'ngrok.err.log'
    if (Test-Path $outLog) { Remove-Item $outLog -Force -ErrorAction SilentlyContinue }
    if (Test-Path $errLog) { Remove-Item $errLog -Force -ErrorAction SilentlyContinue }

    $arguments = @('http')
    if ($Domain) { $arguments += "--domain=$Domain" }
    $arguments += @('8080', '--log=stdout')

    $proc = Start-Process -FilePath $NgrokPath `
        -ArgumentList $arguments `
        -WindowStyle Hidden `
        -RedirectStandardOutput $outLog `
        -RedirectStandardError $errLog `
        -PassThru
    Set-Content -Path (Join-Path $TunnelLogDir 'ngrok.pid') -Value $proc.Id -Encoding ascii
    return $proc
}
