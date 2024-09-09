cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
curl -L -O https://github.com/ultraleap/leapc-python-bindings/archive/refs/heads/main.zip
tar -xf main.zip
del main.zip
python -m pip install --upgrade pip
pip install -r requirements.txt
ren leapc-python-bindings-main leapc
python -m build .\leapc\leapc-cffi
pip install .\leapc\leapc-cffi\dist\leapc_cffi-0.0.1.tar.gz
pip install .\leapc\leapc-python-api
echo Initialisation complete. Run 'start.bat' to start the application.
pause