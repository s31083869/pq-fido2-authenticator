@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0pq_uv_host_windows.ps1" %*
exit /b %ERRORLEVEL%
