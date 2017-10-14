import re
import urllib.request
import socket
socket.setdefaulttimeout(3)

csv_link = 'csr2'

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def start():
    with open(csv_link) as csfile:
        content = csfile.readlines()

        index = 1
        for line in content:
            url = "http://" + line.replace('"', "").strip()
            valid = regex.search(url)
            opener = urllib.request.FancyURLopener({})

            if valid:
                try:
                    print(url)
                    opener.retrieve(url, './data/'+str(index)+'.html')
                    print("done")
                except Exception as e:
                    print(e)
                index = index + 1


# writer = open('./data/test.html', 'a+')
# writer.write("wri")
start()