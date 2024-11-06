# Project Commands

## Setup Commands

These commands are used to configure your environment and install necessary dependencies to run the project.

### 1. Configure Git Credentials

Store your Git credentials globally to avoid repeated prompts.

```bash
git config --global credential.helper store
```

### 2. Hugging Face CLI Operations

Log in to Hugging Face, verify your account, and log out when necessary.

```bash
# Log in to Hugging Face
huggingface-cli login

# Verify your Hugging Face account
huggingface-cli whoami

# Log out from Hugging Face
huggingface-cli logout
```

### 3. Install PyTorch

Install PyTorch with CUDA 11.8 support for GPU acceleration.

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 4. Install Project Dependencies

Install all required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Update `requirements.txt`

Freeze the specific versions of essential packages to ensure consistency across environments.

```bash
pip freeze | findstr "huggingface_hub transformers accelerate Flask fastapi uvicorn" > requirements.txt
```

### 6. Set Flask Application Environment Variable

Specify the main Flask application file.

```powershell
$env:FLASK_APP = "main.py"
```

---

## Post-Setup Commands

After completing the setup, use the following commands to activate the virtual environment, set environment variables, and run the Flask application.

### 1. Activate Virtual Environment

Activate your project's virtual environment to ensure all dependencies are correctly referenced.

```powershell
.\venv\Scripts\activate
```

*Note: If you're using a different shell or operating system, the activation command might vary.*

### 2. Set Hugging Face Cache Directory

Specify a custom cache directory for Hugging Face to manage model files and other assets.

```powershell
$env:HF_HOME = "D:\your_cache_directory"
```

### 3. Run the Flask Application

Start the Flask server to run your application.

```bash
flask --app main run
```

*Alternatively, you can use:*

```bash
flask run
```

*Ensure that the `FLASK_APP` environment variable is correctly set to `main.py` as shown in the setup commands.*

---

## Additional Tips

- **Virtual Environment**: Always ensure that your virtual environment is activated before running or installing packages to maintain project dependencies isolated.
  
- **Environment Variables**: Consider adding environment variables to a `.env` file and using tools like `python-dotenv` to manage them more efficiently.

- **Performance Optimization**: If you encounter performance issues, revisit the optimization steps or consult the project's documentation for further guidance.