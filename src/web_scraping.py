import argparse
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from utils.email_automation import MailSender
import http.client
from utils.validator import get_url
from utils.image_sorter import sort_images_by_format

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Extract JS and CSS URLs and optionally send via email.")
    parser.add_argument("--send-email", action="store_true", help="Send the results via email")
    parser.add_argument("--email", type=str, help="Sender email address")
    parser.add_argument("--password", type=str, help="Sender email password")
    return parser.parse_args()

def validate_email_args(args):
    '''Validate email arguments if send-email flag is set.'''
    if args.send_email and (not args.email or not args.password):
        print("Email and password must be provided with --email and --password.")
        return False
    return True

def is_reachable(url):
    """Check if the given URL is reachable via HTTPS."""
    try:
        parsed = urlparse(url)
        conn = http.client.HTTPSConnection(parsed.netloc, timeout=5)
        conn.request("HEAD", parsed.path or "/")
        response = conn.getresponse()
        return response.status < 400
    except Exception as e:
        print("HTTP error:", e)
        return False

def get_html_content(url):
    """Fetch HTML content of a URL."""
    session = requests.Session()
    response = session.get(url)
    return response.content

def extract_script_files(soup, base_url):
    """Extract all JavaScript file URLs from HTML soup."""
    script_files = []
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(base_url, script.attrs.get("src"))
            script_files.append(script_url)
    return script_files

def extract_css_files(soup, base_url):
    """Extract all CSS file URLs from HTML soup."""
    css_files = []
    for link in soup.find_all("link"):
        if link.attrs.get("href") and "stylesheet" in link.attrs.get("rel", []):
            css_url = urljoin(base_url, link.attrs.get("href"))
            css_files.append(css_url)
    return css_files

def extract_image_files(soup, base_url):
    """Extract all image file URLs from HTML soup."""
    image_files = []
    for img in soup.find_all("img"):
        if img.attrs.get("src"):
            img_url = urljoin(base_url, img.attrs.get("src"))
            image_files.append(img_url)
    return image_files

def write_to_file(filename, data):
    """Write list of items to a text file."""
    with open(filename, "w") as f:
        for item in data:
            print(item, file=f)

def send_files_via_email(email, password):
    """Send extracted JS and CSS files via email."""
    with open("javascript_files.txt") as jsf, open("css_files.txt") as cssf:
        message = "[JavaScript Files]\n" + jsf.read() + "\n[CSS Files]\n" + cssf.read()
    sender = MailSender(email,password)
    sender.sendmail(message)

def save_extracted_resources(script_files, css_files, image_files):
    '''Saving extracted webpage resources to files and sort images.'''
    write_to_file("javascript_files.txt", script_files)
    write_to_file("css_files.txt", css_files)
    sort_images_by_format(image_files)
    print("Links saved to 'javascript_files.txt', 'css_files.txt', and 'sorted_images'.")

def process_webpage(url):
    '''Processing a webpage to extract resources.'''
    soup = bs(get_html_content(url), "html.parser")
    script_files = extract_script_files(soup, url)# Extract resources
    css_files = extract_css_files(soup, url)
    image_files = extract_image_files(soup, url)
    print(f"Found: {len(script_files)} script files, {len(css_files)} CSS files, {len(image_files)} image files")
    if script_files or css_files or image_files:
        save_extracted_resources(script_files, css_files, image_files)
    else:
        print("No script, CSS, or image files found on this page.")    
    return script_files, css_files


def main():
    """Main function to handle argument parsing and execution flow."""
    try: 
        args = parse_args() # Parse and validate arguments
        if not validate_email_args(args):
            return  
        url = get_url(is_reachable) # checking URL
        process_webpage(url) # Processing webpage
        if args.send_email:# Sending email if requested
            send_files_via_email(args.email, args.password)         
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")   

if __name__ == "__main__":
    main()
