import os
import sys
import subprocess
import platform

def main():
    # Step 1: Check for virtual environment and create it if necessary
    venv_dir = os.path.join(os.getcwd(), "venv")
    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created.")
    
     # Step 2: Activate virtual environment
    is_windows = platform.system() == "Windows"
    activate_script = os.path.join(venv_dir, "Scripts", "activate") if is_windows else os.path.join(venv_dir, "bin", "activate")
    venv_python = os.path.join(venv_dir, "Scripts", "pip.exe") if is_windows else os.path.join(venv_dir, "bin", "pip")
    
    if not os.path.exists(venv_python):
        print(f"Error: Virtual environment not properly created at {venv_dir}.")
        sys.exit(1)
    
    if is_windows:
        activate_command = rf"{venv_dir}\Scripts\activate"
    else:
        activate_command = f"source {venv_dir}/bin/activate"
    
    # Note: Activating in a subprocess may not propagate to this script's parent process.
    subprocess.run(activate_command, shell=True, check=True)

    # Step 3: Handle cache directory
    project_dir = os.getcwd()  # Update this if needed
    cache_dir = os.path.join(project_dir, "cache_directory")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        print("Cache directory created.")
    
    # Set HF_HOME environment variable
    os.environ["HF_HOME"] = cache_dir

    # Step 4: Install essential dependencies
    dependencies = ["python-dotenv", "huggingface-hub", "transformers", "datasets", "fastapi[standard]", "torch", "protobuf" ,"uvicorn", "scikit-learn"]
    subprocess.run([venv_python, "install", *dependencies], shell=True, check=True)
    
    # Step 5: Import necessary modules
    # try:
    #     from dotenv import load_dotenv
    #     from huggingface_hub import login
    # except ImportError as e:
    #     print("Error: Required module not found after installation:", str(e))
    
    # # Step 6: Load API Key and login
    # load_dotenv()  # Load environment variables from .env
    # api_key = os.getenv("HF_API_KEY")
    # if api_key:
    #     login(api_key)
    #     print("Logged into Hugging Face.")
    # else:
    #     print("HF_API_KEY not found in .env. Please add it to proceed.")
    #     sys.exit(1)
    
    print("Setup complete. You are now ready to use the application.")


if __name__ == "__main__":
    main()