import glob
import htmlcleaner
import custom_errors

csr = True

if not csr:
    htmldirs = ["./server/data/html-ncsr1/*.html", "./server/data/html-ncsr2/*.html"]
    outputdir = './server/text/ncsr/'
else:
    htmldirs = ["./server/data/html-csr1/*.html", "./server/data/html-csr2/*.html"]
    outputdir = './server/text/csr/'


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
        except Exception as e:
            print(e)
            continue

        if parsed:
            title = parsed[0]

            if title:
                string = title + " "
            else:
                string = ""
            for s in parsed[1]:
                string += s

            if string is not "" or string is not "NoneNone":
                writer = open(outputdir + str(index) + '.txt', 'a+', errors="ignore")
                try:
                    writer.write(string)
                except UnicodeEncodeError as e:
                    print(e)
                    continue
            else:
                print("Empty index " + str(index))
        index = index + 1

