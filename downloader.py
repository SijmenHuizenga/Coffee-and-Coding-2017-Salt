import re
import urllib.request
import socket
socket.setdefaulttimeout(3)

linksfile = './testhtml/csr_data_12.csv'

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

opener = urllib.request.FancyURLopener({})

with open(linksfile) as f:
    links = f.readlines()

index = 1
for link in links:
    url = "http://" + link.replace('"', "").strip()
    if not regex.search(url):
        continue

    try:
        opener.retrieve(url, './data/'+str(index)+'.html')
        index = index + 1
    except Exception as e:
        print(e)
