from colorama import Fore, Style
import requests
import re

compromised_component_list = [
    {"name": "UltimatePDF","Forge version":"12.0.1", "description": "Maybe it allows you to bypass forbidden 403 screens."},
    {"name": "ImageToolbox","Forge version":"2.1.1", "description": "Maybe vulnerable according to CVE-2016.3714."},
    {"name": "FroalaEditor","Forge version":"1.0.0", "description": "Perhaps vulnerable according to CVE-2023.41592 reported by LUCAS 5O4R3S."},
    {"name": "CK Editor 4","Forge version":"1.0.10", "description": "Perhaps vulnerable according to CVE-2022-24728."},
]

def check_compromised_component(component_name):
    # Accessing list elements
    for item in compromised_component_list:
        if item["name"].lower() == component_name.lower():
            print(f"| {Fore.WHITE}[200]{Style.RESET_ALL} {Fore.YELLOW}[WARNING] {item['name']} {item['description']}{Style.RESET_ALL}")
            return True
    return False

def get_module_references(environment,app_module_name,header):

    # Sending a GET request to the URL
    url = environment+'/'+app_module_name+'/scripts/'+app_module_name+'.referencesHealth.js'
    response = requests.get(url, headers=header)

    # Checking the response code
    if response.status_code == 200:
        # Split the string by lines
        lines = response.text.splitlines()

        # Find lines containing specific keys
        references_lines = [line for line in lines if "//" in line]

        # Regular expression to capture text in single quotes
        # e.g // Reference to producer 'HtmlRenderer' is OK return "HtmlRenderer"
        regex = r"'(.*?)'"

        # Extract values
        for lines in references_lines:
            # Extract text using regular expression
            module_name_filtered = re.findall(regex, lines)[0]

            # Check compromised components
            result = check_compromised_component(module_name_filtered)

            # Print informations
            if not result:
                # Print informations without warnings
                print(f"| {Fore.WHITE}[200] {Style.DIM}{module_name_filtered}{Style.RESET_ALL}")
            
    else:
        # Error in request
        print(f"{Fore.RED}{Style.DIM}get_modulesreferences.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")