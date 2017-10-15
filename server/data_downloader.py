import re
import urllib.request
import glob
from html2object import parser

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
                    fa = opener.open(url, timeout=3)
                    content = fa.read()

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


def read_html(bases, base_folder):
    for base in bases:
        html_files = glob.glob(base)
        index = 1

        for path in html_files:
            file = open(path, errors="ignore")
            try:
                read = file.read()
            except UnicodeDecodeError as e:
                print(e)
                continue

            try:
                parsed = parser.parsehtml(read)
            except ValueError as e:
                print(e)
                continue

            if parsed:
                title = parsed[0]

                if title:
                    string = title + " "
                else:
                    string = ""
                # print(parsed[0])
                for s in parsed[1]:
                    string += s

                if string is not "" or string is not "NoneNone":
                    writer = open(base_folder + str(index) + '.txt', 'a+', errors="ignore")
                    try:
                        writer.write(string)
                    except UnicodeEncodeError as e:
                        print(e)
                        continue
                else:
                    print("Empty index " + str(index))
            index = index + 1

            # except Exception as e:
            #     print('something went wrong')


# read_html(["./data/html-ncsr1/*.html", "./data/html-ncsr2/*.html"], './text/ncsr/')
# read_html(["./data/html-csr1/*.html", "./data/html-csr2/*.html"], './text/csr/')

# writer = open('./data/test.html', 'a+')
# writer.write("wri")
# start()
