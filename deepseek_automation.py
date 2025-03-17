import os
import time
import argparse
import sys
import random
from datetime import datetime
from dotenv import load_dotenv
print("Script started")
print(f"Python version: {sys.version}")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from PIL import Image
    print("All modules imported successfully")
except Exception as e:
    print(f"Error importing modules: {str(e)}")
    sys.exit(1)

# Load environment variables
print("Loading environment variables")
try:
    load_dotenv()
    print("Environment variables loaded")
except Exception as e:
    print(f"Error loading environment variables: {str(e)}")

def setup_driver():
    """Set up and return a configured Chrome WebDriver."""
    print("Setting up Chrome WebDriver")
    try:
        chrome_options = Options()
        # Uncomment the line below to run in headless mode (no browser UI)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        
        # Add options to bypass SSL certificate errors
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--disable-web-security")
        
        # Add additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-features=NetworkService")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--dns-prefetch-disable")
        
        # Use a local ChromeDriver instead of downloading it
        # First, check if chromedriver.exe exists in the current directory
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        if not os.path.exists(chromedriver_path):
            print(f"ChromeDriver not found at {chromedriver_path}")
            print("Please download ChromeDriver from https://chromedriver.chromium.org/downloads")
            print("and place it in the current directory as 'chromedriver.exe'")
            sys.exit(1)
        
        print(f"Using ChromeDriver at {chromedriver_path}")
        service = Service(executable_path=chromedriver_path)
        print("Creating Chrome WebDriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set page load timeout to 60 seconds
        driver.set_page_load_timeout(60)
        
        print("Chrome WebDriver created successfully")
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {str(e)}")
        sys.exit(1)

def login_to_deepseek(driver, phone, password):
    """Log in to DeepSeek Chat using phone number and password."""
    print("Navigating to DeepSeek Chat...")
    try:
        # Try with HTTPS first
        driver.get("https://chat.deepseek.com/")
        print("Successfully loaded the page with HTTPS")
    except Exception as e:
        print(f"Error loading with HTTPS: {str(e)}")
        try:
            # Try with HTTP if HTTPS fails
            driver.get("http://chat.deepseek.com/")
            print("Successfully loaded the page with HTTP")
        except Exception as e:
            print(f"Error loading with HTTP: {str(e)}")
            return False
    
    try:
        # 等待页面加载完成
        print("Waiting for page to load...")
        time.sleep(5)
        
        # 截图初始页面
        take_screenshot(driver, "screenshots", "initial_page.png")
        print("Saved screenshot of initial page")
        
        # 检查是否已经在登录页面，如果不是，点击登录按钮
        try:
            # 查找并点击登录按钮（如果在主页）
            print("Looking for login button...")
            login_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), '登录')]"))
            )
            print(f"Found login button with text: {login_button.text}")
            login_button.click()
            print("Clicked login button")
            time.sleep(2)
        except Exception as e:
            print(f"No login button found or already on login page: {str(e)}")
        
        # 截图登录表单
        take_screenshot(driver, "screenshots", "login_form.png")
        print("Saved screenshot of login form")
        
        # 使用精确的XPath切换到密码登录
        try:
            # 使用用户提供的密码登录tab的XPath
            print("Clicking password login tab using exact XPath...")
            password_tab = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]"))
            )
            password_tab.click()
            print("Switched to password login")
            time.sleep(1)
        except Exception as e:
            print(f"Error clicking password login tab: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative method to find password login tab...")
                password_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '密码登录')]"))
                )
                password_tab.click()
                print("Switched to password login using alternative method")
                time.sleep(1)
            except Exception as e2:
                print(f"No password login tab found or already on password login: {str(e2)}")
        
        # 使用精确的XPath输入手机号
        try:
            print("Entering phone number using exact XPath...")
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div/input"))
            )
            phone_input.clear()
            phone_input.send_keys(phone)
            print(f"Entered phone number: {phone}")
        except Exception as e:
            print(f"Error finding phone input with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative method to find phone input...")
                phone_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, '手机号') or contains(@placeholder, '邮箱')]"))
                )
                phone_input.clear()
                phone_input.send_keys(phone)
                print(f"Entered phone number using alternative method: {phone}")
            except Exception as e2:
                print(f"Failed to find phone input: {str(e2)}")
                return False
        
        # 使用精确的XPath输入密码
        try:
            print("Entering password using exact XPath...")
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[5]/div[1]/div/input"))
            )
            password_input.clear()
            password_input.send_keys(password)
            print("Entered password")
        except Exception as e:
            print(f"Error finding password input with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative method to find password input...")
                password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password' or contains(@placeholder, '密码')]"))
                )
                password_input.clear()
                password_input.send_keys(password)
                print("Entered password using alternative method")
            except Exception as e2:
                print(f"Failed to find password input: {str(e2)}")
                return False
        
        # 使用精确的XPath勾选同意协议
        try:
            print("Checking agreement checkbox using exact XPath...")
            agreement_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[6]/div[1]/div/div[1]/div"))
            )
            if not agreement_checkbox.is_selected():
                agreement_checkbox.click()
                print("Checked agreement checkbox")
        except Exception as e:
            print(f"Error finding agreement checkbox with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative method to find agreement checkbox...")
                agreement_checkbox = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox'] | //div[contains(@class, 'checkbox')]"))
                )
                if not agreement_checkbox.is_selected():
                    agreement_checkbox.click()
                    print("Checked agreement checkbox using alternative method")
            except Exception as e2:
                print(f"No agreement checkbox found or already checked: {str(e2)}")
        
        # 截图填写完成的登录表单
        take_screenshot(driver, "screenshots", "filled_login_form.png")
        print("Saved screenshot of filled login form")
        
        # 使用精确的XPath点击登录按钮
        try:
            print("Clicking login button using exact XPath...")
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[7]"))
            )
            submit_button.click()
            print("Clicked login button")
        except Exception as e:
            print(f"Error finding login button with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative method to find login button...")
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(text(), '登录')]"))
                )
                submit_button.click()
                print("Clicked login button using alternative method")
            except Exception as e2:
                print(f"Failed to find login button: {str(e2)}")
                return False
        
        # 等待登录完成，检查是否进入聊天界面
        print("Waiting for login to complete...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'chat-container') or //textarea[contains(@placeholder, 'Send a message') or contains(@placeholder, '发送消息')]]"))
        )
        print("Successfully logged in")
        
        # 截图登录成功的页面
        take_screenshot(driver, "screenshots", "login_success.png")
        print("Saved screenshot of successful login")
        
        return True
        
    except Exception as e:
        print(f"Login failed: {str(e)}")
        # 截图登录失败的页面
        take_screenshot(driver, "screenshots", "login_failed.png")
        print("Saved screenshot of failed login attempt")
        return False

def ask_question(driver, question):
    """Ask a question in the chat interface."""
    try:
        # Wait for the input area to be available
        input_area = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Send a message') or contains(@placeholder, '发送消息')]"))
        )
        
        # Clear any existing text and enter the question
        input_area.clear()
        input_area.send_keys(question)
        
        # 使用用户提供的精确XPath勾选"深度思考"选项
        try:
            print("Clicking '深度思考' option using exact XPath...")
            deep_thinking_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[1]"))
            )
            deep_thinking_option.click()
            print("Clicked '深度思考' option")
            time.sleep(1)
        except Exception as e:
            print(f"Error clicking '深度思考' option with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative methods to find '深度思考' option...")
                # 尝试方法1：使用文本内容查找
                try:
                    deep_thinking_option = driver.find_element(By.XPATH, "//div[contains(text(), '深度思考') or contains(text(), 'R1')]")
                    deep_thinking_option.click()
                    print("Clicked '深度思考' option using text content")
                    time.sleep(1)
                except Exception as e1:
                    print(f"Failed to find '深度思考' option by text: {str(e1)}")
                    
                # 尝试方法2：使用相对位置
                try:
                    # 尝试点击输入框下方的第一个按钮
                    input_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, '发送消息')]")
                    parent_div = input_box.find_element(By.XPATH, "./ancestor::div[contains(@class, 'flex')]")
                    buttons = parent_div.find_elements(By.XPATH, ".//div[contains(@class, 'button')]")
                    if len(buttons) > 0:
                        buttons[0].click()
                        print("Clicked first button near input box (likely '深度思考')")
                        time.sleep(1)
                except Exception as e2:
                    print(f"Failed to find '深度思考' option by position: {str(e2)}")
            except Exception as e3:
                print(f"All attempts to find '深度思考' option failed: {str(e3)}")
        
        # 使用用户提供的精确XPath勾选"联网搜索"选项
        try:
            print("Clicking '联网搜索' option using exact XPath...")
            web_search_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[2]"))
            )
            web_search_option.click()
            print("Clicked '联网搜索' option")
            time.sleep(1)
        except Exception as e:
            print(f"Error clicking '联网搜索' option with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative methods to find '联网搜索' option...")
                # 尝试方法1：使用文本内容查找
                try:
                    web_search_option = driver.find_element(By.XPATH, "//div[contains(text(), '联网搜索') or contains(text(), 'Web Search')]")
                    web_search_option.click()
                    print("Clicked '联网搜索' option using text content")
                    time.sleep(1)
                except Exception as e1:
                    print(f"Failed to find '联网搜索' option by text: {str(e1)}")
                    
                # 尝试方法2：使用相对位置
                try:
                    # 尝试点击输入框下方的第二个按钮
                    input_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, '发送消息')]")
                    parent_div = input_box.find_element(By.XPATH, "./ancestor::div[contains(@class, 'flex')]")
                    buttons = parent_div.find_elements(By.XPATH, ".//div[contains(@class, 'button')]")
                    if len(buttons) > 1:
                        buttons[1].click()
                        print("Clicked second button near input box (likely '联网搜索')")
                        time.sleep(1)
                except Exception as e2:
                    print(f"Failed to find '联网搜索' option by position: {str(e2)}")
            except Exception as e3:
                print(f"All attempts to find '联网搜索' option failed: {str(e3)}")
        
        # 截图勾选选项后的状态
        take_screenshot(driver, "screenshots", "options_checked.png")
        print("Saved screenshot after checking options")
        
        # 使用用户提供的精确XPath点击提交按钮
        try:
            print("Clicking submit button using exact XPath...")
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]"))
            )
            submit_button.click()
            print("Clicked submit button")
        except Exception as e:
            print(f"Error clicking submit button with exact XPath: {str(e)}")
            # 尝试备用方法
            try:
                print("Trying alternative methods to find submit button...")
                # 尝试方法1：使用通用提交按钮XPath
                try:
                    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                    submit_button.click()
                    print("Clicked submit button using type attribute")
                except Exception as e1:
                    print(f"Failed to find submit button by type: {str(e1)}")
                    
                # 尝试方法2：使用相对位置
                try:
                    # 尝试点击输入框旁边的按钮
                    input_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, '发送消息')]")
                    parent_div = input_box.find_element(By.XPATH, "./ancestor::div[contains(@class, 'flex')]")
                    submit_button = parent_div.find_element(By.XPATH, ".//button")
                    submit_button.click()
                    print("Clicked button near input box (likely submit)")
                except Exception as e2:
                    print(f"Failed to find submit button by position: {str(e2)}")
            except Exception as e3:
                print(f"All attempts to find submit button failed: {str(e3)}")
                return False
        
        print(f"Question sent: {question}")
        
        # 截图发送问题后的页面
        take_screenshot(driver, "screenshots", "question_sent.png")
        print("Saved screenshot after sending question")
        
        # Wait for the response to complete
        # This is a bit tricky as we need to detect when the AI has finished responding
        # We'll look for the loading indicator to disappear
        print("Waiting for response to complete (timeout: 5 minutes)...")
        WebDriverWait(driver, 600).until_not(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'typing')]"))
        )
        
        print("Response completed")
        
        # Give a little extra time for any animations to complete
        time.sleep(5)
        
        # 截图获得回答后的页面
        take_screenshot(driver, "screenshots", "response_received.png")
        print("Saved screenshot after receiving response")
        
        return True
    except Exception as e:
        print(f"Failed to ask question: {str(e)}")
        # 截图失败状态
        take_screenshot(driver, "screenshots", "question_failed.png")
        print("Saved screenshot of failed question attempt")
        return False

def take_screenshot(driver, output_dir="screenshots", filename=None):
    """Take a screenshot of the current page."""
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate a filename with timestamp if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"deepseek_chat_{timestamp}.png"
        
        # Full path to save the screenshot
        filepath = os.path.join(output_dir, filename)
        
        # Take the screenshot
        driver.save_screenshot(filepath)
        print(f"Screenshot saved to {filepath}")
        
        return filepath
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")
        return None

def load_questions_from_file(file_path):
    """从文件加载问题列表"""
    try:
        print(f"Reading questions from file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
        print(f"Read {len(questions)} questions from file")
        return questions
    except Exception as e:
        print(f"Error reading questions file: {str(e)}")
        return []

def get_random_question(questions_file):
    """从问题文件中随机选择一个问题"""
    questions = load_questions_from_file(questions_file)
    if not questions:
        print("No questions found in the file")
        return None
    
    random_question = random.choice(questions)
    print(f"Randomly selected question: {random_question}")
    return random_question

def main():
    print("Starting main function")
    parser = argparse.ArgumentParser(description="Automate DeepSeek Chat interactions")
    parser.add_argument("--question", type=str, help="Question to ask DeepSeek")
    parser.add_argument("--questions-file", type=str, help="File containing questions, one per line")
    parser.add_argument("--random", action="store_true", help="Randomly select a question from the questions file")
    parser.add_argument("--config", type=str, default="questions_config.txt", help="Configuration file with questions (default: questions_config.txt)")
    parser.add_argument("--wait-time", type=int, default=3, help="Wait time in seconds between questions (default: 3)")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum number of retries for each question (default: 3)")
    parser.add_argument("--questions", nargs='+', help="Multiple questions to ask (space separated)")
    args = parser.parse_args()
    
    # Get credentials from environment variables
    phone = os.getenv("DEEPSEEK_PHONE")
    password = os.getenv("DEEPSEEK_PASSWORD")
    
    # 检查凭据是否已更新
    if phone == "your_phone_number" or password == "your_password":
        print("错误: 请先在.env文件中设置您的实际DeepSeek手机号和密码")
        print("Error: Please set your actual DeepSeek phone number and password in the .env file")
        return
    
    print(f"Credentials loaded: phone={'*****' if phone else 'None'}, password={'*****' if password else 'None'}")
    
    if not phone or not password:
        print("Error: Phone number and password must be set in the .env file")
        return
    
    # Get questions
    questions = []
    
    # 处理随机问题选择
    if args.random:
        config_file = args.config
        if not os.path.exists(config_file):
            print(f"Error: Configuration file '{config_file}' not found")
            return
        
        random_question = get_random_question(config_file)
        if random_question:
            questions.append(random_question)
    # 处理直接指定的问题
    elif args.question:
        questions.append(args.question)
    # 处理从命令行传入的多个问题
    elif args.questions:
        questions.extend(args.questions)
    # 处理从文件读取的问题列表
    elif args.questions_file:
        questions = load_questions_from_file(args.questions_file)
    
    if not questions:
        print("No questions provided. Use --question, --questions, --questions-file, or --random with --config")
        return
    
    print(f"Total questions to process: {len(questions)}")
    
    print("Setting up WebDriver")
    # Setup the WebDriver
    driver = setup_driver()
    
    try:
        # Login to DeepSeek
        print("Attempting to login to DeepSeek")
        if login_to_deepseek(driver, phone, password):
            print("\n登录已完成，开始进行提问...\n")
            print("Login completed successfully, starting to ask questions...\n")
            
            # Process each question
            for i, question in enumerate(questions):
                print(f"\nProcessing question {i+1}/{len(questions)}: {question}")
                
                # 尝试多次提问，直到成功或达到最大尝试次数
                success = False
                for attempt in range(1, args.max_retries + 1):
                    if attempt > 1:
                        print(f"Retry attempt {attempt}/{args.max_retries} for question: {question}")
                    
                    if ask_question(driver, question):
                        # Take a screenshot after getting the response
                        take_screenshot(driver)
                        success = True
                        break
                    else:
                        print(f"Failed to ask question, attempt {attempt}/{args.max_retries}")
                        time.sleep(2)  # 短暂等待后重试
                
                if not success:
                    print(f"Failed to ask question after {args.max_retries} attempts: {question}")
                
                # Wait a bit before asking the next question
                if i < len(questions) - 1:
                    wait_seconds = args.wait_time
                    print(f"Waiting {wait_seconds} seconds before next question...")
                    time.sleep(wait_seconds)
        
    finally:
        # Always close the browser when done
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    print("Script execution started")
    main()
    print("Script execution completed") 