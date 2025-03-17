@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo DeepSeek自动化工具启动器
echo =============================================
echo.

REM 创建截图文件夹
echo 创建截图文件夹...
if not exist screenshots mkdir screenshots
echo 截图将保存在 %CD%\screenshots 目录中

echo 正在检查Python安装...
REM 检查Python是否安装
where python >nul 2>nul
echo 检查结果: %ERRORLEVEL%
if %ERRORLEVEL% neq 0 (
    echo 错误: 未找到Python。请确保Python已安装并添加到PATH环境变量中。
    goto :end
)

echo Python已安装，版本信息:
python --version

echo 正在检查脚本文件...
REM 检查脚本文件是否存在
if not exist deepseek_automation.py (
    echo 错误: 未找到deepseek_automation.py文件。
    echo 请确保该文件在当前目录中。
    goto :end
)

echo 脚本文件存在。

echo 正在检查ChromeDriver...
REM 检查ChromeDriver是否存在
if not exist chromedriver.exe (
    echo 警告: 未找到chromedriver.exe。
    
    choice /C YN /M "是否要下载ChromeDriver?"
    if errorlevel 2 goto :skip_chromedriver
    if errorlevel 1 (
        echo 正在尝试下载ChromeDriver...
        
        if exist download_chromedriver_134.py (
            echo 找到下载脚本，正在执行...
            python download_chromedriver_134.py
            if %ERRORLEVEL% neq 0 (
                echo 使用Python脚本下载失败，尝试使用PowerShell下载...
                powershell -Command "& {Invoke-WebRequest -Uri 'https://storage.googleapis.com/chrome-for-testing-public/134.0.5226.0/win64/chromedriver-win64.zip' -OutFile 'chromedriver.zip'}"
                powershell -Command "& {Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force}"
                copy chromedriver-win64\chromedriver.exe . >nul 2>nul
            )
        ) else (
            echo 下载脚本不存在，使用PowerShell下载...
            powershell -Command "& {Invoke-WebRequest -Uri 'https://storage.googleapis.com/chrome-for-testing-public/134.0.5226.0/win64/chromedriver-win64.zip' -OutFile 'chromedriver.zip'}"
            powershell -Command "& {Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force}"
            copy chromedriver-win64\chromedriver.exe . >nul 2>nul
        )
        
        if exist chromedriver.exe (
            echo ChromeDriver下载成功。
        ) else (
            echo ChromeDriver下载失败。请手动下载并放置在当前目录。
            echo 您可以从 https://chromedriver.chromium.org/downloads 下载。
            goto :skip_chromedriver
        )
    )
) else (
    echo ChromeDriver已找到。
)

:skip_chromedriver

echo 正在检查.env文件...
REM 检查.env文件是否存在
if not exist .env (
    echo 警告: 未找到.env文件。
    echo 正在创建.env文件...
    echo DEEPSEEK_PHONE=your_phone_number>.env
    echo DEEPSEEK_PASSWORD=your_password>>.env
    echo 请编辑.env文件，填入您的DeepSeek手机号和密码。
    
    choice /C YN /M "是否现在编辑.env文件?"
    if errorlevel 1 if not errorlevel 2 notepad .env
)

echo 环境检查完成，准备显示菜单...
pause

:menu
cls
echo DeepSeek自动化工具 - 功能菜单
echo =============================================
echo 1. 提问单个问题
echo 2. 提问多个问题（命令行指定）
echo 3. 从文件中提问多个问题
echo 4. 随机选择问题
echo 5. 高级选项
echo 6. 编辑.env文件
echo 7. 编辑问题配置文件
echo 8. 退出
echo.
set /p choice=请选择功能 (1-8): 

if "%choice%"=="1" goto :single_question
if "%choice%"=="2" goto :multiple_questions
if "%choice%"=="3" goto :file_questions
if "%choice%"=="4" goto :random_question
if "%choice%"=="5" goto :advanced_options
if "%choice%"=="6" goto :edit_env
if "%choice%"=="7" goto :edit_config
if "%choice%"=="8" goto :end

echo 无效选择，请重新输入。
timeout /t 2 >nul
goto :menu

:single_question
cls
echo 提问单个问题
echo =============================================
set /p question=请输入您的问题: 
echo.
echo 正在执行...
python deepseek_automation.py --question "%question%"
echo.
echo 执行完成。
pause
goto :menu

:multiple_questions
cls
echo 提问多个问题（命令行指定）
echo =============================================
echo 请输入问题，每个问题用引号括起来，按回车结束输入
echo 示例: "问题1" "问题2" "问题3"
echo.
set /p questions=请输入问题: 
echo.
echo 正在执行...
python deepseek_automation.py --questions %questions%
echo.
echo 执行完成。
pause
goto :menu

:file_questions
cls
echo 从文件中提问多个问题
echo =============================================
if not exist questions_config.txt (
    echo 警告: 未找到默认问题配置文件。
    echo 是否要创建一个示例文件? (Y/N)
    set /p create_choice=
    if /i "!create_choice!"=="Y" (
        echo 创建示例问题文件...
        echo DeepSeek AI的核心技术优势是什么？>questions_config.txt
        echo 如何使用DeepSeek进行代码生成？>>questions_config.txt
        echo DeepSeek与其他大语言模型相比有哪些特点？>>questions_config.txt
    )
)
set /p file=请输入问题文件路径 (默认: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
if not exist "!file!" (
    echo 错误: 文件 "!file!" 不存在。
    pause
    goto :menu
)
echo.
echo 正在执行...
python deepseek_automation.py --questions-file "!file!"
echo.
echo 执行完成。
pause
goto :menu

:random_question
cls
echo 随机选择问题
echo =============================================
set /p config=请输入配置文件路径 (默认: questions_config.txt): 
if "!config!"=="" set config=questions_config.txt
if not exist "!config!" (
    echo 错误: 文件 "!config!" 不存在。
    pause
    goto :menu
)
echo.
echo 正在执行...
python deepseek_automation.py --random --config "!config!"
echo.
echo 执行完成。
pause
goto :menu

:advanced_options
cls
echo 高级选项
echo =============================================
echo 1. 设置问题之间的等待时间
echo 2. 设置每个问题的最大尝试次数
echo 3. 组合使用多个选项
echo 4. 返回主菜单
echo.
set /p adv_choice=请选择选项 (1-4): 

if "%adv_choice%"=="1" goto :wait_time
if "%adv_choice%"=="2" goto :max_retries
if "%adv_choice%"=="3" goto :combined_options
if "%adv_choice%"=="4" goto :menu

echo 无效选择，请重新输入。
timeout /t 2 >nul
goto :advanced_options

:wait_time
cls
echo 设置问题之间的等待时间
echo =============================================
set /p file=请输入问题文件路径 (默认: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p wait_time=请输入等待时间(秒) (默认: 3): 
if "!wait_time!"=="" set wait_time=3
echo.
echo 正在执行...
python deepseek_automation.py --questions-file "!file!" --wait-time !wait_time!
echo.
echo 执行完成。
pause
goto :menu

:max_retries
cls
echo 设置每个问题的最大尝试次数
echo =============================================
set /p file=请输入问题文件路径 (默认: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p retries=请输入最大尝试次数 (默认: 3): 
if "!retries!"=="" set retries=3
echo.
echo 正在执行...
python deepseek_automation.py --questions-file "!file!" --max-retries !retries!
echo.
echo 执行完成。
pause
goto :menu

:combined_options
cls
echo 组合使用多个选项
echo =============================================
set /p file=请输入问题文件路径 (默认: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p wait_time=请输入等待时间(秒) (默认: 3): 
if "!wait_time!"=="" set wait_time=3
set /p retries=请输入最大尝试次数 (默认: 3): 
if "!retries!"=="" set retries=3
set /p use_random=是否使用随机问题? (Y/N) (默认: N): 
if "!use_random!"=="" set use_random=N

echo.
echo 正在执行...
if /i "!use_random!"=="Y" (
    python deepseek_automation.py --random --config "!file!" --wait-time !wait_time! --max-retries !retries!
) else (
    python deepseek_automation.py --questions-file "!file!" --wait-time !wait_time! --max-retries !retries!
)
echo.
echo 执行完成。
pause
goto :menu

:edit_env
cls
echo 编辑.env文件
echo =============================================
if not exist .env (
    echo DEEPSEEK_PHONE=your_phone_number>.env
    echo DEEPSEEK_PASSWORD=your_password>>.env
)
notepad .env
goto :menu

:edit_config
cls
echo 编辑问题配置文件
echo =============================================
set /p config=请输入配置文件路径 (默认: questions_config.txt): 
if "!config!"=="" set config=questions_config.txt
if not exist "!config!" (
    echo 文件 "!config!" 不存在。是否创建? (Y/N)
    set /p create_choice=
    if /i "!create_choice!"=="Y" (
        echo 创建文件 "!config!"...
        echo DeepSeek AI的核心技术优势是什么？>"!config!"
        echo 如何使用DeepSeek进行代码生成？>>"!config!"
        echo DeepSeek与其他大语言模型相比有哪些特点？>>"!config!"
    ) else (
        goto :menu
    )
)
notepad "!config!"
goto :menu

:end
echo.
echo 感谢使用DeepSeek自动化工具！
timeout /t 3 >nul
endlocal 