# ${ROOT}/FluxCLI/FluxCLI.py
# --> CLI Prompt Entry Point
#
# 1. Discovers available modules.
# 2. Loads each module’s commands.
# 3. Builds a command registry.
# 4. Implements a REPL (interactive mode) if no arguments are given.
# 5. Accepts direct command usage if arguments are provided (e.g. fluxcli nmap pingsweep 192.168.1.0/24).
#

import sys
import os
import yaml
import importlib
import json
from .settings import loadUserSettings
from .settings import saveUserSettings

def discoverModules():
    """
    Discover subdirectories in 'modules' that contain an __init__.py,
    indicating a valid Python package.
    Returns a list of module names (e.g. ["nmap", "tmux"]).
    """
    sBasePath = os.path.join(os.path.dirname(__file__), "modules")
    if not os.path.isdir(sBasePath):
        return []

    lstModules = []
    for sItem in os.listdir(sBasePath):
        sFullPath = os.path.join(sBasePath, sItem)
        if os.path.isdir(sFullPath):
            # Check if __init__.py is present
            if "__init__.py" in os.listdir(sFullPath):
                lstModules.append(sItem)
    return lstModules

def loadModuleCommands(sModuleName):
    """
    Load the commands.yaml file for the specified module.
    Returns a dictionary of command definitions or an empty dict if not found.
    """
    sCmdPath = os.path.join(os.path.dirname(__file__), "modules", sModuleName, "commands.yaml")
    if not os.path.exists(sCmdPath):
        return {}
    with open(sCmdPath, "r", encoding="utf-8") as fCmd:
        return yaml.safe_load(fCmd)

def getModuleInstance(sModuleName):
    """
    Dynamically import the 'module.py' file from the specified module package.
    Returns the imported module object or None if import fails.
    """
    sImportPath = f"fluxcli.modules.{sModuleName}.module"
    try:
        oModule = importlib.import_module(sImportPath)
        return oModule
    except ImportError as e:
        print(f"Error importing module '{sModuleName}': {e}")
        return None

def discoverNativeCommands():
    """
    Load the top-level commands from config/commands.yaml.
    These commands do not belong to any module, but to the CLI itself.
    """
    sConfigPath = os.path.join(os.path.dirname(__file__), "..", "config", "commands.yaml")
    if os.path.exists(sConfigPath):
        with open(sConfigPath, "r", encoding="utf-8") as fNative:
            return yaml.safe_load(fNative)
    return {}

def buildCommandRegistry():
    """
    Build a registry of all modules and their commands, plus any native commands.
    Returns a dictionary like:
    {
      "nmap": {
          "commands": {...},
          "instance": <module 'fluxcli.modules.nmap.module'>
      },
      "tmux": {
          "commands": {...},
          "instance": <module 'fluxcli.modules.tmux.module'>
      },
      "_native_": {
          "commands": {...},  # from config/commands.yaml
          "instance": None
      }
    }
    """
    dRegistry = {}

    # Load modules
    lstFoundModules = discoverModules()
    for sMod in lstFoundModules:
        dCmds = loadModuleCommands(sMod).get("commands", {})
        oInst = getModuleInstance(sMod)
        dRegistry[sMod] = {
            "commands": dCmds,
            "instance": oInst
        }

    # Load native commands
    dNative = discoverNativeCommands().get("commands", {})
    dRegistry["_native_"] = {
        "commands": dNative,
        "instance": None
    }

    return dRegistry

def listAllModules(dRegistry):
    """
    Print a list of all discovered modules (keys in dRegistry except '_native_').
    """
    print("Available modules:")
    for sMod in dRegistry.keys():
        if sMod == "_native_":
            continue
        print(f"  {sMod}")
    print("Use: load <moduleName> to switch context to a module.")

def listModuleCommands(dRegistry, sModuleName):
    """
    Print the commands for a given module.
    """
    dModuleInfo = dRegistry.get(sModuleName)
    if not dModuleInfo:
        print(f"No module named '{sModuleName}' found in registry.")
        return
    dCmds = dModuleInfo.get("commands", {})
    if not dCmds:
        print(f"No commands found for module '{sModuleName}'.")
        return
    print(f"Commands in module '{sModuleName}':")
    for sCmdName, dCmdData in dCmds.items():
        print(f"  {sCmdName} - {dCmdData.get('description', '')}")

def dispatchModuleCommand(dRegistry, sModuleName, sCmdName, lstArgs):
    """
    Dispatch to the appropriate function in the specified module with given arguments.
    """
    dModuleInfo = dRegistry.get(sModuleName)
    if not dModuleInfo:
        print(f"Error: Module '{sModuleName}' not found.")
        return

    dCmds = dModuleInfo.get("commands", {})
    if sCmdName not in dCmds:
        print(f"Error: Command '{sCmdName}' not found in module '{sModuleName}'.")
        return

    oModule = dModuleInfo.get("instance")
    if not oModule:
        print(f"Error: Module instance for '{sModuleName}' is not loaded.")
        return

    # Attempt to call the function in module.py
    if not hasattr(oModule, sCmdName):
        print(f"Error: '{sCmdName}' is not implemented in {sModuleName}.module.py.")
        return

    # Call the function
    funcCmd = getattr(oModule, sCmdName)
    try:
        dResult = funcCmd(*lstArgs)
        # You might format output as JSON or something
        print(json.dumps(dResult, indent=2))
    except Exception as e:
        print(f"Command '{sCmdName}' failed: {e}")

def dispatchNativeCommand(dRegistry, sCmdName, lstArgs):
    """
    Dispatch a CLI-native command (found in config/commands.yaml).
    You might later implement Python callbacks for these, or some static behavior.
    Here we just show that it exists. You could do something advanced if needed.
    """
    dNative = dRegistry["_native_"]["commands"]
    if sCmdName not in dNative:
        print(f"Error: Native command '{sCmdName}' not recognized.")
        return
    dCmdInfo = dNative[sCmdName]
    print(f"Running native command '{sCmdName}'. No custom logic implemented.")
    # Possibly parse dCmdInfo or implement a callback.

def replLoop(dRegistry):
    """
    A simple REPL that:
    - Uses 'load <module>' to switch context
    - Then runs commands within that module
    - 'help' to show usage
    - 'exit' to quit
    """
    dSettings = loadUserSettings()
    sPrompt = dSettings.get("prompt", "[ fluxcli ] > ")
    sCurrentModule = None

    print("Welcome to FluxCLI!")
    print("Type 'help' for a list of commands, 'exit'/'quit' to leave.\n")

    while True:
        try:
            sLine = input(sPrompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not sLine:
            continue

        if sLine in ("exit", "quit"):
            print("Goodbye.")
            break

        lstParts = sLine.split()
        sCmd = lstParts[0]
        lstArgs = lstParts[1:]

        if sCmd == "help":
            if not sCurrentModule:
                # List all modules + usage
                listAllModules(dRegistry)
                print("To load a module: load <moduleName>")
                print("To run a native command: <nativeCmd>")
            else:
                # List commands in the current module
                listModuleCommands(dRegistry, sCurrentModule)
            continue

        if sCmd == "load":
            if not lstArgs:
                print("Usage: load <moduleName>")
                continue
            if lstArgs[0] in dRegistry and lstArgs[0] != "_native_":
                sCurrentModule = lstArgs[0]
                print(f"Module '{sCurrentModule}' loaded. Type 'help' to see commands.")
            else:
                print(f"Module '{lstArgs[0]}' not found.")
            continue

        # If user typed e.g. "nmap pingsweep 192.168.1.0/24" from outside any module
        if sCmd in dRegistry and sCmd != "_native_":
            # means they typed <module> <command> <args>
            if len(lstArgs) < 1:
                print(f"Usage: {sCmd} <command> <arguments>")
                continue
            sActualCmd = lstArgs[0]
            lstActualArgs = lstArgs[1:]
            dispatchModuleCommand(dRegistry, sCmd, sActualCmd, lstActualArgs)
            continue

        # If a module is currently loaded, interpret the first token as a command in that module
        if sCurrentModule:
            # sCmd is actually a command in the current module
            dispatchModuleCommand(dRegistry, sCurrentModule, sCmd, lstArgs)
        else:
            # Maybe it's a native command?
            dispatchNativeCommand(dRegistry, sCmd, lstArgs)

def main():
    """
    Entry point. If called with arguments:
        fluxcli <module> <command> [args...]
      we run that command directly.
      Otherwise, we drop into the REPL.
    """
    dRegistry = buildCommandRegistry()
    if len(sys.argv) < 2:
        # No arguments -> REPL
        replLoop(dRegistry)
    else:
        # Example usage: fluxcli nmap pingsweep 192.168.1.0/24
        # or fluxcli tmux attach
        sModOrCmd = sys.argv[1]
        lstArgs = sys.argv[2:]

        if sModOrCmd in dRegistry and sModOrCmd != "_native_":
            # They specified a module
            if len(lstArgs) < 1:
                print(f"Usage: fluxcli {sModOrCmd} <command> [args...]")
                sys.exit(1)
            sCommand = lstArgs[0]
            lstCmdArgs = lstArgs[1:]
            dispatchModuleCommand(dRegistry, sModOrCmd, sCommand, lstCmdArgs)
        else:
            # Possibly a native command
            dispatchNativeCommand(dRegistry, sModOrCmd, lstArgs)

if __name__ == "__main__":
    main()



