import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

print("浏览器启动测试脚本")
print("=============================================")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

try:
    print("\n1. 检查ChromeDriver...")
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    if os.path.exists(chromedriver_path):
        print(f"ChromeDriver存在: {chromedriver_path}")
    else:
        print(f"错误: ChromeDriver不存在: {chromedriver_path}")
        sys.exit(1)
    
    print("\n2. 设置Chrome选项...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # 取消下面的注释以查看更多调试信息
    # chrome_options.add_argument("--verbose")
    # chrome_options.add_argument("--log-level=0")
    
    print("\n3. 创建Chrome服务...")
    service = Service(executable_path=chromedriver_path)
    
    print("\n4. 尝试启动浏览器...")
    print("如果长时间无响应，可能是ChromeDriver与Chrome版本不匹配")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("\n5. 浏览器已成功启动!")
    print("正在访问百度...")
    driver.get("https://www.baidu.com")
    
    print("\n6. 等待5秒...")
    time.sleep(5)
    
    print("\n7. 关闭浏览器...")
    driver.quit()
    
    print("\n测试成功完成!")
    
except Exception as e:
    print(f"\n错误: {str(e)}")
    print("\n详细错误信息:")
    import traceback
    traceback.print_exc()
    
input("\n按Enter键退出...") 