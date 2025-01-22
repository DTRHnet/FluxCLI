import os
import sys
import subprocess
import platform
import re
import shutil

# Default environment paths
_ENV_ROOT_ = ".env"
_DEFAULT_ENV_ = os.path.join(_ENV_ROOT_, ".FluxCLI")

# Get the current operating system
def getOperatingSystem():
    sSystemName = platform.system().lower()
    if "windows" in sSystemName:
        return "win"
    elif "darwin" in sSystemName:
        return "osx"
    elif "linux" in sSystemName:
        return "linux"
    else:
        print("[ERROR] Unsupported operating system:", sSystemName)
        sys.exit(1)

_OS_ = getOperatingSystem()

# Validate environment name
def isValidEnvName(sEnvName):
    sPattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(sPattern, sEnvName))

# Handle arguments and set environment name
def getEnvironmentName():
    if len(sys.argv) == 1:
        return _DEFAULT_ENV_  # No argument passed, use default
    elif len(sys.argv) == 2:
        sCustomEnv = os.path.join(_ENV_ROOT_, sys.argv[1])
        if not isValidEnvName(sys.argv[1]):
            print(f"[ERROR] Invalid environment name '{sys.argv[1]}'. Use only letters, numbers, '-', '_', and '.'.")
            sys.exit(1)
        return sCustomEnv
    else:
        print("[ERROR] Too many arguments. Usage: python setup_env.py [env_name]")
        sys.exit(1)

_ENV_ = getEnvironmentName()

# Determine the correct activation script based on OS and shell
def getShell():
    if _OS_ == "win":
        sParentProcess = os.environ.get("ComSpec", "").lower()
        if "cmd.exe" in sParentProcess:
            return "cmd"
        elif "powershell.exe" in sParentProcess:
            return "powershell"
        else:
            return "unknown"
    else:
        return "unix"

def getActivationScript():
    sEnvPath = os.path.abspath(_ENV_)
    sShellType = getShell()
    if _OS_ == "win":
        if sShellType == "cmd":
            return os.path.join(sEnvPath, "Scripts", "activate.bat")
        elif sShellType == "powershell":
            return os.path.join(sEnvPath, "Scripts", "Activate.ps1")
        else:
            print("[ERROR] Unsupported Windows shell. Please run in CMD or PowerShell.")
            sys.exit(1)
    elif _OS_ in ["osx", "linux"]:
        return os.path.join(sEnvPath, "bin", "activate")

# Ensure the script is not run as root (Linux/Mac)
def checkRootPrivileges():
    if _OS_ in ["linux", "osx"] and os.geteuid() == 0:
        print("[ERROR] Do not run this script as root! It may break package installations.")
        sys.exit(1)

# Check if Python3 is installed
def checkPythonInstallation():
    if shutil.which("python3") is None:
        print("[ERROR] Python3 is not installed. Please install Python3 and try again.")
        sys.exit(1)

# Create virtual environment if it doesn't exist
def createVirtualEnvironment():
    if os.path.exists(_ENV_):
        print(f"[INFO] Virtual environment '{_ENV_}' already exists. Skipping creation.")
    else:
        print(f"[INFO] Creating virtual environment '{_ENV_}'...")
        os.makedirs(_ENV_ROOT_, exist_ok=True)
        subprocess.run(["python3", "-m", "venv", _ENV_], check=True)
        print(f"[SUCCESS] Virtual environment '{_ENV_}' created successfully.")

# Activate the virtual environment and verify success
def activateVirtualEnvironment():
    sActivationScript = getActivationScript()
    if _OS_ == "win":
        sCommand = f'cmd /c "{sActivationScript} && echo FluxCLI environment loaded successfully"'
    else:
        sCommand = f'source {sActivationScript} && echo FluxCLI environment loaded successfully'
    
    result = subprocess.run(sCommand, shell=True)
    if result.returncode != 0:
        print("[ERROR] Failed to activate the environment.")
        sys.exit(1)
    print("[SUCCESS] FluxCLI environment loaded successfully.")

# Offer auto-activation setup
def setupAutoActivation():
    bResponse = input("[PROMPT] Do you want to enable automatic activation of the environment when entering the project directory? (y/n): ").strip().lower()
    if bResponse == 'y':
        if _OS_ in ["linux", "osx"]:
            sRcFile = os.path.expanduser("~/.bashrc")
            sActivationLine = f'source {os.path.abspath(getActivationScript())}'
            with open(sRcFile, "a") as f:
                f.write(f"\n# Auto-activate FluxCLI\ncd $(pwd) && {sActivationLine}\n")
            print(f"[INFO] Added auto-activation to {sRcFile}. Restart your shell to take effect.")
        elif _OS_ == "win":
            sPowershellProfile = os.path.expanduser("~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1")
            with open(sPowershellProfile, "a") as f:
                f.write(f"\n# Auto-activate FluxCLI\ncd $(pwd); & {getActivationScript()}\n")
            print(f"[INFO] Added auto-activation to PowerShell profile. Restart PowerShell to take effect.")
    else:
        print("[INFO] Skipping automatic activation setup.")

# Check and prompt outside environment
def checkAndPromptOutsideProject():
    sCurrentDir = os.getcwd()
    sProjectDir = os.path.abspath(os.path.dirname(__file__))
    if sCurrentDir != sProjectDir and os.path.exists(_DEFAULT_ENV_):
        bResponse = input("[PROMPT] You are outside the project folder. Do you want to activate FluxCLI environment? (y/n): ").strip().lower()
        if bResponse == 'y':
            activateVirtualEnvironment()
        else:
            print("[INFO] Skipping environment activation.")

# Install dependencies
def installDependencies():
    sReqFile = "requirements.txt"
    if os.path.exists(sReqFile):
        subprocess.run([os.path.join(_ENV_, "bin" if _OS_ != "win" else "Scripts", "python"), "-m", "pip", "install", "-r", sReqFile], check=True)
        print("[SUCCESS] Dependencies installed successfully.")
    else:
        print("[WARNING] No requirements.txt found. Skipping dependency installation.")

# Main function to orchestrate setup
def main():
    checkRootPrivileges()
    checkPythonInstallation()
    createVirtualEnvironment()
    activateVirtualEnvironment()
    installDependencies()
    setupAutoActivation()
    checkAndPromptOutsideProject()
    print("[SUCCESS] Environment is ready to use!")

if __name__ == "__main__":
    main()
