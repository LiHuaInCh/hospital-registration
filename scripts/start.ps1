param(
    [switch]$SkipBuild,
    [switch]$SkipTunnel
)

. (Join-Path $PSScriptRoot 'common.ps1')

Write-Host ''
Write-Host '   医院门诊挂号平台 · 一键启动' -ForegroundColor Cyan
Write-Host '   --------------------------------' -ForegroundColor DarkGray

# 1. 数据库
$service = Get-DbService
if (-not $service) {
    Write-Note '未检测到 MySQL 服务，跳过（使用远程数据库时可忽略）'
} elseif ($service.Status -eq 'Running') {
    Write-Ok "MySQL 服务 $($service.Name) 已在运行"
} else {
    Write-Step "正在启动 MySQL 服务 $($service.Name) …"
    if (-not (Invoke-ServiceAction $service.Name 'Start')) {
        Write-Bad 'MySQL 启动失败，请右键 start.bat 选择「以管理员身份运行」'
        exit 1
    }
    (Get-Service $service.Name).WaitForStatus('Running', [TimeSpan]::FromSeconds(30))
    Write-Ok 'MySQL 已启动'
}

if (-not (Wait-PortOpen 3306 20)) {
    Write-Bad '3306 端口未监听，数据库可能尚未就绪'
    exit 1
}

# 2. 后端 jar
if (-not (Test-Path $JarPath)) {
    if ($SkipBuild) {
        Write-Bad '缺少后端 jar（backend/target），且指定了 -SkipBuild'
        exit 1
    }
    Write-Step '首次启动，正在编译后端（约 30 秒）…'
    if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) {
        Write-Bad '未找到 Maven，请先安装或手动执行 mvn package'
        exit 1
    }
    Push-Location $BackendDir
    try {
        & mvn -B -ntp -q -DskipTests package
        if ($LASTEXITCODE -ne 0) {
            Write-Bad '后端编译失败，请查看上面的 Maven 输出'
            exit 1
        }
    } finally {
        Pop-Location
    }
    Write-Ok '编译完成'
}

# 3. 后端是否已在运行
$backendStarted = $false
if (Test-PortOpen 8080) {
    $running = Get-BackendProcesses
    if ($running -and (Get-BackendHealthy)) {
        Write-Ok "后端已在运行（PID $($running[0].Id)），无需重复启动"
    } else {
        Write-Bad '8080 端口被其他程序占用，请先释放该端口（可执行 scripts\stop.ps1 后重试）'
        exit 1
    }
} else {
    $java = Get-JavaPath
    if (-not $java) {
        Write-Bad '未找到 java，请确认已安装 JDK 并配置 PATH'
        exit 1
    }

    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    $outLog = Join-Path $LogDir 'backend.out.log'
    $errLog = Join-Path $LogDir 'backend.err.log'
    if (Test-Path $outLog) { Remove-Item $outLog -Force }
    if (Test-Path $errLog) { Remove-Item $errLog -Force }

    Write-Step '正在启动后端 …'
    $proc = Start-Process -FilePath $java `
        -ArgumentList @('-Dfile.encoding=UTF-8', '-jar', "`"$JarPath`"") `
        -WorkingDirectory $Root `
        -WindowStyle Hidden `
        -RedirectStandardOutput $outLog `
        -RedirectStandardError $errLog `
        -PassThru
    Set-Content -Path $PidFile -Value $proc.Id -Encoding ascii

    Write-Step '等待服务就绪 …'
    $deadline = (Get-Date).AddSeconds(60)
    $healthy = $false
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 1
        if ($proc.HasExited) { break }
        if (Get-BackendHealthy) { $healthy = $true; break }
    }

    if (-not $healthy) {
        Write-Bad '后端启动失败'
        if (Test-Path $errLog) {
            $tail = Get-Content $errLog -Tail 15 -ErrorAction SilentlyContinue
            if ($tail) {
                Write-Host ''
                Write-Host '   --- 错误日志 ---' -ForegroundColor DarkGray
                $tail | ForEach-Object { Write-Host "   $_" -ForegroundColor DarkGray }
            }
        }
        Write-Host ''
        Write-Note '常见原因：数据库未初始化（执行 database/init.sql）、application.yml 里的账号密码不对'
        exit 1
    }
    $backendStarted = $true
}

# 4. ngrok 内网穿透
$publicUrl = $null
if ($SkipTunnel) {
    Write-Step '按要求跳过 ngrok 隧道'
} else {
    $ngrok = Get-NgrokPath
    if (-not $ngrok) {
        Write-Note '未找到 ngrok，跳过公网隧道（可只在本机调试）'
    } else {
        $tunnel = Get-NgrokTunnel
        if ($tunnel) {
            $publicUrl = $tunnel.public_url
            Write-Ok "ngrok 隧道已在运行：$publicUrl"
        } else {
            Write-Step '正在启动 ngrok 隧道 …'
            $tunnelProc = Start-NgrokTunnel -NgrokPath $ngrok -Domain $NgrokDomain -TunnelLogDir $LogDir
            $deadline = (Get-Date).AddSeconds(30)
            while ((Get-Date) -lt $deadline) {
                Start-Sleep -Milliseconds 800
                if ($tunnelProc.HasExited) { break }
                $tunnel = Get-NgrokTunnel
                if ($tunnel) { break }
            }
            if ($tunnel) {
                $publicUrl = $tunnel.public_url
                Write-Ok "公网地址 $publicUrl"
            } else {
                Write-Note 'ngrok 隧道启动失败，详见 logs\ngrok.out.log（后端仍在运行）'
            }
        }
    }
}

$lan = Get-LanAddress
Write-Host ''
Write-Ok '启动完成'
Write-Host ''
Write-Host "   后端接口   $BackendUrl" -ForegroundColor White
if ($publicUrl) {
    Write-Host "   公网地址   $publicUrl" -ForegroundColor White
    Write-Dim '真机、体验版、其他电脑都用这个地址（app.js 里的 baseUrl）'
} elseif ($lan) {
    Write-Host "   局域网     http://${lan}:8080" -ForegroundColor White
}
Write-Host '   管理后台   admin / 123456' -ForegroundColor White
Write-Dim '运行日志   logs\backend.out.log、logs\ngrok.out.log'
Write-Dim '停止服务   双击 stop.bat'
Write-Host ''

if ($backendStarted) { exit 0 }
