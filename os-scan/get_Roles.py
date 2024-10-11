from colorama import Fore, Style
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_roles_os11(response_text):

    pattern = r'^roleException: new OS\.Exceptions\.Exceptions\.NotRegisteredException\(".*'
    
    # Search for lines that begin with "return ClientVarsService."
    matching_lines = re.findall(pattern, response_text, flags=re.MULTILINE)

    for line in matching_lines:
            # Extract the items inside .getVariable()
        items = re.search(r'\("(.*?)"\)', line)

        if items:
            roles = items.group(1).split(",")[0].strip().replace(".Not"," --> [Role Name: ").replace("\"","")
            print(f"| {Fore.WHITE}{Style.DIM}Supplier module: {roles}]{Style.RESET_ALL}")

def get_roles_odc(response_text):
    pattern = r'^roleException: new OS\.Exceptions\.Exceptions\.NotRegisteredException\(".*'
    
    # Search for lines that begin with "return ClientVarsService."
    matching_lines = re.findall(pattern, response_text, flags=re.MULTILINE)

    for line in matching_lines:
            # Extract the items inside .getVariable()
        items = re.search(r'\("(.*?)"\)', line)

        if items:
            roles = items.group(1).split(",")[0].strip().replace(".Not"," --> [Role Name: ").replace("\"","")
            print(f"| {Fore.WHITE}{Style.DIM}Supplier module: {roles}]{Style.RESET_ALL}")

def get_all_roles(environment,app_module_name,header):

    # Sending a GET request to the URL
    url = environment+'/'+app_module_name+'/scripts/'+app_module_name+'.controller.js'
    response = requests.get(url, headers=header, verify=False)

    # Checking the response code
    if response.status_code == 200:

        # Verify roles in OS11
        if "Controller.prototype.roles" in response.text:
            get_roles_os11(response.text)
        
        # Verify roles in OS11
        elif  "get roles()" in response.text:
            get_roles_odc(response.text)
        else:
            print(f"| {Fore.WHITE}[|||] {Style.DIM}Unable to find roles for this application.{Style.RESET_ALL}")
    else:
        # Error in request
        print(f"{Fore.RED}{Style.DIM}get_Roles.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")