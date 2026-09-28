import re
import validators

def validate_input(input_str):
    """Validates if input is a valid IP address or domain name"""
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}'
    domain_pattern = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}'
    if re.match(ip_pattern, input_str):
        octets = input_str.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            return 'ip', input_str
    if re.match(domain_pattern, input_str):
        return 'domain', input_str
    return None, input_str

def validate_port(port_str):
    """Validates if input is a valid port number"""
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
    except ValueError:
        raise ValueError("Invalid port number.")


def get_ip():
    '''Prompts the user until a valid IPv4 or IPv6 address is provided.'''
    ipv4_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    ipv6_pattern = re.compile(r"^([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}$")

    while True:
        ip_address = input("Enter IP address: ").strip()
        if ipv4_pattern.fullmatch(ip_address) or ipv6_pattern.fullmatch(ip_address):
            return ip_address
        print("Invalid IP address. Please try again.")

def get_url(is_reachable):
    '''Prompts the user for a domain or URL and validates its format and reachability.'''
    while True:
        user_input = input("Enter a website URL or domain name: ").strip()
        if validators.url(user_input):
            url = user_input
        else:
            url = f"https://{user_input}"
            if not validators.url(url):
                print("Invalid input. Please enter a valid domain or full URL.")
                continue
        if is_reachable(url):
            return url
        else:
            print("Cannot connect to the provided URL. Please try again.")   


def get_port_range():
 '''Prompts the user to enter a valid range of ports in the format "<min>-<max>".'''
 port_range_pattern = re.compile("([0-9]+)-([0-9]+)") 
 while True:
    print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        return port_min, port_max
    else:
        print("Invalid port range format. Try again.") 

def validate_paramiko_input(hostname):
    '''Validates if the input is a valid IPv4 address or hostname (for SSH/Paramiko usage).'''
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    hostname_pattern = re.compile(r'(?i)^(?:([a-z0-9-]+|\*)\.)?([a-z0-9-]{1,61})\.([a-z0-9]{2,7})$')
    if re.match(ip_pattern, hostname):
        octets = hostname.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            return hostname
        return True
    elif hostname_pattern.search(hostname):
        return True
    else:
        return False