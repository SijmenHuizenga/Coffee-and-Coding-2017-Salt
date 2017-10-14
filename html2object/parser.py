import re
try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser
htmler = HTMLParser()


def parsehtml(html):
    bodies = find_tags_content(html, "body")
    if len(bodies) == 0:
        raise ValueError('No body tag found')
    html = bodies[0]

    html = html.replace("\r", "\n")
    html = re.sub(r"[\s]+", " ", html)

    html = dolooped(remove_everything_between, html, "<!--", "-->")
    html = dolooped(remove_everything_between, html, "<script", "</script>")
    html = dolooped(remove_everything_between, html, "<style", "</style>")

    for p in find_tags_content(html, "p"):
        if containstag(p, "div") or containstag(p, "input") or containstag(p, "textarea") or re.match(r"^[\d\s]*$", p):
            continue
        p = remove_tags(p).strip()
        if " " not in p:
            continue
        p = htmler.unescape(p)  # to get rid of   &#8216;
        print(p)

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


def find_tags_content(text, tagname):
    leftneedle = re.compile("<"+tagname+"[^>]*>")
    rightneedle = re.compile("<\/"+tagname+">")

    index = 0
    out = []

    while index < len(text):
        searchtext = text[index:]
        leftsearch = re.search(leftneedle, searchtext)
        if leftsearch is None:
            break

        rightsearch = re.search(rightneedle, searchtext[leftsearch.end():])

        if rightsearch is None:
            break

        out.append(searchtext[leftsearch.end():leftsearch.end()+rightsearch.start()])
        index += leftsearch.end()+rightsearch.end()
    return out


def containstag(text, tagname):
    return contains_fulltag(text, tagname) or contains_simpletag(text, tagname)


def contains_simpletag(text, tagname):
    regexr = re.compile("<"+tagname+"[^\/]+\/>")
    return re.search(regexr, text) is not None


def contains_fulltag(text, tagname):
    leftneedle = re.compile("<"+tagname+"[^>]*>")
    rightneedle = re.compile("<\/"+tagname+">")

    leftsearch = re.search(leftneedle, text)
    if leftsearch is None:
        return False

    rightsearch = re.search(rightneedle, text[leftsearch.end():])

    if rightsearch is None:
        return False
    return True


def remove_tags(text):
    return re.sub(r"<[^>]+>", "", text)

# testing code
with open('example.html', 'r') as myfile:
    data = myfile.read()
parsehtml(data)

# parsehtml("123<!-- this is the app -->456<style>   </style>789")
