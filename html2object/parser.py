import re


def parsehtml(html):
    html = get_everything_between_two_needles(html, re.compile("<body[^>]*>"), re.compile("<\/body>"))
    if html == -1:
        raise ValueError('No body tag found')

    html = html.replace("\r", "\n")
    html = re.sub(r"[\s]+", " ", html)

    html = dolooped(remove_everything_between, html, "<!--", "-->")
    html = dolooped(remove_everything_between, html, "<script", "</script>")
    html = dolooped(remove_everything_between, html, "<style", "</style>")

    print(html)
    return (
        "Title", ["paragraaf", "paragraaf"]
    )


def dolooped(func, *args):
    while True:
        new = func(*args)
        if args[0] == new:
            return new
        lst = list(args)
        lst[0] = new
        args = tuple(lst)


def remove_everything_between(text: str, leftneedle: str, rightneedle: str):
    leftstart = text.find(leftneedle)
    if leftstart == -1:
        return text

    rightstart = text.find(rightneedle, leftstart+len(leftneedle))

    if rightstart == -1:
        return text

    return text[:leftstart]+text[rightstart+len(rightneedle):]


def get_everything_between_two_needles(text, leftneedle, rightneedle):
    leftsearch = re.search(leftneedle, text)
    if leftsearch is None:
        print("left not found")
        return None

    rightsearch = re.search(rightneedle, text)

    if rightsearch is None:
        print("right not found")
        return None

    return text[leftsearch.end():rightsearch.start()]


# testing code
with open('example.html', 'r') as myfile:
    data = myfile.read()
parsehtml(data)

# parsehtml("123<!-- this is the app -->456<style>   </style>789")
