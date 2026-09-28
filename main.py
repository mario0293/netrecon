import argparse
import subprocess
import sys
import shlex


def display_logo():
    print('NetRecon - Python Network Security Toolkit')


def display_tool_options():
    print("Select a NetRecon tool:")
    for number, label in enumerate([
        "HTTP traffic lab", "MAC address lab", "SSH session management",
        "Primarch web scraper", "Web resource scraper", "ARP lab",
        "Port reconnaissance", "Local keyboard event exercise", "Reflected XSS checks", "Exit"
    ], start=1):
        print(f"  {number}. {label}")

def get_feature_mapping():
    """mapping between menu choices and their corresponding scripts."""
    return {
        "1": {"script": "src/ddos_attack.py", "name": "HTTP traffic lab", "args_supported": False},
        "2": {"script": "src/mac_spoofing.py", "name": "MAC Spoofing", "args_supported": False},
        "3": {"script": "src/paramiko_study.py", "name": "SSH session management", "args_supported": False},
        "4": {"script": "src/primarch_scraper.py", "name": "Primarch Scraper", "args_supported": True,
             "args_help": ["--no-headless: Opens the browser for scraping", 
                          "--output FILE:  Save data to specified filename",
                          "--browser BROWSER  Browser type (default: firefox)"]},
        "5": {"script": "src/web_scraping.py", "name": "Web Scraping", "args_supported": True,
            "args_help": ["--send-email: Sending scraped javascript and css files only via email",
                          "--email EMAIL: Sender email address @gmail.com",
                         "--password PASSWORD: Sender email password, must be app password"]},
        "6": {"script": "src/arp_spoofing.py", "name": "ARP Spoofing", "args_supported": False},
        "7": {"script": "src/port_scanner.py", "name": "Port Scanner", "args_supported": False},
        "8": {"script": "src/keylogger.py", "name": "Local keyboard event exercise", "args_supported": False},
        "9": {"script": "src/xss_scanner.py", "name": "XSS Scanner", "args_supported": False},
        "10": {"script": "exit", "name": "Exit", "args_supported": False}
    }


def display_help_info():
    print("\nTo use: Enter a number (1-9) followed by any arguments for that tool.")
    print("For example: '4 --no-headless --output data.json'")
    print("To see help for a specific tool: '4 --help' or '4 -h'")
    print("\nTools that accept arguments:")
    print("  4. Primarch Scraper:")
    print("     --no-headless    : Run with visible browser")
    print("     --output FILE    : Save results to custom filename")
    print("     --browser BROWSER  Browser type (default: firefox)")
    print("\n")
    print("  5. Web Scraping:")
    print("     --send-email    : Send the results via email")
    print("\n")

def return_to_menu():
    display_logo()
    display_tool_options()
    choice, args = parse_user_input()
    # Handling special commands here instead of passing them through
    if choice in ["menu", "help"]:
        return return_to_menu()  # Just recursively call this function again 
    return choice, args

def execute_script(script_path, args=None):
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    try:
        print(f"Launching: {' '.join(cmd)}")
        process = subprocess.run(cmd, check=True)
        return process.returncode == 0
    except subprocess.CalledProcessError:
        print(f"Error running script: {script_path}")
        return False
    except FileNotFoundError:
        print(f"Script not found: {script_path}")
        return False

def show_tool_specific_help(tool_data):
    """Display help information for a specific tool."""
    if "args_help" in tool_data:
        print("\nAdditional information about arguments:")
        for arg_help in tool_data["args_help"]:
            print(f"  {arg_help}")
        print()

def get_raw_user_input():
    """Get and perform initial processing of user input string."""
    user_input = input("Enter your choice (with optional arguments): ").strip()  
    # Handle special commands
    if user_input.lower() in ["help"]:
        display_help_info()
        input("Press Enter to continue...") # Wait for user to press enter before continuing
        return "menu"
    if user_input.lower() == "menu":
        return "menu"
    return user_input

def parse_user_input():
    """Parsing user input for menu selection and arguments."""
    user_input = get_raw_user_input()    
    if user_input == "menu":# Handle special return values
        return "menu", []     
    try: # Split the input into choice and arguments
        parts = shlex.split(user_input)
    except ValueError:
        print("Error occurred. Please make sure quotes are properly closed.")
        return "menu", []       
    if not parts:
        return "menu", []  # Return empty choice and args if input is empty     
    choice = parts[0]
    args = parts[1:] if len(parts) > 1 else []  
    return choice, args

def validate_tool_args(tool_data, args):
    """Check if arguments are supported for the tool."""
    name = tool_data["name"]
    args_supported = tool_data["args_supported"]
    is_help_request = args and ('--help' in args or '-h' in args)
    if args and not args_supported:
        print(f"Warning: {name} does not support command line arguments. Arguments will be ignored.") 
    return is_help_request

def execute_tool(tool_data, args, interactive_mode=False):
    """Execute the tool with provided arguments."""
    script = tool_data["script"]
    name = tool_data["name"]
    is_help_request = validate_tool_args(tool_data, args)
    print(f"Starting {name}...")
    #to handle help requests in interactive mode differently
    if interactive_mode and is_help_request:
        execute_script(script, args)
        show_tool_specific_help(tool_data)
        return False
    else:
        execute_script(script, args)
        return True


def run_tool(choice, args, feature_menu, interactive_mode=True):
    # Handle *special* choice
    if choice == "0":
        print("NetRecon closing screen.")
        execute_script("src/.hidden_tools/unknown_sword.py")
        sys.exit(0)    
    if choice not in feature_menu: # Handle invalid choices
        print("Invalid choice. Please try again.")
        return False
    if choice == "10": # Exit choice
        print("Exiting... Goodbye!")
        sys.exit(0)  
    tool_data = feature_menu[choice] # processing valid choices
    return execute_tool(tool_data, args, interactive_mode)


def confirm_exit():
    exit_choice = input("Do you want to exit? (y/n): ").lower()
    if exit_choice == 'y':
        print("NetRecon session complete. Goodbye!")
        return True
    elif exit_choice == 'n':
        print("Returning to the NetRecon menu.")
        return False
    else:
        print("Invalid input. Exiting... Goodbye!")
        return True


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='NetRecon - Python Network Security Toolkit - Select and execute various security tools.')
    parser.add_argument('feature', nargs='?', help='Tool number to run directly (1-9 or 10 to exit)')
    parser.add_argument('feature_args', nargs=argparse.REMAINDER, 
                      help='Arguments to pass to the selected tool (these will be passed as-is)')
    parser.add_argument('--menu', action='store_true', help='Show the menu to get information about the tools')
    return parser.parse_args()

def main():
    try:
        args = parse_command_line_args()
        feature_menu = get_feature_mapping() 
        if args.menu:  # Just display the menu and exit         
            display_logo()
            display_tool_options()
            sys.exit(0)
        elif args.feature: # Non-interactive mode: Run directly from command line
            run_tool(args.feature, args.feature_args, feature_menu)
            sys.exit(0)
        else:   # Interactive mode: Showing menu and process user input 
         while True:  
                choice, script_args = return_to_menu()
                tool_executed = run_tool(choice, script_args, feature_menu, interactive_mode=True)# Handle the user's choice
                if tool_executed and confirm_exit():# Only ask to exit if we actually ran a tool (not just help)
                    break 
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting program...")
        sys.exit(0)


if __name__ == "__main__":
    main()