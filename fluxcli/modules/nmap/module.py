import subprocess
import re

def pingsweep(sSubnet: str) -> dict:
    """
    Perform an Nmap ping sweep on sSubnet.
    Returns a dict with discovered hosts, e.g. {"hosts": [...]}.
    """
    try:
        oResult = subprocess.run(
            ["nmap", "-sn", sSubnet],
            capture_output=True,
            text=True,
            check=False
        )
        sOutput = oResult.stdout
        sPattern = r"Nmap scan report for ([^ ]+) \(([\d\.]+)\).*?MAC Address: ([\w:]+)"
        lstMatches = re.findall(sPattern, sOutput, flags=re.DOTALL)
        lstHosts = []
        for sHostname, sIp, sMac in lstMatches:
            lstHosts.append({
                "ip": sIp,
                "hostname": sHostname,
                "mac": sMac
            })
        return {"hosts": lstHosts}
    except Exception as e:
        return {"error": str(e)}

def portscan(sTarget: str, sPorts="1-1000") -> dict:
    """
    Perform an Nmap port scan on sTarget for ports in sPorts range.
    Returns a dict with open ports or an error.
    """
    try:
        oResult = subprocess.run(
            ["nmap", "-p", sPorts, sTarget],
            capture_output=True,
            text=True,
            check=False
        )
        sOutput = oResult.stdout
        # For simplicity, let's parse lines indicating open ports:
        # e.g. "PORT   STATE SERVICE"
        # We'll return them in a simple structure
        lstOpen = []
        for sLine in sOutput.splitlines():
            # A very naive parse, e.g. "80/tcp open  http"
            if "/tcp" in sLine and " open " in sLine:
                lstOpen.append(sLine.strip())
        return {"ports_open": lstOpen}
    except Exception as e:
        return {"error": str(e)}
