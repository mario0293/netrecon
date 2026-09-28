import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from datetime import datetime
from utils.validator import get_url
from pathlib import Path
import fnmatch
import base64

def is_reachable(url):
    '''Check if a URL is reachable with a request.'''
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def get_all_forms(url):
    ''' Retrieve all HTML forms from a given URL.'''
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    '''extracting all possible useful information about an HTML `form`'''
    details = {}
    action = form.attrs.get("action", "").lower()# get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()# get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action# put everything to the resulting dictionary
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, url, value):
    ''' Submit a form with a given payload.'''
    target_url = urljoin(url, form_details["action"])# constructing the full URL (if the url provided in action is relative)
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search": # replace all text and search values with `value`
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:# if input name and value are not None,    
            data[input_name] = input_value# then add them to the data of form submission
    print(f"[+] Submitting malicious payload to {target_url}")
    print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)


def scan_xss(url, report_file):
    ''' Scan a URL for reflected XSS vulnerabilities.'''
    forms = get_all_forms(url)
    report_file.write(f"[+] Detected {len(forms)} forms on {url}.\n")
    js_script = "<script>alert('hi')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        response = submit_form(form_details, url, js_script)
        content = response.content.decode(errors="ignore")
        if js_script in content:
            report_file.write(f"[!] XSS Detected on {url}\n")
            report_file.write("[*] Form details:\n")
            report_file.write(pprint(form_details, stream=None, indent=4) or "")
            is_vulnerable = True
    return is_vulnerable

def report_to_file(url):
    ''' Scan a URL and save the XSS scan report to a timestamped file.'''
    now = datetime.now()  
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"xss_report_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as report_file:
        report_file.write(f"XSS Scan Report\nDate & Time: {now}\nURL: {url}\n\n")
        vulnerable = str(scan_xss(url, report_file))
        encoded = base64.b64encode(vulnerable.encode('utf-8')).decode()
        report_file.write(f"\nScan completed. Vulnerable: {encoded}\n")
    print(f"[+] Report saved to {filename}")    

def main():
    '''Main function to initiate the XSS scan process.'''
    try:
     url = get_url(is_reachable)
     report_to_file(url)
     reports_2025 = [
        file for file in Path(".").iterdir()
        if file.is_file() and fnmatch.fnmatch(file.name, "xss_report_2025*.txt")
     ]
     print(f"[+] You have completed {len(reports_2025)} XSS scans in 2025.")
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.") 

if __name__ == "__main__":
    main()
