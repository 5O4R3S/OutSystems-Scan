from colorama import Fore, Style

# Open wordlist file
with open("wordlist/ScreenNames.txt", "r") as file_screen_wordlist:
    # read content of file
    wordlist_screen_names = file_screen_wordlist.readlines()

# Close file
file_screen_wordlist.close()

# Remove spaces between words
wordlist_screen_names = [word.strip() for word in wordlist_screen_names]

def check_screenName(screen_name):
    for word in wordlist_screen_names:
       if word.lower() in screen_name.lower():
           return True
    return False

def get_all_pages(data,environment_url,app_name):
    # No comments
    potential_screen_found = False

    print(f"{Fore.WHITE}[-] ==============================={Style.RESET_ALL}")
    print(f"{Fore.WHITE}[-] ==> ALL PAGES AND TEST PAGES =={Style.RESET_ALL}")
    print(f"{Fore.WHITE}[-] ==============================={Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}[i] Searching for pages available in the application...{Style.RESET_ALL}")

    # Extrair a lista "urlMappings"
    url_mappings = data["manifest"]["urlMappings"]
    print(f"{Fore.WHITE}[-] List of screens discovered in '{app_name}' module:{Style.RESET_ALL}")
    # Acessar as chaves do dicionário
    for key in url_mappings.keys():
        # Verificar se a palavra "moduleservices" está na chave
        if "moduleservices" not in key.lower():
            # Verificar se a palavra "test" ou "testes" está na chave
            if check_screenName(key.lower()):
                # Imprimir a chave em verde
                print(f"{Fore.YELLOW}{Style.BRIGHT}[+] [WARNING] {environment_url}{key}{Style.RESET_ALL}")
                if not potential_screen_found:
                    potential_screen_found = True
            else:
                # Imprimir a chave normalmente
                print(f"[-] {Fore.WHITE}{Style.DIM}[200] {environment_url}{key}{Style.RESET_ALL}")
    if potential_screen_found:
        print(f"{Fore.RED}{Style.BRIGHT}[i] Potentially vulnerable test screens were found in{Style.RESET_ALL} {Fore.YELLOW}{Style.BRIGHT}yellow{Style.RESET_ALL} {Fore.RED}{Style.BRIGHT}above.{Style.RESET_ALL}")
        print(f"{Fore.RED}[i] Soon you will be able to use other commands to perform a full page scan.{Style.RESET_ALL}")