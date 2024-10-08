import os
import subprocess

# Change to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Command to activate the virtual environment and run main.py in the same session
command = ' && '.join([
    'call venv\\Scripts\\activate',
    'python main.py'
])

# Execute the command
subprocess.call(command, shell=True)
