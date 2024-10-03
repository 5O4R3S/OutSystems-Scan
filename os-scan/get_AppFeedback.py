from colorama import Fore, Style
import requests
import re

def get_EctAppFeedback(environment,app_module_name,header):
    # Checking ECT Provider version
    print(f"| {Fore.WHITE}[|||] {Style.DIM}{Style.BRIGHT}[App Feedback] Checking the version of ECT Provider (App Feedback) on the domain...{Style.RESET_ALL}")
    check_ECTModule(environment,app_module_name,header)


def default_msg(environment):
    print(f"| {Fore.WHITE}[|||] {Style.DIM}[App Feedback] Manually check the version by accessing the ECT Provider login page at: '{environment}/ECT_Provider'{Style.RESET_ALL}")
    print(f"| {Fore.WHITE}[|||] {Style.DIM}[App Feedback] Versions below 11.27 may be vulnerable according to the security article: https://www.linkedin.com/pulse/outsystems-security-feedback-app-extremely-vulnerable-lucas-soares-fnjge/{Style.RESET_ALL}")

def check_ECTModule(environment,app_module_name,header):
    url_ECTProvider = environment+'/ECT_Provider/_osjs.js'
    # Sending a GET request to the URL
    response = requests.get(url_ECTProvider, headers=header)

    # Checking the response code
    if response.status_code == 200:
        
        # Regular expression to capture text in single quotes
        # e.g // * OutSystems Platform Server 11.27.0.42818 return "11.27.0.42818"
        regex = r"Server (\d+\.\d+\.\d+\.\d+)"

        # Extract values
        result = re.search(regex,response.text)
        if result:
            version_string = result.group(1)
            version_numeric = [int(x) for x in version_string.split('.')]
            
            # Version with vulnerability
            version_vulnerable = [11, 27, 0, 42818]
            
            if version_numeric <= version_vulnerable:
                print(f"| {Fore.RED}[|||] {Style.DIM}[App Feedback] The current version {version_string} of ECT Provider running on the domain is vulnerable to arbitrary code execution!{Style.RESET_ALL}")
                print(f"| {Fore.RED}[POC] {Style.DIM}[App Feedback] Use the 'nodeXPath' parameter when sending feedback to inject javascript code, for example: 'nodeXPath=;alert();'.{Style.RESET_ALL}")
                print(f"| {Fore.RED}[|||] {Style.DIM}[App Feedback] READ HOW TO EXPLOIT AND PROTECT against this vulnerability in the security article: https://www.linkedin.com/pulse/outsystems-security-feedback-app-extremely-vulnerable-lucas-soares-fnjge/{Style.RESET_ALL}")
            else:
                print(f"| {Fore.WHITE}[|||] {Style.DIM}[App Feedback] The current version {version_string} of ECT Provider is not vulnerable.{Style.RESET_ALL}")
    else:
        # Error in request
        print(f"{Fore.RED}{Style.DIM}get_AppFeedback.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")