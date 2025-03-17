import os
import sys
import re
import subprocess
import requests
import zipfile
import shutil
from io import BytesIO

def get_chrome_version():
    """获取Chrome浏览器版本"""
    print("正在检查Chrome浏览器版本...")
    
    # Windows系统
    if sys.platform.startswith('win'):
        try:
            # 尝试从注册表获取版本
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            version, _ = winreg.QueryValueEx(key, 'version')
            print(f"从注册表获取的Chrome版本: {version}")
            return version
        except:
            # 如果注册表方法失败，尝试从安装路径获取
            try:
                paths = [
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                    os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
                ]
                
                for path in paths:
                    if os.path.exists(path):
                        print(f"找到Chrome安装路径: {path}")
                        # 使用wmic获取版本信息
                        output = subprocess.check_output(
                            f'wmic datafile where name="{path.replace("\\", "\\\\")}" get Version /value',
                            shell=True
                        ).decode('utf-8')
                        version_match = re.search(r'Version=(.+)', output)
                        if version_match:
                            version = version_match.group(1).strip()
                            print(f"从文件属性获取的Chrome版本: {version}")
                            return version
            except Exception as e:
                print(f"从文件属性获取Chrome版本失败: {str(e)}")
    
    # 尝试通过命令行获取
    try:
        if sys.platform.startswith('win'):
            cmd = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --version'
            alt_cmd = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --version'
            try:
                output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            except:
                output = subprocess.check_output(alt_cmd, shell=True).decode('utf-8')
        elif sys.platform.startswith('darwin'):  # macOS
            cmd = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        else:  # Linux
            cmd = 'google-chrome --version'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        
        match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', output)
        if match:
            version = match.group(1)
            print(f"从命令行获取的Chrome版本: {version}")
            return version
    except Exception as e:
        print(f"从命令行获取Chrome版本失败: {str(e)}")
    
    print("无法获取Chrome版本，将使用默认版本")
    return None

def get_chromedriver_url(chrome_version):
    """根据Chrome版本获取对应的ChromeDriver下载URL"""
    if not chrome_version:
        print("未提供Chrome版本，将下载最新的ChromeDriver")
        chrome_version = "latest"
    
    # 提取主版本号
    major_version = chrome_version.split('.')[0]
    print(f"Chrome主版本号: {major_version}")
    
    # 根据Chrome版本确定ChromeDriver版本
    try:
        if major_version == "latest":
            # 获取最新版本
            response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
            version = response.text.strip()
        else:
            # 获取对应版本
            response = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}")
            version = response.text.strip()
        
        print(f"匹配的ChromeDriver版本: {version}")
        
        # 确定平台
        platform = 'win32'
        if sys.platform.startswith('linux'):
            platform = 'linux64'
        elif sys.platform.startswith('darwin'):
            platform = 'mac64'
        
        # 构建下载URL
        url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform}.zip"
        print(f"ChromeDriver下载URL: {url}")
        return url
    except Exception as e:
        print(f"获取ChromeDriver URL失败: {str(e)}")
        # 使用备用URL (Chrome 114版本)
        backup_url = "https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/win32/chromedriver-win32.zip"
        print(f"使用备用URL: {backup_url}")
        return backup_url

def download_chromedriver(url):
    """下载并解压ChromeDriver"""
    print(f"正在从 {url} 下载ChromeDriver...")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"下载失败，状态码: {response.status_code}")
            return False
        
        # 解压ZIP文件
        print("下载完成，正在解压...")
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            # 查找chromedriver.exe文件
            for file in zip_file.namelist():
                if file.endswith('chromedriver.exe') or file.endswith('chromedriver'):
                    # 提取文件
                    source = zip_file.open(file)
                    target = open("chromedriver.exe", "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
                    print(f"已解压并保存为 chromedriver.exe")
                    return True
        
        print("ZIP文件中未找到ChromeDriver")
        return False
    except Exception as e:
        print(f"下载或解压失败: {str(e)}")
        return False

def main():
    print("ChromeDriver版本检查和下载工具")
    print("=============================================")
    
    # 检查是否已存在ChromeDriver
    if os.path.exists("chromedriver.exe"):
        print("发现现有的ChromeDriver.exe")
        choice = input("是否要重新下载? (y/n): ").lower()
        if choice != 'y':
            print("保留现有的ChromeDriver")
            return
    
    # 获取Chrome版本
    chrome_version = get_chrome_version()
    
    # 获取下载URL
    url = get_chromedriver_url(chrome_version)
    
    # 下载ChromeDriver
    if download_chromedriver(url):
        print("ChromeDriver下载和安装成功!")
    else:
        print("ChromeDriver下载或安装失败!")
        
        # 尝试备用下载方法
        print("\n尝试备用下载方法...")
        try:
            print("使用PowerShell下载...")
            backup_url = "https://storage.googleapis.com/chrome-for-testing-public/114.0.5735.90/win32/chromedriver-win32.zip"
            ps_command = f'powershell -Command "& {{Invoke-WebRequest -Uri \'{backup_url}\' -OutFile \'chromedriver.zip\'}}"'
            subprocess.run(ps_command, shell=True, check=True)
            
            print("解压文件...")
            with zipfile.ZipFile("chromedriver.zip") as zip_file:
                for file in zip_file.namelist():
                    if file.endswith('chromedriver.exe'):
                        source = zip_file.open(file)
                        target = open("chromedriver.exe", "wb")
                        with source, target:
                            shutil.copyfileobj(source, target)
                        print("备用方法成功!")
                        return
            
            print("备用方法未找到chromedriver.exe")
        except Exception as e:
            print(f"备用方法失败: {str(e)}")

if __name__ == "__main__":
    main()
    input("\n按Enter键退出...") 