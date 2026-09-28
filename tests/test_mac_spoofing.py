import os
import sys
import subprocess
import re
import pytest
from src.mac_spoofing import generate_random_mac, change_mac

def get_current_mac(interface):
    """Extracting current MAC address from `ifconfig` output."""
    try:
        result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
        match = re.search(r"ether\s+([0-9a-fA-F:]{17})", result.stdout)
        return match.group(1).lower() if match else None
    except FileNotFoundError:
        pytest.skip("'ifconfig' not found. This test only works on Linux systems.")

@pytest.mark.skipif(
    sys.platform != "linux" or os.environ.get("NETRECON_RUN_NETWORK_TESTS") != "1",
    reason="Changes eth0; opt in only on an isolated Linux lab machine.",
)
def test_mac_change():
    """testing the mac change"""
    interface = "eth0"
    new_mac = generate_random_mac()
    try:
        change_mac(interface, new_mac)
        changed_mac = get_current_mac(interface)
        assert changed_mac == new_mac.lower(), f"MAC not changed correctly! Expected {new_mac}, got {changed_mac}"
    except FileNotFoundError:
        pytest.skip("'ifconfig' not found. This test only works on Linux systems.") #skipping when testing on windows

def test_mac_format():
    mac = generate_random_mac()
    assert re.match(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$", mac), f"Invalid MAC format: {mac}"
