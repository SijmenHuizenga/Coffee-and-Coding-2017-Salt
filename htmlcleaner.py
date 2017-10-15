import re

with open('englishwords.txt') as wordfile:
    mostusedwords = wordfile.readlines()

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser
htmler = HTMLParser()


def parsehtml(html):
    try:
        htmlbody = find_body(html)  # find the body
    except ValueError as e:
        raise ValueError(e)

    cleanedbody = remove_nontext_arias(htmlbody)  # remove things like scripts and style things
    tags = find_usefull_tags(cleanedbody)  # gives (name, props, body)

    title = None
    paragraphs = []

    for tag in tags:
        if title is None:
            if tag[0] == "p":
                continue
            if tag[0] == "h1" or tag[0] == "h2":
                title = tag[2]
                continue
        if len(paragraphs) != 0 and (tag[0] == "h1" or tag[0] == "h2" or tag[0] == "h3"):
            break
        paragraphs.append(tag[2])
    return title, paragraphs


def find_body(html):
    bodies = find_tags(html, ["body"])
    if len(bodies) == 0:
        raise ValueError('No body tag found')
    return bodies[0][2]


def remove_nontext_arias(html):
    html = html.replace("\r", "\n")
    html = re.sub(r"[\s]+", " ", html)

    html = dolooped(remove_everything_between, html, "<!--", "-->")
    html = dolooped(remove_everything_between, html, "<script", "</script>")
    html = dolooped(remove_everything_between, html, "<style", "</style>")
    return html


def find_usefull_tags(html):
    strictmode = len(find_tags(html, "h1")) > 1

    out = []
    for tag in find_tags(html, ["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        tagname = tag[0]
        tagprops = tag[1]
        tagbody = tag[2]
        if tagname == "p" and (
                            containstag(tagbody, "div")
                        or containstag(tagbody, "input")
                    or containstag(tagbody, "textarea")
                or re.match(r"^[\d\s]*$", tagbody)
        ):
            continue

        tagbody = re.sub(r" +", " ", remove_tags(tagbody).strip().lower())
        if " " not in tagbody:
            continue

        if strictmode and not contains_english_word(tagbody):
            continue

        out.append((tagname, tagprops, htmler.unescape(tagbody)))
    return out


def contains_english_word(text):
    for w in mostusedwords:
        if " " + w + " " in text or text.startswith(w + " ") or text.endswith(" " + w):
            return True
    return False


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

    rightstart = text.find(rightneedle, leftstart + len(leftneedle))

    if rightstart == -1:
        return text

    return text[:leftstart] + text[rightstart + len(rightneedle):]


def find_tags(text, tags):
    index = 0
    out = []

    while index < len(text):
        searchtext = text[index:]

        searches = []

        for tagname in tags:
            leftneedle = re.compile("<" + tagname + "([^>])*>")
            rightneedle = re.compile("<\/" + tagname + ">")

            leftsearch = re.search(leftneedle, searchtext)
            if leftsearch is None:
                continue

            rightsearch = re.search(rightneedle, searchtext[leftsearch.end():])

            if rightsearch is None:
                continue
            searches.append((tagname, leftsearch, rightsearch))
        if len(searches) == 0:
            break
        searches.sort(key= lambda x: x[1].start())

        tagname = searches[0][0]
        leftsearch = searches[0][1]
        rightsearch = searches[0][2]

        out.append((
            tagname,
            leftsearch.group(1),
            searchtext[leftsearch.end():leftsearch.end() + rightsearch.start()]
        ))
        index += leftsearch.end() + rightsearch.end()
    return out


def containstag(text, tagname):
    return contains_fulltag(text, tagname) or contains_simpletag(text, tagname)


def contains_simpletag(text, tagname):
    regexr = re.compile("<" + tagname + "[^\/]+\/>")
    return re.search(regexr, text) is not None


def contains_fulltag(text, tagname):
    leftneedle = re.compile("<" + tagname + "[^>]*>")
    rightneedle = re.compile("<\/" + tagname + ">")

    leftsearch = re.search(leftneedle, text)
    if leftsearch is None:
        return False

    rightsearch = re.search(rightneedle, text[leftsearch.end():])

    if rightsearch is None:
        return False
    return True


def remove_tags(text):
    return re.sub(r"<[^>]+>", "", text)
