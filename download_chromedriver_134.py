import os
import sys
import requests
import zipfile
import io

def download_chromedriver_134():
    """Download ChromeDriver 134 for Windows."""
    print("Downloading ChromeDriver 134 for Windows...")
    
    # Direct URL for ChromeDriver 134 for Windows
    url = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.15/win32/chromedriver-win32.zip"
    
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url)
        
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Extract all files to the current directory
            zip_file.extractall()
        
        # The ChromeDriver is in a subdirectory, move it to the current directory
        chromedriver_path = os.path.join("chromedriver-win32", "chromedriver.exe")
        if os.path.exists(chromedriver_path):
            # If chromedriver.exe already exists in the current directory, remove it
            if os.path.exists("chromedriver.exe"):
                os.remove("chromedriver.exe")
            
            # Move the chromedriver.exe to the current directory
            import shutil
            shutil.move(chromedriver_path, "chromedriver.exe")
            
            # Remove the extracted directory
            shutil.rmtree("chromedriver-win32")
            
        print("ChromeDriver downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return False

if __name__ == "__main__":
    if download_chromedriver_134():
        print("ChromeDriver is ready to use")
    else:
        print("Failed to download ChromeDriver")
        sys.exit(1) 