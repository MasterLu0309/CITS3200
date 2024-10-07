import os
import subprocess
import urllib.request
import zipfile
import shutil
import sys
import time

def download_with_progress(url, filename, retries=3):
    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        print(f"\rDownloading {filename}... {percent}%", end="")
    
    for attempt in range(retries):
        try:
            urllib.request.urlretrieve(url, filename, reporthook)
            print()
            return
        except Exception as e:
            print(f"\nFailed to download {filename}: {e}")
            if attempt < retries - 1:
                print(f"Retrying... ({attempt + 1}/{retries})")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("Exceeded maximum retries. Exiting.")
                sys.exit(1)

def run_command(command, error_message):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        input("Press Enter to continue...")
        sys.exit(1)

# Change to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Download Winpython installer
winpython_url = "https://github.com/winpython/winpython/releases/download/7.1.20240203final/Winpython64-3.11.8.0.exe"
winpython_installer = "Winpython64-3.11.8.0.exe"
download_with_progress(winpython_url, winpython_installer)
time.sleep(3)

# Run the Winpython installer
print("Installing Winpython version 3.11.8 (this can take a while!)")
run_command([winpython_installer, '-y'], "Failed to install Winpython.")

# Create a virtual environment
print("Creating virtual environment...")
venv_path = os.path.join(os.getcwd(), "venv")
python_exe = os.path.join(os.getcwd(), "WPy64-31180", "python-3.11.8.amd64", "python.exe")
run_command([python_exe, '-m', 'venv', venv_path], "Failed to create virtual environment.")

# Activate the virtual environment
activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
run_command([activate_script], "Failed to activate virtual environment.")

# Delete the Winpython installer
try:
    os.remove(winpython_installer)
except Exception as e:
    print(f"Failed to delete Winpython installer: {e}")
    input("Press Enter to continue...")
    sys.exit(1)

# Download LeapC Python bindings
leapc_url = "https://github.com/ultraleap/leapc-python-bindings/archive/refs/heads/main.zip"
leapc_zip = "main.zip"
download_with_progress(leapc_url, leapc_zip)

# Extract the LeapC Python bindings
print("Extracting LeapC Python bindings...")
try:
    with zipfile.ZipFile(leapc_zip, 'r') as zip_ref:
        zip_ref.extractall()
except Exception as e:
    print(f"Failed to extract LeapC Python bindings: {e}")
    input("Press Enter to continue...")
    sys.exit(1)

# Delete the zip file
try:
    os.remove(leapc_zip)
except Exception as e:
    print(f"Failed to delete LeapC Python bindings zip file: {e}")
    input("Press Enter to continue...")
    sys.exit(1)

# Install required packages
run_command([os.path.join(venv_path, "Scripts", "python.exe"),'-m', 'pip', 'install', '-r', 'requirements.txt'], "Failed to install required packages.")

# Rename the extracted directory
try:
    os.rename("leapc-python-bindings-main", "leapc")
except Exception as e:
    print(f"Failed to rename LeapC Python bindings directory: {e}")
    input("Press Enter to continue...")
    sys.exit(1)

# Build the leapc-cffi package
run_command([os.path.join(venv_path, "Scripts", "python"), '-m', 'build', './leapc/leapc-cffi'], "Failed to build leapc-cffi package.")

# Install the built package
run_command([os.path.join(venv_path, "Scripts", "pip"), 'install', './leapc/leapc-cffi/dist/leapc_cffi-0.0.1.tar.gz'], "Failed to install leapc-cffi package.")

# Install the leapc-python-api package
run_command([os.path.join(venv_path, "Scripts", "pip"), 'install', './leapc/leapc-python-api'], "Failed to install leapc-python-api package.")

print("Initialisation complete. Run 'start.py' to start the application.")
input("Press Enter to continue...")
