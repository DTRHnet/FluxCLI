# **Changelog for FluxCLI**

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## **[0.1.0] - 2025-01-22** *(Broken)*

### **Overview**

This is the initial pre-release version of FluxCLI, representing the groundwork for a modern command-line interface that simplifies complex command execution. However, this version is currently tagged as **broken**, and significant fixes are planned for the first major release.

### **Added**

- **Core Functionality:**
  - Command-line interface to wrap and simplify tools such as Nmap.
  - Automatic environment management using Python virtual environments.
  - Cross-platform support for Windows (CMD/PowerShell), Linux, and macOS.
  - JSON-formatted output for structured and easily consumable results.

- **Modules System:**
  - Initial support for dynamically loadable modules (e.g., `nmap` module for network scanning).
  - YAML-based command registration for extendability.

- **Command Execution Features:**
  - Simplified wrapper for commands like `pingsweep`, reducing redundant CLI flags.
  - Standardized data output to JSON for better interoperability with other tools.

- **Automation and Ease of Use:**
  - Automatic activation of virtual environments when entering the project directory.
  - User prompts to guide through environment setup and usage.
  - Basic dependency installation via `requirements.txt`.

### **Fixed**

- N/A (Initial release, no prior versions).

### **Known Issues / Broken Features**

- **Inconsistent Activation:**  
  - Environment activation may fail under certain shells (especially on Windows PowerShell).  
  - Fix planned for better shell detection and activation script handling.

- **Module Loading Bugs:**  
  - Some modules fail to load dynamically due to incorrect command mappings.  
  - Module registry improvements planned for the next release.

- **Dependency Management:**  
  - `requirements.txt` is not being handled correctly in some environments.  
  - Fix planned to ensure robust dependency handling.

- **Error Handling and Logging:**  
  - Poor error messages for failed activations and module loading.  
  - Improvements to error handling will be introduced in the next release.

- **Cross-Platform Issues:**  
  - Inconsistent path handling across different OS platforms.
  - Planned fixes include better OS detection and path resolution logic.

---

## **[0.2.0] - Upcoming (Planned Fixes)**

### **Planned Fixes and Improvements**

- **Environment Activation Fixes:**
  - Reliable activation across Windows CMD, PowerShell, and Linux/macOS shells.
  - Improved detection of shell environment and auto-activation configuration.

- **Enhanced Error Handling:**
  - Detailed logging for troubleshooting failed commands and misconfigurations.
  - Better validation for module loading and command execution.

- **Improved Module Management:**
  - Unified command registry to allow for dynamic loading and help messages.
  - Additional modules planned (e.g., `tmux` integration).

- **Performance Optimizations:**
  - More efficient command parsing and execution to reduce processing overhead.
  - Parallel execution where applicable.

---

## **[1.0.0] - Upcoming (Stable Release)**

- The first major release of FluxCLI will include all planned fixes, refinements, and feature enhancements, making it fully stable and production-ready.

---

## **How to Contribute**

If you'd like to contribute to fixing the broken aspects of FluxCLI, please check the open issues or submit a pull request with proposed changes.

---

## **Versioning**

FluxCLI follows [Semantic Versioning](https://semver.org/), using the following structure:

- **MAJOR:** Breaking changes, major improvements.
- **MINOR:** New features, backwards-compatible improvements.
- **PATCH:** Bug fixes and minor enhancements.

---

## **License**

FluxCLI is licensed under the MIT License. See the `LICENSE` file for details.

---

Stay tuned for further updates and improvements as we work toward the stable 1.0.0 release!