import socket

def get_address(url):
  url = url.replace("https://","")
  try:
    host = socket.gethostbyname(url)
    ip_address = socket.gethostbyaddr(host)[0]
    return ip_address
  except socket.gaierror:
    return url
