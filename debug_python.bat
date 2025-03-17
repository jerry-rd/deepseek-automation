@echo off
chcp 65001 >nul
echo Python环境调试工具
echo =============================================
echo.

echo 检查Python版本:
python --version
echo.

echo 检查Python路径:
where python
echo.

echo 检查Python模块:
python -c "import sys; print('Python路径:', sys.executable); print('Python版本:', sys.version); print('模块搜索路径:', sys.path)"
echo.

echo 检查必要模块:
python -c "try: import selenium; print('selenium已安装'); except: print('selenium未安装')"
python -c "try: import dotenv; print('dotenv已安装'); except: print('dotenv未安装')"
python -c "try: from PIL import Image; print('PIL已安装'); except: print('PIL未安装')"
echo.

echo 检查当前目录文件:
dir
echo.

echo 调试完成。
pause 