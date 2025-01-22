# **Changelog for `setup_env.py`**

## **[1.0.0] - 2025-01-22**

### **Summary**

This initial release of `setup_env.py` provides a comprehensive and user-friendly solution for setting up and managing Python virtual environments across Windows, macOS, and Linux. The script streamlines the environment creation process, ensuring cross-platform compatibility and seamless automation for developers.

### **Key Features**

- **Environment Management**
  - Automatic creation and activation of virtual environments in the `.env/` directory.
  - Customizable environment names with validation to prevent invalid characters.
  - Detection and handling of existing environments to prevent redundant operations.
  - Automatic dependency installation via `requirements.txt`, with informative prompts.

- **Cross-Platform Compatibility**
  - OS detection and tailored environment activation for Windows (CMD/PowerShell), Linux, and macOS.
  - Shell-specific handling to ensure the correct activation script is used.

- **User Experience Enhancements**
  - Prompts to enable automatic activation upon entering the project directory.
  - Intelligent checks for environment activation when the script is run from outside the project directory.
  - Informative output messages to guide the user through the setup process.
  - Clear error handling and validation for command-line arguments.

- **Improved Code Readability**
  - Functions have been refactored with standardized naming conventions to enhance clarity and maintainability.
  - Modularized logic to allow for easier future extensions and improvements.

### **Enhancements & Fixes**
- Root execution prevention to avoid unnecessary security risks, and potential package managment permission conflicts.
- Detailed success/error messages for better troubleshooting.
- Handling of common installation issues such as missing Python3, `pip`, or `venv`.


---

**HISTORY**

---

## **[Unreleased]**

### **Added**
- Initial release of `setup_env.py` script.

---

## **[0.1.0] - 2025-01-22**

### **Added**
- **Core Features:**
  - Detection of operating system (Windows, macOS, Linux).
  - Validation of command-line arguments to allow an optional environment name.
  - Default environment path set to `.env/.FluxCLI`, with support for custom environment names in `.env/<custom_env>`.
  - Automatic virtual environment creation if it doesn't exist.
  - Activation of the virtual environment upon successful creation.
  - Dependency installation via `requirements.txt` if available.

- **Error Handling:**
  - Check for `Python3` installation and exit with an error message if not found.
  - Validation of the environment name to ensure it contains only valid characters.
  - Detection of script execution as root on Linux/macOS with a warning and exit.
  - Proper error messages for failed operations (environment creation, activation, dependency installation).

- **User Interaction:**
  - Prompt to enable automatic activation of the environment when entering the project directory.
  - Prompt to activate the environment when running outside the project directory.
  - Success and error messages for each step of the process.

- **Cross-Platform Compatibility:**
  - Windows shell detection (CMD vs PowerShell) to determine correct activation script.
  - Linux/macOS shell compatibility (`source` command).
  - Handling of paths appropriately for each OS.

---

## **[0.1.0] - 2:10am**

### **Added**
- **Automated Activation Setup:**
  - Added support for automatically activating the environment when entering the project directory.
  - Supports `.bashrc` and `.zshrc` on Linux/macOS.
  - Supports PowerShell profile on Windows.

- **Outside Directory Check:**
  - When running the script outside the project directory, it prompts the user to activate the environment if it exists.

### **Fixed**
- Corrected environment activation commands for PowerShell (`. <path>\Activate.ps1`).
- Improved path handling to work correctly with relative paths.
- Minor bug fixes related to string handling in environment name validation.

---

## **[0.1.0] - 3:05am**

### **Added**
- **Activation Verification:**
  - The script now checks if the environment activation was successful and displays an appropriate success or failure message.

- **Enhanced Logging:**
  - Added more informative `[INFO]`, `[SUCCESS]`, `[ERROR]` messages for better readability and troubleshooting.
  - Introduced timestamped logs for tracking script execution.

### **Changed**
- Default environment directory updated to `.env/.FluxCLI` for better separation of environments.
- Improved argument parsing to provide clearer error messages for invalid inputs.
- Windows activation method enhanced to support both `CMD` and `PowerShell` automatically.

---

## **[0.1.0] - 03:20am**

### **Added**
- **Support for More Shells:**
	  - Support for `fish` shell auto-activation on Linux/macOS.
  - Improved Windows shell detection to include Git Bash.

- **Custom Prompt for Activated Environment:**
  - Adds an environment-specific prompt in the shell after activation.

### **Changed**
- Refactored code for better modularity and readability.
- Improved handling of subprocess calls to prevent shell compatibility issues.

### **Removed**
- Deprecated direct `os.system` calls in favor of `subprocess.run`.

---

## **[1.0.0] - 04-15am**

### **Added**
- **Backup & Restore:**
  - The script now takes a backup of existing environment folders before recreating them.
  - Added an option to restore previous environments in case of accidental deletion.

### **Fixed**
- Compatibility issue with older versions of PowerShell on Windows.
- Proper path resolution for symbolic links in macOS.

---

### **Versioning**

This project follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH), where:

- **MAJOR**: Breaking changes.
- **MINOR**: New features, but backward compatible.
- **PATCH**: Bug fixes and improvements.

---
