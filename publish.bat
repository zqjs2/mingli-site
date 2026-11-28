@echo off
title Publish Blog Site
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "G:\mingli-site\publish.ps1"
echo.
echo ============================================
echo  If you see "Deployment complete", publish OK
echo  Open https://zqjs.ziqing.ccwu.cc and refresh
echo ============================================
pause
