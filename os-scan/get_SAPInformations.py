from colorama import Fore, Style
import requests
import json

def get_SapInformations(environment,header):

    url = environment+'/SAPDevService/rest/SAP/CheckSAPHealth'

    # Sending a GET request to the URL
    response = requests.get(url, headers=header)

    # Checking the response code
    if response.status_code == 200:
        # The request was successful
        data = response.json()

        is_sap_conect_presente = data["IsSAPConnectorPresent"]
        sap_conect_version = data["SapConnectorVersion"]

        # Print informations
        print(f"| {Fore.WHITE}SAP Connector: {Style.DIM}[{is_sap_conect_presente}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}SAP Connector Version: {Style.DIM}[{sap_conect_version}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}Exposed API documentation: {Style.DIM}[{environment}/SAPDevService/rest/SAP/]{Style.RESET_ALL}")
    else:
        # The request failed
        # Printing the response code and error message
        # Print the key normally
        print(f"{Fore.RED}There was a problem trying to access the url, more details below:{Style.RESET_ALL}")
        print(f"{Fore.RED}{Style.DIM}get_SAPInformations.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}")