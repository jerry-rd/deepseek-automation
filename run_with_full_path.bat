@echo off
chcp 65001 >nul
echo 使用完整路径运行Python脚本
echo =============================================
echo.

REM 创建截图文件夹
echo 创建截图文件夹...
if not exist screenshots mkdir screenshots
echo 截图将保存在 %CD%\screenshots 目录中
echo.

echo 此脚本将尝试使用常见的Python安装路径运行DeepSeek自动化脚本
echo.

set SCRIPT_PATH=%CD%\deepseek_automation.py

echo 检查脚本文件是否存在...
if not exist "%SCRIPT_PATH%" (
    echo 错误: 未找到脚本文件 %SCRIPT_PATH%
    goto :end
)

echo 脚本文件存在，尝试使用不同的Python路径运行...
echo.

if exist "C:\Python39\python.exe" (
    echo 尝试使用 C:\Python39\python.exe
    "C:\Python39\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Python310\python.exe" (
    echo 尝试使用 C:\Python310\python.exe
    "C:\Python310\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Python311\python.exe" (
    echo 尝试使用 C:\Python311\python.exe
    "C:\Python311\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Python312\python.exe" (
    echo 尝试使用 C:\Python312\python.exe
    "C:\Python312\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Python313\python.exe" (
    echo 尝试使用 C:\Python313\python.exe
    "C:\Python313\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files\Python39\python.exe" (
    echo 尝试使用 "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python39\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files\Python310\python.exe" (
    echo 尝试使用 "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python310\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files\Python311\python.exe" (
    echo 尝试使用 "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python311\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files\Python312\python.exe" (
    echo 尝试使用 "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python312\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files\Python313\python.exe" (
    echo 尝试使用 "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python313\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files (x86)\Python39\python.exe" (
    echo 尝试使用 "C:\Program Files (x86)\Python39\python.exe"
    "C:\Program Files (x86)\Python39\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Program Files (x86)\Python310\python.exe" (
    echo 尝试使用 "C:\Program Files (x86)\Python310\python.exe"
    "C:\Program Files (x86)\Python310\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" (
    echo 尝试使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo 尝试使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo 尝试使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    echo 尝试使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    echo 尝试使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" "%SCRIPT_PATH%" --random
    if %ERRORLEVEL% equ 0 goto :success
)

echo 未找到可用的Python安装或所有尝试都失败了。
echo 请安装Python并确保将其添加到PATH环境变量中。
goto :end

:success
echo 脚本执行成功!

:end
echo.
echo 操作完成。
pause 