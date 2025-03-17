@echo off
chcp 65001 >nul
echo ChromeDriver检查和下载工具
echo =============================================
echo.

echo 正在检查当前目录...
dir chromedriver.exe
echo.

echo 是否要下载ChromeDriver? (Y/N)
set /p download_choice=

if /i "%download_choice%"=="Y" (
    echo 正在尝试下载ChromeDriver...
    
    if exist download_chromedriver_134.py (
        echo 找到下载脚本，正在执行...
        python download_chromedriver_134.py
    ) else (
        echo 下载脚本不存在，正在创建简单的下载命令...
        echo 使用PowerShell下载...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://storage.googleapis.com/chrome-for-testing-public/134.0.5226.0/win64/chromedriver-win64.zip' -OutFile 'chromedriver.zip'}"
        
        echo 解压文件...
        powershell -Command "& {Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force}"
        
        echo 移动文件...
        copy chromedriver-win64\chromedriver.exe .
    )
) else (
    echo 已取消下载。
)

echo.
echo 再次检查ChromeDriver...
dir chromedriver.exe

echo.
echo 操作完成。
pause 