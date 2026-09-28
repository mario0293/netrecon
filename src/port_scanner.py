import nmap
import itertools
from utils.validator import get_ip, get_port_range


def scan_ports(ip_add_entered, port_min, port_max):
    """Scanning the IP address for open TCP ports within the specified range."""
    nm = nmap.PortScanner()
    port_range = f"{port_min}-{port_max}"
    print(f"To exit press Ctrl+C")
    print(f"Scanning {ip_add_entered} for ports {port_range}...")
    try:
        nm.scan(ip_add_entered, port_range)
        port_iterator = itertools.islice(itertools.count(port_min), port_max - port_min + 1)
        for port in port_iterator:
            if port in nm[ip_add_entered]['tcp']:  # We're looping over all of the ports in the specified range.
                port_status = nm[ip_add_entered]['tcp'][port]['state'] # extracting the port status from the returned object
                print(f"Port {port} is {port_status}")
            else:
                print(f"Port {port} has no information.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to get input and perform the port scan."""
    try:
        ip_address = get_ip()
        port_min, port_max = get_port_range()
        scan_ports(ip_address, port_min, port_max)
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)
    
if __name__ == "__main__":
    main()        