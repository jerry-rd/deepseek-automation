@echo off
chcp 65001 >nul
echo DeepSeek自动化工具 - 无检查版
echo =============================================
echo.

REM 创建截图文件夹
echo 创建截图文件夹...
if not exist screenshots mkdir screenshots
echo 截图将保存在 %CD%\screenshots 目录中
echo.

echo 跳过所有检查，直接执行...
echo.

echo 正在执行随机问题...
python deepseek_automation.py --random

echo.
echo 执行完成。
pause 