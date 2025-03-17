@echo off
chcp 65001 >nul
echo Chrome版本检查和ChromeDriver下载工具
echo =============================================
echo.

echo 正在运行Chrome版本检查脚本...
python check_chrome_version.py

echo.
echo 操作完成。
pause 