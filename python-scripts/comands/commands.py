import os
import sys
import subprocess

# Step 1: Check for virtual environment
if not os.path.exists("venv"):
    subprocess.run(["python", "-m", "venv", "venv"])
    
# Step 2: Activate virtual environment (for Windows)
activate_script = r".\venv\Scripts\activate"
venv_dir = os.path.join(os.getcwd(), "venv")
venv_python = os.path.join(venv_dir, "Scripts", "pip.exe")
subprocess.run(activate_script, shell=True, check=True)

# Step 3: Handle cache directory
project_dir = "project_dir"  # Update this to your project directory
cache_dir = os.path.join(project_dir, "cache_directory")
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Set HF_HOME environment variable
os.environ["HF_HOME"] = cache_dir

# Print Python interpreter
print(f"Python interpreter: {sys.executable}")

# Step 3.1: Install dependencies
subprocess.run([venv_python, "install", "python-dotenv", "huggingface-hub"], shell=True, check=True)

# Step 3.2: Import load_dotenv
from dotenv import load_dotenv
from huggingface_hub import login

# Step 5: Get API Key from .env and use it
load_dotenv()  # Load environment variables from .env
api_key = os.getenv("HF_API_KEY")
if api_key:
    login(api_key)
else:
    print("HF_API_KEY not found in .env.")

# Step 6: Install dependencies
subprocess.run([venv_python, "install", "fastapi[standard]", "gpt4all"], shell=True, check=True)
# subprocess.run(["pip", "install", "-r", "commands\requirements.txt"], shell=True, check=True)

# Step 7: Run the main script
subprocess.run(["python", "main.py"], shell=True, check=True)
