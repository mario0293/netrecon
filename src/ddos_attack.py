import socket
import threading
import time
from utils.validator import validate_input,validate_port


def send_requests(target, port, stop_flag):
    """Sends HTTP requests to target"""
    while not stop_flag[0]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode('ascii'))
            s.close()
        except socket.error:
            time.sleep(0.5)  # Waiting before trying again

def resolve_domain(target):
    """Resolving a domain name to an IP address."""
    try:
        print(f"Resolving {target}...")
        resolved_ip = socket.gethostbyname(target)
        print(f"Resolved to {resolved_ip}")
        return resolved_ip
    except socket.gaierror:
        print(f"Could not resolve {target}. Please check the domain name.")
        return None
    
def get_target_info():
    """Geting and validating target information from user"""
    while True:
        try:
            user_target = input("Target (IP or domain): -> ")
            input_type, target = validate_input(user_target)
            if input_type is None:
              print("Invalid input. Please enter a valid IP address or domain name.")
              continue
            user_port = input("Port (default is 80): -> ")
            port = validate_port(user_port) if user_port else 80
        except ValueError:
            print("Invalid port number. Please enter a valid integer.")
            continue
        if input_type == 'domain':
            resolve_domain(target)
        return target, port

def create_threads(target, port, thread_count, stop_flag):
    """Creating and starting worker threads for the test"""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_requests, args=(target, port, stop_flag))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    return threads

def run_test():
    """execution function"""
    try: 
        target, port = get_target_info() # Get target information
        thread_input = input("Number of threads (default 50): -> ")
        thread_count = int(thread_input) if thread_input else 50 
        stop_flag = [False] #shared flag for stopping threads
        print(f"Starting test on {target}:{port} with {thread_count} threads...") #Launching threads
        print("Press Ctrl+C to stop")
        create_threads(target, port, thread_count, stop_flag)
        while True: 
            time.sleep(1)  # Keeping the main thread alive until interrupted
    except KeyboardInterrupt:
        stop_flag[0] = True
        print("\nTest stopped by user.")
        time.sleep(1)  # Allow threads time to exit

def main():
    run_test()

if __name__ == "__main__":
    main()