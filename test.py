import htmlcleaner

with open('example.html', 'r') as myfile:
    data = myfile.read()
(t, p) = htmlcleaner.parsehtml(data)
print("TITLE: " + t)
for line in p:
    print(line)