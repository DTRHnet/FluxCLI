"""
settings.py - Load and save user settings for FluxCLI on Windows.

If you're adding cross-platform logic, you can also detect platform.system()
and change paths accordingly. But this example focuses on Windows AppData.
"""

import os
import yaml
import platform

__all__ = ["loadUserSettings", "saveUserSettings"]  # Ensures these are exported

def getWindowsSettingsPath() -> str:
    """
    Return the path to the fluxcli config file on Windows.
    Typically: C:\\Users\\<Username>\\AppData\\Roaming\\FluxCLI\\fluxcli.yaml.
    """
    # The %APPDATA% environment variable usually points to
    # 'C:\\Users\\<Username>\\AppData\\Roaming'
    sAppData = os.environ.get("APPDATA", None)
    if not sAppData:
        # Fallback if APPDATA is not defined
        sAppData = os.path.expanduser("~")

    return os.path.join(sAppData, "FluxCLI", "fluxcli.yaml")

def getSettingsPath() -> str:
    """
    Return the path to fluxcli.yaml. 
    If you're strictly on Windows, we always use getWindowsSettingsPath().
    For cross-platform usage, you'd detect OS with platform.system().
    """
    sSystem = platform.system().lower()
    if sSystem == "windows":
        return getWindowsSettingsPath()
    else:
        # Example fallback for Linux/macOS:
        sHome = os.path.expanduser("~")
        return os.path.join(sHome, ".fluxcli", "fluxcli.yaml")

def loadUserSettings() -> dict:
    """
    Load user settings from the fluxcli.yaml file, creating an empty dict if none exist.
    """
    sPath = getSettingsPath()
    if not os.path.exists(sPath):
        return {}  # No settings file yet

    try:
        with open(sPath, "r", encoding="utf-8") as fSettings:
            dData = yaml.safe_load(fSettings)
            if not dData:
                return {}
            return dData
    except Exception as e:
        # If something goes wrong reading YAML, return empty or log error.
        print(f"[Warning] Failed to read settings file '{sPath}': {e}")
        return {}

def saveUserSettings(dSettings: dict) -> None:
    """
    Save the given dictionary of settings to fluxcli.yaml.
    Creates the necessary directory if it doesn't exist.
    """
    sPath = getSettingsPath()
    try:
        os.makedirs(os.path.dirname(sPath), exist_ok=True)
        with open(sPath, "w", encoding="utf-8") as fSettings:
            yaml.dump(dSettings, fSettings)
    except Exception as e:
        print(f"[Error] Failed to save settings to '{sPath}': {e}")
