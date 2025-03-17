@echo off
chcp 65001 >nul
echo Python安装工具
echo =============================================
echo.

echo 此脚本将下载并安装Python 3.10.11
echo 请确保您有管理员权限运行此脚本
echo.
pause

echo 正在下载Python安装程序...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile 'python-3.10.11-amd64.exe'}"

if not exist "python-3.10.11-amd64.exe" (
    echo 下载失败，请检查网络连接或手动下载Python安装程序。
    echo 您可以从 https://www.python.org/downloads/ 下载。
    goto :end
)

echo 下载完成。
echo.
echo 正在安装Python...
echo 请在安装程序中选择"Add Python to PATH"选项。
echo.
start /wait python-3.10.11-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo.
echo 安装完成。请重新打开命令提示符并运行 python -V 检查安装是否成功。
echo.

:end
pause 