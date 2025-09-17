# WebWh00pzer - Advanced Web Vulnerability Scanner


**The Most Powerful Web Vulnerability Scanner Ever Created**

Created by: **o0c**
- 🐙 GitHub: [github.com/o0cdev](https://github.com/o0cdev)
- 💬 Discord: **0xo0c**
- 📸 Instagram: [instagram.com/o0ctf](https://instagram.com/o0ctf)
## Showcase 

![showcase](https://raw.githubusercontent.com/o0cdev/WebWh00pzer/refs/heads/main/edit1.png)
![showcase]([https://raw.githubusercontent.com/o0cdev/WebWh00pzer/refs/heads/main/edit3.png))
![showcase]([https://raw.githubusercontent.com/o0cdev/WebWh00pzer/refs/heads/main/edit2.png))
![showcase](https://raw.githubusercontent.com/o0cdev/WebWh00pzer/refs/heads/main/edi4.png)


## 🚀 Features

- **Advanced XSS Detection**: 50+ sophisticated XSS payloads including DOM, reflected, and stored XSS
- **SQL Injection Scanner**: 60+ SQL injection payloads for MySQL, PostgreSQL, MSSQL, Oracle, and NoSQL
- **Multi-threaded Scanning**: Lightning-fast concurrent vulnerability testing
- **WAF Bypass Techniques**: Advanced evasion techniques to bypass security filters
- **Real-time Progress Tracking**: Live scanning progress with detailed statistics
- **Professional Terminal Interface**: Beautiful red-themed hacker-style interface
- **Payload Generation**: Export all payloads to text files for manual testing
- **Multiple Scan Types**: Full scan, XSS-only, or SQL injection-only modes

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Install
```bash
git clone https://github.com/o0cdev/WebWh00pzer
cd WebWh00pzer
pip install -r requirements.txt
python webwh00pzer.py
```

### Manual Install
```bash
pip install requests colorama urllib3
python webwh00pzer.py
```

## 📖 Usage

### Basic Commands
```bash
scan https://target.com/vulnerable.php?id=1


xss https://target.com/search.php?q=test

sqli https://target.com/login.php?user=admin

payloads

help

clear

exit
```

### Example Session
```
WebWh00pzer@o0c:~$ scan https://example.com/search.php?q=test
[*] Starting FULL scan on: https://example.com/search.php?q=test
[*] Initializing scanner...
[*] Loaded 110 payloads
[*] Testing vulnerabilities...

[!] XSS VULNERABILITY FOUND!
    Method: GET | Parameter: q
    Payload: <script>alert('XSS')</script>

[!] SQL INJECTION VULNERABILITY FOUND!
    Method: GET | Parameter: q
    Payload: ' OR 1=1--

================================================================================
SCAN COMPLETE!
Payloads tested: 110
Requests sent: 220
Vulnerabilities found: 2
================================================================================
```

## 🎯 Payload Categories

### XSS Payloads
- **Basic XSS**: Standard script injections
- **Event Handlers**: onload, onerror, onfocus attacks
- **HTML5 XSS**: Modern HTML5 element exploitation
- **Filter Bypass**: Case manipulation and encoding
- **DOM XSS**: Client-side JavaScript exploitation
- **Polyglot Payloads**: Multi-context injection vectors
- **WAF Bypass**: Advanced evasion techniques
- **Unicode/Encoding**: Character encoding attacks

### SQL Injection Payloads
- **Union-based**: Data extraction via UNION queries
- **Boolean-based Blind**: Logic-based information extraction
- **Time-based Blind**: Delay-based vulnerability detection
- **Error-based**: Database error message exploitation
- **Database-specific**: MySQL, PostgreSQL, MSSQL, Oracle payloads
- **NoSQL Injection**: MongoDB and other NoSQL databases
- **Stacked Queries**: Multiple query execution
- **Second-order**: Stored payload exploitation

##  Performance Features

- **Multi-threading**: Up to 20 concurrent requests
- **Smart Rate Limiting**: Prevents server overload
- **Progress Tracking**: Real-time scanning statistics
- **Memory Efficient**: Optimized payload handling
- **Error Handling**: Robust exception management
- **Session Management**: Persistent HTTP sessions

##  Ethical Usage

This tool is designed for:
- **Authorized penetration testing**
- **Bug bounty hunting**
- **Security research**
- **Educational purposes**

⚠️ **IMPORTANT**: Only use this tool on systems you own or have explicit permission to test. Unauthorized scanning is illegal and unethical.

## 📊 Technical Specifications

- **Language**: Python 3.7+
- **Dependencies**: requests, colorama, urllib3
- **Payload Count**: 110+ unique payloads
- **Scan Types**: 3 (Full, XSS, SQL)
- **Threading**: Configurable (default: 20 threads)
- **Output Formats**: Terminal, Text files
- **Platform Support**: Windows, Linux, macOS

## 🔥 Advanced Features

### Payload Export
```bash
WebWh00pzer@o0c:~$ payloads
[*] Generating payload files...
[+] XSS payloads saved to: xss_payloads.txt (50 payloads)
[+] SQL injection payloads saved to: sqli_payloads.txt (60 payloads)
```

### Custom User Agent
The scanner uses a realistic browser user agent to avoid detection:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

### Error Pattern Detection
Advanced SQL error pattern matching for multiple database types:
- MySQL
- PostgreSQL  
- Microsoft SQL Server
- Oracle
- SQLite

## 🎨 Interface Features

- **Red Terminal Theme**: Professional hacker aesthetic
- **Real-time Progress**: Live scanning updates
- **Color-coded Output**: Easy vulnerability identification
- **ASCII Art Banner**: Impressive visual presentation
- **Command History**: Easy command reuse
- **Cross-platform**: Works on all operating systems

## 🚨 Disclaimer

This tool is for educational and authorized testing purposes only. The author (o0c) is not responsible for any misuse or damage caused by this software. Users must comply with all applicable laws and regulations.

## 📞 Contact & Support

- **Creator**: o0c
- **GitHub**: [github.com/o0cdev](https://github.com/o0cdev)
- **Discord**: 0xo0c
- **Instagram**: [instagram.com/o0ctf](https://instagram.com/o0ctf)

---

**WebWh00pzer** - *MADEinRAVEN-X* 🔴
