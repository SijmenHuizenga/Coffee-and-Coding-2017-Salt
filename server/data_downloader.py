import re
import urllib.request

csv_link = './testhtml/csr_data_12.csv'

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def start():
    with open(csv_link) as f:
        content = f.readlines()

        index = 1
        for line in content:
            url = "http://" + line.replace('"', "").strip()
            valid = regex.search(url)

            if valid:
                try:
                    opener = urllib.request.FancyURLopener({})
                    # url = "http://stackoverflow.com/"
                    f = opener.open(url)
                    content = f.read()

                    writer = open('./data/'+str(index)+'.html', 'a+')
                    try:
                        a = content.decode()
                        print(a)

                        if a:
                            writer.write(a)
                    except Exception as e:
                        print(e)

                    index = index + 1
                    # return content.decode('utf-8')
                except Exception:
                    raise FileNotFoundError


# writer = open('./data/test.html', 'a+')
# writer.write("wri")
start()