import socket

def get_address(url):
    url = url.replace("https://", "").replace("http://", "")
    try:
        host = socket.gethostbyname(url)
        try:
            ip_address = socket.gethostbyaddr(host)[0]  # Try to get the PTR record (reverse DNS)
            return ip_address
        except socket.herror:  # If no PTR record is found
            return "Not found!"
    except socket.gaierror:  # If the domain can't be resolved, return the URL
        return url

