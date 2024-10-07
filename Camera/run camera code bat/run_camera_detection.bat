@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

:: Check if OpenCV (cv2) is installed
python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo OpenCV not found. Installing OpenCV...
    python -m pip install opencv-python
    if %errorlevel% neq 0 (
        echo OpenCV installation failed. Please check your internet connection or pip installation.
        pause
        exit /b
    )
    echo OpenCV successfully installed.
)

:: After successful installation, reset the error level
python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install OpenCV after retrying. Exiting...
    pause
    exit /b
)

:: Run your Python script
python camera.py

pause

