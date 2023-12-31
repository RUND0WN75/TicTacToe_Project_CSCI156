import requests
import re
 
def get_external_ip():
    # Make a request to checkip.dyndns.org as proposed
    # in https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery#DNS_Addresses
    response = requests.get('http://checkip.dyndns.org').text
 
    # Filter the response with a regex for an IPv4 address
    ip = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response).group()
    return ip
 
external_ip = get_external_ip()
print(external_ip)