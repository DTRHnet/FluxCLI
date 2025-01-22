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

---


## **Interactive Shell Mode**

When FluxCLI is run without any arguments, it launches into an **interactive shell mode**, providing a REPL-style (Read-Eval-Print Loop) environment for efficient command execution and exploration. This live shell allows users to work within the FluxCLI ecosystem without needing to re-enter the binary for each command, offering a more streamlined and productive workflow.

### **Key Benefits of the Interactive Shell Mode**

1. **Persistent Context:**  
   - FluxCLI retains the state of loaded modules, user-defined variables, and session history, reducing redundancy when executing multiple related commands.
   
2. **Autocomplete Support:**  
   - Commands, options, and module parameters can be auto-completed, making navigation and usage quicker and easier.
   
3. **Enhanced User Experience:**  
   - Custom prompts, colorized outputs, and helpful suggestions provide a more interactive and user-friendly experience.

---

### **Launching the FluxCLI Interactive Shell**

To enter the interactive shell, simply run:

```bash
fluxcli
```

Example output:

```plaintext
Welcome to FluxCLI - Your Simplified CLI Interface
Type 'help' to see available commands.

[ FluxCLI ] > _
```

---

### **Impact on Command Usage**

Once inside the interactive shell, commands are executed **without prefixing `fluxcli`**, providing a more natural command-line experience.

#### **Example Usage (Inside FluxCLI Shell)**

**Traditional CLI Usage (Outside FluxCLI shell):**
```bash
fluxcli load nmap
fluxcli pingsweep 10.0.0.1/24
fluxcli help
```

**Interactive Shell Usage (Inside FluxCLI shell):**
```plaintext
[ FluxCLI ] > load nmap
Module 'nmap' loaded successfully.

[ FluxCLI ] > pingsweep 10.0.0.1/24
{
  "hosts": [
    {
      "ip": "192.168.1.1",
      "hostname": "rabbit.hole.net",
      "mac": "C4:41:1E:0E:70:21"
    }
  ]
}

[ FluxCLI ] > help
Available Commands:
- load <module>
- pingsweep <subnet>
- sysinfo
- exit
```

#### **Command Usage from Outside vs. Inside the Shell**

| Action                          | Outside Shell (`fluxcli <cmd>`) | Inside Shell (`[ FluxCLI ] >`) |
|---------------------------------|--------------------------------|------------------------------|
| Load a module                    | `fluxcli load nmap`             | `load nmap`                   |
| Perform a ping sweep              | `fluxcli pingsweep 10.0.0.1/24`  | `pingsweep 10.0.0.1/24`        |
| View help                         | `fluxcli help`                   | `help`                         |
| Exit                              | `exit`                           | `exit`                         |

---

### **Exit Interactive Shell**

To exit the interactive shell, simply type:

```plaintext
[ FluxCLI ] > exit
```

---

### **Environment Awareness in the Shell**

FluxCLI automatically detects whether it is running inside an active environment and ensures the appropriate modules are loaded and available for execution. If the environment is not activated, the shell will provide a prompt asking whether the user would like to activate it:

```plaintext
[WARNING] You are not in an active FluxCLI environment.
Would you like to activate '.env/.FluxCLI'? (y/n): y
[INFO] FluxCLI environment activated.
```

---

### **Command History and Session Persistence**

The FluxCLI shell maintains a command history within the current session, enabling users to navigate previous commands using the up/down arrow keys.

Example:

```plaintext
[ FluxCLI ] > load nmap
[ FluxCLI ] > pingsweep 10.0.0.1/24
# Pressing the 'up' arrow will recall previous commands
```

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

FluxCLI is built with extendability in mind. Check back soon for more details.
---

## **Native Commands**

Native commands are built directly into FluxCLI and do not require module loading. Examples include:

- `load` - To load a module
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