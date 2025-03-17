@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo DeepSeek Automation Tool Launcher
echo =============================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found. Please make sure Python is installed and added to PATH.
    goto :end
)

REM Check if script file exists
if not exist deepseek_automation.py (
    echo Error: deepseek_automation.py file not found.
    echo Please make sure the file is in the current directory.
    goto :end
)

REM Check if ChromeDriver exists
if not exist chromedriver.exe (
    echo Warning: chromedriver.exe not found.
    echo Do you want to download ChromeDriver? (Y/N)
    set /p download_choice=
    if /i "!download_choice!"=="Y" (
        echo Downloading ChromeDriver...
        python download_chromedriver_134.py
        if %ERRORLEVEL% neq 0 (
            echo Failed to download ChromeDriver. Please download it manually and place it in the current directory.
            goto :end
        )
    ) else (
        echo Please download ChromeDriver manually and place it in the current directory.
        goto :end
    )
)

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found.
    echo Creating .env file...
    echo DEEPSEEK_PHONE=your_phone_number>.env
    echo DEEPSEEK_PASSWORD=your_password>>.env
    echo Please edit the .env file and enter your DeepSeek phone number and password.
    notepad .env
)

:menu
cls
echo DeepSeek Automation Tool - Menu
echo =============================================
echo 1. Ask a single question
echo 2. Ask multiple questions (command line)
echo 3. Ask questions from a file
echo 4. Ask a random question
echo 5. Advanced options
echo 6. Edit .env file
echo 7. Edit questions config file
echo 8. Exit
echo.
set /p choice=Select an option (1-8): 

if "%choice%"=="1" goto :single_question
if "%choice%"=="2" goto :multiple_questions
if "%choice%"=="3" goto :file_questions
if "%choice%"=="4" goto :random_question
if "%choice%"=="5" goto :advanced_options
if "%choice%"=="6" goto :edit_env
if "%choice%"=="7" goto :edit_config
if "%choice%"=="8" goto :end

echo Invalid choice, please try again.
timeout /t 2 >nul
goto :menu

:single_question
cls
echo Ask a Single Question
echo =============================================
set /p question=Enter your question: 
echo.
echo Executing...
python deepseek_automation.py --question "%question%"
echo.
echo Execution completed.
pause
goto :menu

:multiple_questions
cls
echo Ask Multiple Questions (Command Line)
echo =============================================
echo Enter questions, each enclosed in quotes, press Enter when done
echo Example: "Question 1" "Question 2" "Question 3"
echo.
set /p questions=Enter questions: 
echo.
echo Executing...
python deepseek_automation.py --questions %questions%
echo.
echo Execution completed.
pause
goto :menu

:file_questions
cls
echo Ask Questions from a File
echo =============================================
if not exist questions_config.txt (
    echo Warning: Default questions config file not found.
    echo Do you want to create a sample file? (Y/N)
    set /p create_choice=
    if /i "!create_choice!"=="Y" (
        echo Creating sample questions file...
        echo What are the core technical advantages of DeepSeek AI?>questions_config.txt
        echo How to use DeepSeek for code generation?>>questions_config.txt
        echo What features does DeepSeek have compared to other large language models?>>questions_config.txt
    )
)
set /p file=Enter questions file path (default: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
if not exist "!file!" (
    echo Error: File "!file!" does not exist.
    pause
    goto :menu
)
echo.
echo Executing...
python deepseek_automation.py --questions-file "!file!"
echo.
echo Execution completed.
pause
goto :menu

:random_question
cls
echo Ask a Random Question
echo =============================================
set /p config=Enter config file path (default: questions_config.txt): 
if "!config!"=="" set config=questions_config.txt
if not exist "!config!" (
    echo Error: File "!config!" does not exist.
    pause
    goto :menu
)
echo.
echo Executing...
python deepseek_automation.py --random --config "!config!"
echo.
echo Execution completed.
pause
goto :menu

:advanced_options
cls
echo Advanced Options
echo =============================================
echo 1. Set wait time between questions
echo 2. Set maximum retry attempts for each question
echo 3. Combine multiple options
echo 4. Return to main menu
echo.
set /p adv_choice=Select an option (1-4): 

if "%adv_choice%"=="1" goto :wait_time
if "%adv_choice%"=="2" goto :max_retries
if "%adv_choice%"=="3" goto :combined_options
if "%adv_choice%"=="4" goto :menu

echo Invalid choice, please try again.
timeout /t 2 >nul
goto :advanced_options

:wait_time
cls
echo Set Wait Time Between Questions
echo =============================================
set /p file=Enter questions file path (default: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p wait_time=Enter wait time in seconds (default: 3): 
if "!wait_time!"=="" set wait_time=3
echo.
echo Executing...
python deepseek_automation.py --questions-file "!file!" --wait-time !wait_time!
echo.
echo Execution completed.
pause
goto :menu

:max_retries
cls
echo Set Maximum Retry Attempts
echo =============================================
set /p file=Enter questions file path (default: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p retries=Enter maximum retry attempts (default: 3): 
if "!retries!"=="" set retries=3
echo.
echo Executing...
python deepseek_automation.py --questions-file "!file!" --max-retries !retries!
echo.
echo Execution completed.
pause
goto :menu

:combined_options
cls
echo Combine Multiple Options
echo =============================================
set /p file=Enter questions file path (default: questions_config.txt): 
if "!file!"=="" set file=questions_config.txt
set /p wait_time=Enter wait time in seconds (default: 3): 
if "!wait_time!"=="" set wait_time=3
set /p retries=Enter maximum retry attempts (default: 3): 
if "!retries!"=="" set retries=3
set /p use_random=Use random questions? (Y/N) (default: N): 
if "!use_random!"=="" set use_random=N

echo.
echo Executing...
if /i "!use_random!"=="Y" (
    python deepseek_automation.py --random --config "!file!" --wait-time !wait_time! --max-retries !retries!
) else (
    python deepseek_automation.py --questions-file "!file!" --wait-time !wait_time! --max-retries !retries!
)
echo.
echo Execution completed.
pause
goto :menu

:edit_env
cls
echo Edit .env File
echo =============================================
if not exist .env (
    echo DEEPSEEK_PHONE=your_phone_number>.env
    echo DEEPSEEK_PASSWORD=your_password>>.env
)
notepad .env
goto :menu

:edit_config
cls
echo Edit Questions Config File
echo =============================================
set /p config=Enter config file path (default: questions_config.txt): 
if "!config!"=="" set config=questions_config.txt
if not exist "!config!" (
    echo File "!config!" does not exist. Create it? (Y/N)
    set /p create_choice=
    if /i "!create_choice!"=="Y" (
        echo Creating file "!config!"...
        echo What are the core technical advantages of DeepSeek AI?>"!config!"
        echo How to use DeepSeek for code generation?>>"!config!"
        echo What features does DeepSeek have compared to other large language models?>>"!config!"
    ) else (
        goto :menu
    )
)
notepad "!config!"
goto :menu

:end
echo.
echo Thank you for using the DeepSeek Automation Tool!
timeout /t 3 >nul
endlocal 