@echo off
chcp 65001 >nul
setlocal
set "PS=pwsh"
where pwsh >nul 2>&1 || set "PS=powershell"
title Hospital Registration - Start
"%PS%" -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1" %*
echo.
pause
