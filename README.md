# NetRecon - Python Network Security Toolkit

Developed a penetration testing toolkit featuring network reconnaissance, web application vulnerability scanning, web scraping, SSH session management, and multithreaded socket programming.

NetRecon brings nine Python tools together through a menu-driven command-line interface. It combines practical network security exercises with automation: inspecting TCP ports, checking web forms for reflected input, managing remote SSH commands, and collecting structured website data. Shared validation helpers and a central launcher connect the individual modules into one toolkit.

Created by **Mariam Asatryan** as a coursework project, NetRecon demonstrates modular programming, network communication, browser automation, and automated testing. Network and keyboard exercises are intended for controlled environments where you have explicit permission.

## Features

| Area | What NetRecon implements |
| --- | --- |
| Network reconnaissance | Nmap-backed TCP port scanning across a user-selected range, with per-port status output. |
| Web application vulnerability scanning | HTML form discovery, test-input submission, and reflected XSS checks with timestamped reports. |
| SSH session management | Interactive authentication, repeated remote command execution, output/error display, and connection cleanup. |
| Web scraping | JavaScript and CSS resource discovery, image URL categorization, and optional SMTP reporting. |
| Browser automation | Headless Firefox scraping through Selenium, reusable scraper classes, and structured JSON export. |
| Multithreaded socket programming | Concurrent HTTP requests using sockets, worker threads, and a shared stop flag. |
| Network security exercises | MAC address changes and ARP spoofing, with attempted ARP restoration after keyboard interruption. |
| Keyboard event handling | A local keyboard-listener exercise with timed console output and network connectivity checks. |

### Structured data extraction

The Primarch scraper uses Warhammer 40K wiki data to demonstrate a complete browser-to-JSON workflow. A domain-specific `PrimarchScraper` extends the reusable `WebScraper` class, extracts table records, and exports legion numbers, Primarch names, legion names, and worlds of rediscovery. It supports visible or headless Firefox sessions and configurable output filenames.

## Getting started

Use **Python 3.12** with the supplied dependency snapshot. Open the project root and create an environment:

```sh
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```sh
source .venv/bin/activate
```

Install dependencies and display the menu:

```sh
python -m pip install -r requirements.txt
python main.py --menu
```

The port scanner requires the **Nmap executable**. The Selenium scraper requires **Firefox** and a compatible WebDriver. MAC changes require Linux with `ifconfig`; the ARP exercise assumes an `eth0` interface and raw-packet privileges. These system requirements are separate from the Python packages.

## Usage

```sh
python main.py
```

Choose a tool by number, enter `help` for launcher guidance, or select `10` to exit. Tools can also be selected directly, though most still prompt for their configuration:

```sh
python main.py --help
python main.py 4 --help
python main.py 4 --no-headless --output primarch_data.json
```

The last command starts Firefox and contacts the configured wiki page. See the [complete usage guide](docs/USAGE.md) for all nine modules, their options, generated files, and platform requirements.

## Project structure

```text
netrecon/
  main.py                  Menu, argument parsing, and subprocess dispatch
  requirements.txt         Pinned dependency snapshot
  src/
    port_scanner.py        TCP port reconnaissance
    xss_scanner.py         Reflected-input checks and reports
    paramiko_study.py      SSH sessions and remote commands
    web_scraping.py        Website resource collection
    primarch_scraper.py    Browser automation and JSON export
    ddos_attack.py         Multithreaded HTTP traffic exercise
    mac_spoofing.py        MAC address lab exercise
    arp_spoofing.py        ARP lab exercise
    keylogger.py           Local keyboard event exercise
    utils/                Validation, email, and image helpers
  tests/                  CLI and utility tests
  docs/USAGE.md            Detailed usage guide
```

## Testing

```sh
python -m pytest -q
```

Tests cover CLI argument handling, dispatch decisions, input validation, and MAC address formatting. Console-input tests use mocked responses. The test that changes `eth0` is skipped by default; it requires Linux and explicit opt-in through `NETRECON_RUN_NETWORK_TESTS=1` on a disposable lab machine.

## Scope and limitations

- The XSS module checks for reflected input. It does not prove browser execution or provide comprehensive web vulnerability detection; its report counter is fixed to 2025.
- The traffic module sends requests from one machine. Despite the original `ddos_attack.py` filename, it is not a distributed testing system.
- SSH sessions automatically trust unknown host keys. The optional email flow accepts a password as an argument, which the launcher prints; credential handling needs improvement before use with real credentials.
- The keyboard module captures actual local keystrokes and prints them locally. It makes connectivity checks but does not transmit keystrokes to the supplied host.
- Dependencies preserve the coursework snapshot and have not been security-audited. Unit tests do not establish end-to-end behavior across live networks or changing websites.

## Author

[Mariam Asatryan](https://github.com/mario0293)
