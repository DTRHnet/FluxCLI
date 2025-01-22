# **FluxCLI: A Modern Approach to Simplified Command Execution**

FluxCLI is a high-level, cross-platform command-line interface designed to simplify complex operations by wrapping and enhancing existing tools such as **Nmap**, **tmux**, and more. It provides an intuitive and consistent interface that structures output in a standardized format, making it easy to consume, pipe, and integrate into scripts and applications.

---

## **Background and Evolution**

FluxCLI was born from the need to simplify intricate command-line workflows without sacrificing flexibility. It is the modern successor to **DtRH-Bashlib**, an earlier POSIX-compliant library designed with similar goals. While DtRH-Bashlib was limited to Unix-like environments and required extensive manual scripting, FluxCLI leverages Python’s cross-platform capabilities to provide an extensible and user-friendly solution that works seamlessly across **Windows, macOS, and Linux**.

---

## **Key Features**

- **Simplified Command Execution:**  
  - Complex commands are abstracted into high-level, easy-to-use functions.
  - Advanced users can still access full parameter customization when needed.

- **Standardized Output Structure:**  
  - Outputs are structured into universal data types (e.g., JSON), making them easy to process, store, and transmit.
  - This ensures uniformity across different modules and allows seamless integration with other tools and programming languages.

- **Cross-Platform Compatibility:**  
  - Developed from the ground up to work on **Windows (CMD/PowerShell), macOS, and Linux**.
  - Uses intelligent shell detection to ensure the correct commands and activation methods are applied.

- **Modular Design:**  
  - Core functionality is extended via dynamically loadable **modules**, allowing users to expand capabilities without modifying the core framework.
  - A flexible API for creating custom modules.

- **Automatic Environment Management:**  
  - Virtual environments are automatically created and activated, reducing setup complexity.
  - Users can opt for automatic environment activation when entering project directories.

---

## **Example: Simplifying Nmap's Pingsweep**

Using raw Nmap commands can be cumbersome and verbose:

```bash
nmap -sn 192.168.1.0/24
```

Typical output:

```
Nmap scan report for rabbit.hole.net (192.168.1.1)
Host is up (0.0010s latency).
MAC Address: C4:41:1E:0E:70:21 (Belkin International)
```

### **Conventional Approach Using Regex Filtering**

Without FluxCLI, filtering this output requires multiple commands:

```bash
REGEX='Nmap scan report for ([^ ]+) \(([^)]+)\).*MAC Address: ([^ ]+)'
nmap -sn 10.0.0.1/24 | grep -Eo "$REGEX" | awk -v r="$REGEX" 'match($0, r, arr) {print "{\"ip\":\"" arr[2] "\",\"hostname\":\"" arr[1] "\",\"mac\":\"" arr[3] "\"}"}' | jq -s '{hosts: .}'
```

Result:

```json
{
  "hosts": [
    {
      "ip": "192.168.1.1",
      "hostname": "rabbit.hole.net",
      "mac": "C4:41:1E:0E:70:21"
    }
  ]
}
```

### **FluxCLI's Approach**

FluxCLI simplifies this entire process into a single command:

```bash
[ FluxCLI ] > pingsweep 10.0.0.1/24
```

Result:

```json
{
  "hosts": [
    {
      "ip": "192.168.1.1",
      "hostname": "rabbit.hole.net",
      "mac": "C4:41:1E:0E:70:21"
    }
  ]
}
```

### **Advantages:**

- **Data Standardization:** Output is structured in JSON, making it easier to work with in scripts and applications.
- **Reduced Redundancy:** Strips unnecessary details and presents only relevant information.
- **Interoperability:** The data can be easily converted to other formats like CSV, YAML, or directly integrated into databases.
- **Simplicity:** Users don't need to remember complex flags; FluxCLI handles the internals.

---

## **Installation**

### **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)

### **Installation Steps**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fluxcli.git
   cd fluxcli
   ```

2. NOTE: Check the **'docs/setup_env.md'** file for detailed information about auto triggering the python environment. Run the environment setup script. If you want a custom environment name, provide it as the first and only argument:

   ```bash
   python3 setup_env.py              # Defaults to environment named '.Flex-Env', in the '.env/' folder
   python3 setup_env.py custom_env   # Will generate the environment in '.env/custom_env/'
   ```

3. The environment should auto activate. But if it doesnt, below lists the activation scripts by OS.

   - **Linux/macOS:**  
     ```bash
     source .env/.FluxCLI/bin/activate
     ```
   - **Windows PowerShell:**  
     ```powershell
     .\.env\.FluxCLI\Scripts\Activate.ps1
     ```
   - **Windows CMD:**  
     ```cmd
     .env\.FluxCLI\Scripts\activate.bat
     ```


4. Install dependencies:

   ```bash
   fluxcli getDeps
   ```

---

## **Usage Examples**

### **Basic Commands**

- **List available modules:**

  ```bash
  fluxcli list-modules
  ```

- **Load the Nmap module and run a command:**

  ```bash
  fluxcli load nmap
  fluxcli pingsweep 10.0.0.1/24
  ```

- **Native commands (built into FluxCLI):**

  ```bash
  fluxcli sysinfo
  ```

---

## **Building a Module**

FluxCLI’s modular architecture allows easy extension through the creation of custom modules.

### **Module Structure**

Each module resides under the `fluxcli/modules/` directory:

```
fluxcli/modules/
├── nmap/
│   ├── __init__.py
│   ├── module.py
│   └── commands.yaml
```

### **Steps to Create a New Module**

TODO : FluxCLI is designed with extensibility in mind. Check back soon for more details.
---

## **Native Commands**

Native commands are built directly into FluxCLI and do not require module loading. Examples include:

- `sysinfo` – Displays system information.
- `version` – Prints the current version of FluxCLI.
- `help` – Lists all available commands.

---

## **Configuration**

FluxCLI stores user settings in:

- **Linux/macOS:** `~/.fluxcli/fluxcli.yaml`
- **Windows:** `%APPDATA%\FluxCLI\fluxcli.yaml`

You can customize:

- Default environment name 
- Shell preferences {prompt colors, configurations}
- Output formats {json, csv, raw}

---

## **Contributing**

At the moment, I am not looking for contributions to the main repo, but this will change once this project has taken off a bit. With that said, feel free to fork the repository, use/reuse/republish anything here. I only ask credit be given where it is due.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request with a clear description.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
