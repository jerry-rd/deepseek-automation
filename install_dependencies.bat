@echo off
chcp 65001 >nul
echo DeepSeek自动化工具 - 依赖安装
echo =============================================
echo.

echo 正在检查Python安装...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 错误: 未找到Python。请确保Python已安装并添加到PATH环境变量中。
    goto :try_full_path
)

echo Python已安装，正在安装依赖...
echo.
echo 安装python-dotenv模块...
python -m pip install python-dotenv
echo.
echo 安装selenium模块...
python -m pip install selenium
echo.
echo 安装Pillow模块...
python -m pip install Pillow
echo.
echo 依赖安装完成。
goto :end

:try_full_path
echo 尝试使用完整路径安装依赖...
echo.

if exist "C:\Python39\python.exe" (
    echo 使用 C:\Python39\python.exe 安装依赖...
    "C:\Python39\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Python310\python.exe" (
    echo 使用 C:\Python310\python.exe 安装依赖...
    "C:\Python310\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Python311\python.exe" (
    echo 使用 C:\Python311\python.exe 安装依赖...
    "C:\Python311\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Program Files\Python39\python.exe" (
    echo 使用 "C:\Program Files\Python39\python.exe" 安装依赖...
    "C:\Program Files\Python39\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Program Files\Python310\python.exe" (
    echo 使用 "C:\Program Files\Python310\python.exe" 安装依赖...
    "C:\Program Files\Python310\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" (
    echo 使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" 安装依赖...
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo 使用 "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" 安装依赖...
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" -m pip install python-dotenv selenium Pillow
    goto :success
)

echo 未找到可用的Python安装。请安装Python并确保将其添加到PATH环境变量中。
goto :end

:success
echo 依赖安装完成。

:end
echo.
echo 按任意键退出...
pause 