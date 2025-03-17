import os
import sys
import requests
import zipfile
import io
import platform
import subprocess
import re

def get_chrome_version():
    """Get the installed Chrome version."""
    print("Detecting Chrome version...")
    
    system = platform.system()
    if system == "Windows":
        try:
            # Try to get Chrome version using registry
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            winreg.CloseKey(key)
            print(f"Detected Chrome version: {version}")
            return version
        except:
            # If registry method fails, try using the Chrome executable
            try:
                output = subprocess.check_output(
                    ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                    stderr=subprocess.STDOUT
                )
                version = re.search(r'version\s+REG_SZ\s+([\d\.]+)', output.decode('utf-8')).group(1)
                print(f"Detected Chrome version: {version}")
                return version
            except:
                print("Could not detect Chrome version. Using latest ChromeDriver.")
                return None
    elif system == "Darwin":  # macOS
        try:
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                stdout=subprocess.PIPE
            )
            version = process.communicate()[0].decode('UTF-8').replace('Google Chrome ', '').strip()
            print(f"Detected Chrome version: {version}")
            return version
        except:
            print("Could not detect Chrome version. Using latest ChromeDriver.")
            return None
    elif system == "Linux":
        try:
            process = subprocess.Popen(
                ['google-chrome', '--version'],
                stdout=subprocess.PIPE
            )
            version = process.communicate()[0].decode('UTF-8').replace('Google Chrome ', '').strip()
            print(f"Detected Chrome version: {version}")
            return version
        except:
            print("Could not detect Chrome version. Using latest ChromeDriver.")
            return None
    
    return None

def download_chromedriver():
    """Download the appropriate ChromeDriver for the current platform and Chrome version."""
    print("Downloading ChromeDriver...")
    
    # Determine the platform
    system = platform.system()
    if system == "Windows":
        platform_name = "win32"
    elif system == "Darwin":
        platform_name = "mac64"
    elif system == "Linux":
        platform_name = "linux64"
    else:
        print(f"Unsupported platform: {system}")
        return False
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    
    # Get the major version
    if chrome_version:
        major_version = chrome_version.split('.')[0]
    else:
        major_version = None
    
    # Get the appropriate ChromeDriver version
    try:
        if major_version and int(major_version) >= 115:
            # For Chrome 115+, use the Chrome for Testing JSON API
            print(f"Using Chrome for Testing API for Chrome {major_version}+")
            response = requests.get(f"https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
            data = response.json()
            
            # Find the latest version for the major version
            matching_versions = []
            for version_info in data["versions"]:
                if version_info["version"].startswith(f"{major_version}."):
                    matching_versions.append(version_info)
            
            if not matching_versions:
                print(f"No matching ChromeDriver found for Chrome {major_version}. Using latest version.")
                response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
                version = response.text.strip()
                url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform_name}.zip"
            else:
                # Sort by version and get the latest
                matching_versions.sort(key=lambda x: [int(part) for part in x["version"].split('.')])
                latest_version_info = matching_versions[-1]
                
                # Find the chromedriver download for this platform
                chromedriver_download = None
                for download in latest_version_info["downloads"].get("chromedriver", []):
                    if download["platform"] == platform_name:
                        chromedriver_download = download
                        break
                
                if not chromedriver_download:
                    print(f"No ChromeDriver download found for platform {platform_name}. Using latest version.")
                    response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
                    version = response.text.strip()
                    url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform_name}.zip"
                else:
                    url = chromedriver_download["url"]
                    version = latest_version_info["version"]
        else:
            # For Chrome 114 and below, use the old method
            if major_version:
                response = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}")
                version = response.text.strip()
            else:
                response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
                version = response.text.strip()
            
            url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform_name}.zip"
        
        print(f"Using ChromeDriver version: {version}")
        print(f"Downloading from: {url}")
        
        # Download the ChromeDriver
        response = requests.get(url)
        
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Extract all files to the current directory
            zip_file.extractall()
        
        # Make the ChromeDriver executable on Unix-like systems
        if system != "Windows":
            os.chmod("chromedriver", 0o755)
            
        print("ChromeDriver downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return False

if __name__ == "__main__":
    if download_chromedriver():
        print("ChromeDriver is ready to use")
    else:
        print("Failed to download ChromeDriver")
        sys.exit(1) 