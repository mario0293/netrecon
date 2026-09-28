# NetRecon - Python Network Security Toolkit

Developed a penetration testing toolkit featuring network reconnaissance, web application vulnerability scanning, web scraping, SSH session management, and multithreaded socket programming.

## Setup and navigation

Follow the [README setup instructions](../README.md). Run commands from the repository root so the launcher can locate `src/`.

```sh
python main.py --menu
python main.py --help
python main.py
```

`--menu` displays the list without launching a tool. With no arguments, the launcher prompts for a selection. Enter `help` at that prompt for guidance, `menu` to redraw it, or `10` to exit. After a tool finishes, the launcher offers to exit or return to the menu.

Direct selection uses `python main.py NUMBER`. Most tools still request inputs interactively. Only tools 4 and 5 implement their own argument parsers; use `python main.py 4 --help` or `python main.py 5 --help` for their options.

## 1. HTTP traffic lab

Demonstrates multithreaded socket programming by repeatedly sending HTTP GET requests through worker threads. Prompts for an IP or domain, a port (default `80`), and a thread count (default `50`). A shared flag coordinates stopping after `Ctrl+C`.

This generates continuous traffic from one machine, not a distributed attack. Use an explicitly authorized, isolated lab endpoint. The original implementation remains in `src/ddos_attack.py`.

## 2. MAC address lab

Prompts for an interface, generates a MAC address, and uses `ifconfig` to bring the interface down, change its address, and bring it back up. It then displays the interface configuration.

Requires Linux, `ifconfig`, and privileges to change network configuration. There is no second confirmation after entering the interface. Connectivity may be interrupted, and the original address is not automatically restored.

## 3. SSH session management

Prompts for a hostname or IP, username, and hidden password. After connecting, accepts repeated remote commands and displays their standard output and errors. Enter `exit` at the command prompt to close the session. Errors are logged to `ssh_errors.log`.

The Paramiko implementation automatically accepts unknown host keys. Explicit host-key verification remains an improvement for use beyond controlled lab hosts.

## 4. Primarch web scraper

Loads the configured Warhammer 40K Primarch wiki page in Firefox. `PrimarchScraper` extends `WebScraper` and extracts table records containing `legion_number`, `primarch`, `legion_name`, and `world_of_rediscovery` into JSON.

| Option | Behavior |
| --- | --- |
| `--no-headless` | Shows Firefox; the default is headless. |
| `--output FILE` | Selects the JSON filename; defaults to `primarch_data.json`. |
| `--browser firefox` | Selects Firefox, the only implemented browser. |

```sh
python main.py 4 --no-headless --output primarch_data.json
```

Existing output at the selected path is sent to the recycle bin before replacement. Errors are logged to `selenium_error.log`. Extraction depends on the website's table structure and may need adjustment when the page changes.

## 5. Web resource scraper

Prompts for a URL and extracts JavaScript, stylesheet, and image links from its HTML. Images are downloaded temporarily to identify their formats; saved results contain categorized URL lists, not an image archive.

| Output | Contents |
| --- | --- |
| `javascript_files.txt` | JavaScript resource URLs. |
| `css_files.txt` | Stylesheet resource URLs. |
| `sorted_images/*_files.txt` | Image URL lists grouped by format. |

The existing `sorted_images/` directory is replaced during processing. Temporary files use `temp_downloads/`, which is removed after normal processing.

Optional email arguments are `--send-email`, `--email EMAIL`, and `--password PASSWORD`. The SMTP helper sends the JavaScript and CSS lists to the sender's own address through Gmail SMTP with STARTTLS. The launcher prints arguments, exposing the password in console output; shell history and process listings may also retain it. Do not supply real credentials until credential handling is improved.

## 6. ARP lab

Prompts for target and gateway IP addresses and uses Scapy to send forged ARP responses on the local network. Assumes an `eth0` interface and requires raw-packet privileges. On `Ctrl+C`, it attempts to restore both hosts' ARP mappings; successful restoration depends on hosts responding.

Use an isolated, authorized lab network. This module does not enable packet forwarding or implement traffic capture by itself.

## 7. Port reconnaissance

Prompts for an IP and a TCP port range, then uses `nmap.PortScanner()` to report per-port state. Install Nmap separately from the Python package. Scan only hosts within your authorized scope.

## 8. Local keyboard event exercise

Uses `pynput` to capture actual local keyboard events and accumulate them for periodic console output. Handles printable characters and special keys including Enter, Tab, Space, and Backspace. Collection and display depend on connectivity checks to port `80` of the supplied IP; loopback and common private IPv4 ranges are rejected.

Keystrokes are not saved to a file or transmitted to that host, but network connection attempts occur. Escape handling also depends on connectivity, and timer cleanup has limitations in the original implementation. Use only in a controlled local session without sensitive input.

## 9. Reflected XSS checks

Prompts for a URL, discovers HTML forms, and submits a basic script test value through text/search fields. Checks responses for reflected text and creates `xss_report_YYYY-MM-DD_HH-MM-SS.txt`.

Reflection is an indicator for manual investigation, not proof of executable XSS. The report stores a Boolean result in base64, which is encoding rather than encryption. Form details are printed to the console instead of fully serialized into the report. The scan counter matches reports from 2025, not the current year.

## Testing

```sh
python -m pytest -q
```

Tests cover launcher behavior, validators, and MAC address formatting. The MAC-changing test is disabled by default. On Linux, `NETRECON_RUN_NETWORK_TESTS=1` explicitly enables it; this changes `eth0` and should be used only on a disposable lab machine.

## Generated files

Logs, default scraper outputs, scan reports, environments, and caches are excluded by `.gitignore`. Check custom output filenames before committing. Do not commit credentials, captured data, or private reports.

Return to the [project overview](../README.md).
