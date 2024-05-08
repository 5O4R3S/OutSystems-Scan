from colorama import Fore, Style
import requests
import get_RealAddress

def get_app_definitions(environment,app_module_name,header):

    # Sending a GET request to the URL
    url = environment+'/'+app_module_name+'/scripts/'+app_module_name+'.appDefinition.js'
    response = requests.get(url, headers=header)

    # Checking the response code
    if response.status_code == 200:
        # Split the string by lines
        lines = response.text.splitlines()

        # Find lines containing specific keys
        environment_key_line = [line for line in lines if "environmentKey:" in line][0]
        environment_name_line = [line for line in lines if "environmentName:" in line][0]
        application_name_line = [line for line in lines if "applicationName:" in line][0]
        application_key_line = [line for line in lines if "applicationKey:" in line][0]
        user_provider_line = [line for line in lines if "userProviderName:" in line][0]
        home_module_key_line = [line for line in lines if "homeModuleKey:" in line][0]

        # Extract values
        environment_key = environment_key_line.split(":")[1].strip().strip('"').strip(',')[:-1]
        environment_name = environment_name_line.split(":")[1].strip().strip('"').strip(',')[:-1]
        application_name = application_name_line.split(":")[1].strip().strip('"').strip(',')[:-1]
        application_key = application_key_line.split(":")[1].strip().strip('"').strip(',')[:-1]
        user_provider = user_provider_line.split(":")[1].strip().strip('"').strip(',')[:-1]
        home_module_key = home_module_key_line.split(":")[1].strip().strip('"').strip(',')[:-1]

        # Print informations
        print(f"| {Fore.WHITE}Application: {Style.DIM}[NAME={application_name} KEY={application_key}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}Environment: {Style.DIM}[NAME={environment_name} KEY={environment_key}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}User tenant provider: {Style.DIM}{user_provider}{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}Home module key: {Style.DIM}{home_module_key}{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}Real DNS (enterprise only): {Style.DIM}{get_RealAddress.get_address(environment)}/{app_module_name}{Style.RESET_ALL}")

        # Return
        return application_name
    else:
        # Error in request
        print(f"{Fore.RED}{Style.DIM}get_appdefinitions.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")