import paramiko
from paramiko import SSHClient
from getpass import getpass
import logging
from utils.validator import validate_paramiko_input

def setup_logging():
    """Configures error logging to 'ssh_errors.log'."""
    logging.basicConfig(
        filename='ssh_errors.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

def get_hostname():
    """Prompts the user for a valid hostname or IP address."""
    while True:
        hostname = input("Enter SSH hostname or ip address: ").strip()
        if validate_paramiko_input(hostname):
            return hostname
        print("Invalid hostname. Please enter a valid hostname or IP address.")


def get_username():
    """Prompts the user for an SSH username."""
    while True:
        username = input("Enter SSH username: ").strip()
        if username is not None:
            return username
        print("Invalid input. Please enter a valid username.")

def get_password():
    """Prompts the user for an SSH password (hidden input)."""
    while True:
        password = getpass("Enter SSH password: ").strip()
        if password is not None:
            return password
        print("Invalid input. Please enter a valid password.")

def run_commands(client):
    """Runs user-provided commands on the connected SSH session."""
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit':
            break
        if not command:
            print("Empty command. Try again.")
            continue
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error:
            print("Error:", error)

def make_connection(hostname, username, password):
    """Establishes SSH connection and manages command execution."""
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
        print(f"Connected to {hostname}")
        run_commands(client)
    except paramiko.SSHException as e:
        logging.error(f"SSH connection failed: {e}")
        print(f"SSH connection failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
    finally:
        client.close()
        print("Connection closed.")

def main():
    try:
     setup_logging()
     hostname = get_hostname()
     username = get_username()
     password = get_password()
     make_connection(hostname, username, password)
    except KeyboardInterrupt:
        print("\nExiting...") 
        exit(0)

if __name__ == "__main__":
    main()
