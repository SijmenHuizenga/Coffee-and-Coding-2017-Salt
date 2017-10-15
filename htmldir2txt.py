import glob
import htmlcleaner

htmldirs = ["./data/html-ncsr1/*.html", "./data/html-ncsr2/*.html"]
# htmldirs = ["./data/html-csr1/*.html", "./data/html-csr2/*.html"]

outputdir = './text/ncsr/'
# outputdir = './text/csr/'


for htmldir in htmldirs:
    html_files = glob.glob(htmldir)
    index = 1

    for path in html_files:
        file = open(path, errors="ignore")
        try:
            read = file.read()
        except UnicodeDecodeError as e:
            print(e)
            continue

        try:
            parsed = htmlcleaner.parsehtml(read)
        except ValueError as e:
            print(e)
            continue

        if not parsed:
            title = parsed[0]

            if title:
                string = title + " "
            else:
                string = ""
            for s in parsed[1]:
                string += s

            if string is not "" or string is not "NoneNone":
                writer = open(htmldir + str(index) + '.txt', 'a+', errors="ignore")
                try:
                    writer.write(string)
                except UnicodeEncodeError as e:
                    print(e)
                    continue
            else:
                print("Empty index " + str(index))
        index = index + 1

