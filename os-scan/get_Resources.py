from colorama import Fore, Style
import re

# Open wordlist file
with open("wordlist/Extensions.txt", "r") as file_extensions_wordlist:
    # read content of file
    wordlist_extensions_names = file_extensions_wordlist.readlines()

# Close file
file_extensions_wordlist.close()

# Remove spaces between words
wordlist_extensions_names = [word.strip() for word in wordlist_extensions_names]

def check_extensions(extensions_name):
    for word in wordlist_extensions_names:
       if word.lower() in extensions_name.lower():
           return True
    return False


keys_not_allowed = r"(/css/|/scripts/|/fonts/|/img/|/moduleservices/)"

def get_all_resources(data,environment_url):
    potential_extensions_found = False
    
    # Extract a list of available "urlVersions"
    url_mappings = data["manifest"]["urlVersions"]
    
    # Access the dictionary keys created above
    for key in url_mappings.keys():
        if not re.search(keys_not_allowed, key):
            if check_extensions(key.lower()):
                # Print resources files founded
                print(f"| {Fore.WHITE}[200]{Style.RESET_ALL} {Fore.YELLOW}[WARNING] {environment_url}{key}{Style.RESET_ALL}")
                if not potential_extensions_found:
                        potential_extensions_found = True
            else:
                print(f"| {Fore.WHITE}[200] {Style.DIM}{environment_url}{key}{Style.RESET_ALL}")
    if potential_extensions_found:
        print(f"{Fore.RED}[i] Potential exploitable file found and listed in{Style.RESET_ALL} {Fore.YELLOW}yellow{Style.RESET_ALL} {Fore.RED}above.{Style.RESET_ALL}")
                
