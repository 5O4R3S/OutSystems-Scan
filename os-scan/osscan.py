import argparse
from urllib.parse import urlparse
from colorama import Fore, Style
import commons
import requests
import get_Screens
import get_AppDefinitions
import get_ModulesReferences
import get_EndScope
import get_Resources
import get_ClientVariables
import get_MobileApp

# Create an argument parser
parser = argparse.ArgumentParser(prog="OutSystems Scan", 
                                 description="How to use OutSystems Scan to find potential exploit weaknesses.",
                                 epilog="EXAMPLE USAGE: \n python3 osscan.py -u https://personal.outsystemscloud.com/MyApp")

# Defines an argument
parser.add_argument("-u", "--url", help="Url to be explored, e.g. https://personal.outsystemscloud.com/MyApp", required=True)
#parser.add_argument("-m", "--modules", help="Exploration modules, e.g. Test Screens, Variable Screens, etc.")

# Analyze the arguments.
args = parser.parse_args()

def make_url(in_url):
    if in_url.endswith("/"):
        return in_url[:-1]
    else:
        return in_url
    
# Create variables
url_full = make_url(args.url)
environment = ""
application = ""
module_services = "moduleservices/"
module_services_info = "moduleinfo/"
module_informations_url = ""

# Separating the parts of the url
parsed_url = urlparse(url_full)
url_domain = parsed_url.scheme + "://" + parsed_url.hostname
app_module_name = parsed_url.path.lstrip("/")

# Make Urls
environment = url_domain
application = app_module_name

# Module Informations url
module_informations_url = url_domain+'/'+app_module_name+'/'+module_services+module_services_info

# Tool art
print("""\
   ____   _____       _____                 
  / __ \ / ____|     / ____|                
 | |  | | (___ _____| (___   ___ __ _ _ __  
 | |  | |\___ \______\___ \ / __/ _` | '_ \ 
 | |__| |____) |     ____) | (_| (_| | | | |
  \____/|_____/     |_____/ \___\__,_|_| |_|
                                                         
""")
print(f"  Developed by {Fore.RED}5O4R3S{Style.RESET_ALL} to exploit OutSystems developers' technical debt. | For contact https://soarescorp.com/")
print(f"  {Fore.WHITE}{Style.DIM}Do not run this tool in environments where you are not authorized, you are responsible for your actions. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.{Style.RESET_ALL}")
print(f"\n")
print(f"{Fore.WHITE}[i] {commons.get_current_datetime()} The analysis is starting...{Style.RESET_ALL}")

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36"
}

def exploit_modules(data,environment,app_module_name):
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for module informations...{Style.RESET_ALL}")
    get_AppDefinitions.get_app_definitions(environment,app_module_name,header)

    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for mobile applications in the environment...{Style.RESET_ALL}")
    get_MobileApp.get_mobile_apps(environment,header)
    
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for available screens in the application...{Style.RESET_ALL}")
    get_Screens.get_all_pages(data,environment)
    
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for dependencies in the application...{Style.RESET_ALL}")
    get_ModulesReferences.get_module_references(environment,app_module_name,header)
    
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for public files or in the resources folder...{Style.RESET_ALL}")
    get_Resources.get_all_resources(data,environment)
    
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] {commons.get_current_datetime()} Searching for ClientVariables in the application...{Style.RESET_ALL}")
    get_ClientVariables.get_all_clientvaribles(environment,app_module_name,header)
    
    
    get_EndScope.scan_completed()
    
# Sending a GET request to the URL
response = requests.get(module_informations_url, headers=header)

# Checking the response code
if response.status_code == 200:
    # The request was successful
    # Reading JSON content
    data = response.json()

    # Application is online
    print(f"{Fore.WHITE}[i] {commons.get_current_datetime()} The '{app_module_name}' module is online.{Style.RESET_ALL}")

    # Calling modules
    exploit_modules(data,environment,app_module_name)
else:
    # The request failed
    # Printing the response code and error message
    # Print the key normally
    print(f"{Fore.RED}There was a problem trying to access the url, more details below:{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.DIM}osscan.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")