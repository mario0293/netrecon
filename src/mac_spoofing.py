#!/usr/bin/env python3
import subprocess
import random

def generate_random_mac():
    """Generating a random MAC address."""
    # First byte must have the second last bit unset (locally administered) and the last bit unset (unicast)
    first_byte = random.randint(0, 255) & 0xFC  # Ensuring that unicast and locally administered
    remaining_bytes = [random.randint(0, 255) for _ in range(5)]# Generating remaining 5 bytes and adding the remaining
    mac_bytes = [first_byte] + remaining_bytes
    # Format as MAC address
    random_mac = ':'.join([f"{byte:02x}" for byte in mac_bytes])
    return random_mac

def change_mac(interface, new_mac):
    """Changing MAC address of the specified interface."""
    print(f"Changing MAC address for {interface} to {new_mac}")
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])   # Change the MAC
    subprocess.run(["ifconfig", interface, "up"])# Bringing the interface back up
    # Verify the change
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    print("New configuration:")
    print(result.stdout)

def main():
    try:
     # Get interface from user
     interface = input("Enter network interface (e.g., eth0, wlan0): ")
     new_mac = generate_random_mac()  # Generating a random MAC address
     print(f"Generated random MAC: {new_mac}")
     change_mac(interface, new_mac)# Change MAC address
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.") 
    except FileNotFoundError:
        print("'ifconfig' command not found. This MAC spoofer is only supported on Linux.")

if __name__ == "__main__":
    main()