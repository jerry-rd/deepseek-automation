@echo off
chcp 65001 >nul
echo 使用pip安装依赖
echo =============================================
echo.

echo 正在安装依赖...
pip install -r requirements.txt

echo.
echo 安装完成。
pause 