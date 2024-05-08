from colorama import Fore, Style
import requests
import re

def get_all_clientvaribles(environment,app_module_name,header):

    potential_defaultvalue_found = False

    # Sending a GET request to the URL
    url = environment+'/'+app_module_name+'/scripts/'+app_module_name+'.clientVariables.js'
    response = requests.get(url, headers=header)

    # Checking the response code
    if response.status_code == 200:
        # Search for lines that begin with "return ClientVarsService."
        matching_lines = re.findall(r"^return clientVarsService\..*", response.text, flags=re.MULTILINE)

        for line in matching_lines:
            # Extract the items inside .getVariable()
            items = re.findall(r".getVariable\((.*?)\)", line)

            # Separate items
            for item in items:
                item_content = item.split(", ")
                if len(item.split(", ")) == 4:
                    print(f"| {Fore.WHITE}[200] {Fore.YELLOW}[WARNING] {item_content}{Style.RESET_ALL}")
                    if not potential_defaultvalue_found:
                        potential_defaultvalue_found = True
                else:
                    print(f"| {Fore.WHITE}[200] {Style.DIM}{item_content}{Style.RESET_ALL}")
    else:
        # Error in request
        print(f"{Fore.RED}{Style.DIM}get_clientvariables.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")
    
    if potential_defaultvalue_found:
        print(f"{Fore.RED}[i] Potential default values found in one or more ClientVar listed in{Style.RESET_ALL} {Fore.YELLOW}yellow{Style.RESET_ALL} {Fore.RED}above.{Style.RESET_ALL}")