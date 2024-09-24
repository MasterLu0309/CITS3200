cd /d %~dp0
curl -L -O https://github.com/winpython/winpython/releases/download/7.1.20240203final/Winpython64-3.11.8.0.exe
echo Installing Winpython version 3.11.8 (this can take a while!)
start /b /wait Winpython64-3.11.8.0.exe -y
%~dp0\WPy64-31180\python-3.11.8.amd64\python.exe -m venv venv
call venv\Scripts\activate
del Winpython64-3.11.8.0.exe
curl -L -O https://github.com/ultraleap/leapc-python-bindings/archive/refs/heads/main.zip
tar -xf main.zip
del main.zip
%~dp0\WPy64-31180\python-3.11.8.amd64\python.exe -m pip install --upgrade pip
pip install -r requirements.txt
ren leapc-python-bindings-main leapc
python -m build .\leapc\leapc-cffi
pip install .\leapc\leapc-cffi\dist\leapc_cffi-0.0.1.tar.gz
pip install .\leapc\leapc-python-api
echo Initialisation complete. Run 'start.bat' to start the application.
pause