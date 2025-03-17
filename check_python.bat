@echo off
chcp 65001 >nul
echo Python安装检查工具
echo =============================================
echo.

echo 检查Python命令...
where python
echo 退出代码: %ERRORLEVEL%
echo.

echo 检查Python3命令...
where python3
echo 退出代码: %ERRORLEVEL%
echo.

echo 检查py命令...
where py
echo 退出代码: %ERRORLEVEL%
echo.

echo 检查系统PATH环境变量...
echo %PATH%
echo.

echo 尝试直接调用Python可执行文件...
if exist "C:\Python39\python.exe" (
    echo 尝试 C:\Python39\python.exe -V
    "C:\Python39\python.exe" -V
)

if exist "C:\Python310\python.exe" (
    echo 尝试 C:\Python310\python.exe -V
    "C:\Python310\python.exe" -V
)

if exist "C:\Python311\python.exe" (
    echo 尝试 C:\Python311\python.exe -V
    "C:\Python311\python.exe" -V
)

if exist "C:\Python312\python.exe" (
    echo 尝试 C:\Python312\python.exe -V
    "C:\Python312\python.exe" -V
)

if exist "C:\Python313\python.exe" (
    echo 尝试 C:\Python313\python.exe -V
    "C:\Python313\python.exe" -V
)

if exist "C:\Program Files\Python39\python.exe" (
    echo 尝试 "C:\Program Files\Python39\python.exe" -V
    "C:\Program Files\Python39\python.exe" -V
)

if exist "C:\Program Files\Python310\python.exe" (
    echo 尝试 "C:\Program Files\Python310\python.exe" -V
    "C:\Program Files\Python310\python.exe" -V
)

if exist "C:\Program Files\Python311\python.exe" (
    echo 尝试 "C:\Program Files\Python311\python.exe" -V
    "C:\Program Files\Python311\python.exe" -V
)

if exist "C:\Program Files\Python312\python.exe" (
    echo 尝试 "C:\Program Files\Python312\python.exe" -V
    "C:\Program Files\Python312\python.exe" -V
)

if exist "C:\Program Files\Python313\python.exe" (
    echo 尝试 "C:\Program Files\Python313\python.exe" -V
    "C:\Program Files\Python313\python.exe" -V
)

if exist "C:\Program Files (x86)\Python39\python.exe" (
    echo 尝试 "C:\Program Files (x86)\Python39\python.exe" -V
    "C:\Program Files (x86)\Python39\python.exe" -V
)

if exist "C:\Program Files (x86)\Python310\python.exe" (
    echo 尝试 "C:\Program Files (x86)\Python310\python.exe" -V
    "C:\Program Files (x86)\Python310\python.exe" -V
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" (
    echo 尝试 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" -V
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" -V
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo 尝试 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" -V
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" -V
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo 尝试 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" -V
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" -V
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    echo 尝试 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" -V
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" -V
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    echo 尝试 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" -V
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" -V
)

echo.
echo 检查完成。
pause 