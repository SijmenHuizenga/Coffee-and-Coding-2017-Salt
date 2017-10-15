import re
from custom_errors import *

with open('englishwords') as wordfile:
    mostusedwords = wordfile.readlines()

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser
htmler = HTMLParser()


class AstNode:
    tagname = None
    tagprops = None
    tagbody = None
    tagchilds = []

    def __init__(self, tagname, tagprops, tagbody, tagchilds):
        self.tagname = tagname
        self.tagprops = tagprops
        self.tagbody = tagbody
        self.tagchilds = tagchilds


def parsehtml(html):
    try:
        htmlbody = find_body(html)
    except ValueError as e:
        if not (containstag(html, "frame") or containstag(html, "iframe")):
            raise e
        src = re.search(r"src=\"([^\"]+)\"", html)
        if not src:
            raise e
        raise CustomFrameError(src.group(1))

    cleanedbody = remove_nontext_arias(htmlbody)  # remove things like scripts and style things
    tags = find_usefull_tags(cleanedbody)  # gives (name, props, body)
    ast = make_ast(tags)
    printast("", ast)

    paragraphs = []

    for astnode in ast:
        if not ast_contains_p(astnode.tagchilds):
            continue
        if ast_count_p_span_morethan_5_words(astnode.tagchilds) <= 2:
            continue
        if count_p_span_words(astnode.tagchilds) > 40:
            paragraphs.extend(ast2paragraphs(astnode.tagchilds))
            paragraphs.extend("\n")

    ast.sort(key=lambda x: count_p_span_words(x.tagchilds), reverse=True)
    title = ast[0].tagbody

    return title, paragraphs


def make_ast(tags):
    depthdict = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 5, "p": 7, "span": 7}

    leveldict = {0: AstNode(None, None, None, []), 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}

    for (tagname, tagprops, tagbody) in tags:
        taglevel = depthdict[tagname]
        parentlevel = taglevel

        while True:
            if parentlevel == 0:
                break
            parentlevel -= 1
            if leveldict[parentlevel] is not None:
                break
        newasttag = AstNode(tagname, tagprops, tagbody, [])
        if leveldict[parentlevel] is None:
            leveldict[parentlevel] = newasttag
            continue
        leveldict[parentlevel].tagchilds.append(newasttag)  # add to parent
        leveldict[parentlevel+1] = newasttag
        for i in range(parentlevel+2, 8):
            leveldict[i] = None

    return leveldict[0].tagchilds


def printast(prefix, ast):
    for astnode in ast:
        print(prefix + astnode.tagname + ":" + astnode.tagbody)
        printast(prefix+" -> ", astnode.tagchilds)


def ast2paragraphs(ast):
    out = []
    for astnode in ast:
        out.append(astnode.tagbody)
        out.extend(ast2paragraphs(astnode.tagchilds))
    return out


def count_p_span_words(ast):
    total = 0
    for astnode in ast:
        total += count_p_span_words(astnode.tagchilds)
        if not (astnode.tagname == "span" or astnode.tagname == "p"):
            continue
        total += len(astnode.tagbody.split())
    return total


def ast_contains_p(ast):
    for node in ast:
        if node.tagname == "span" or node.tagname == "p":
            return True
        if ast_contains_p(node.tagchilds):
            return True
    return False


def ast_count_p_span_morethan_5_words(ast):
    total = 0
    for node in ast:
        if node.tagname == "span" or node.tagname == "p":
            if len(node.tagbody.split()) > 5:
                total += 1
        total += ast_count_p_span_morethan_5_words(node.tagchilds)
    return total


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
    html = dolooped(remove_everything_between, html, "<svg", "</svg>")
    html = dolooped(remove_everything_between, html, "<footer", "</footer>")
    return html


def find_usefull_tags(html):
    # strictmode = len(find_tags(html, "h1")) > 1

    out = []
    for tag in find_tags(html, ["p", "span", "h1", "h2", "h3", "h4", "h5", "h6"]):
        tagname = tag[0]
        tagprops = tag[1]
        tagbody = tag[2]
        if (tagname == "p" or tagname == "span") and (
                            containstag(tagbody, "div")
                        or containstag(tagbody, "input")
                    or containstag(tagbody, "textarea")
                or re.match(r"^[\d\s]*$", tagbody)
        ):
            continue
        if len(find_tags(tagbody, "a")) >= 3:
            continue

        tagbody = re.sub(r" +", " ", remove_tags(tagbody).strip().lower())
        if " " not in tagbody:
            continue

        # if strictmode and not contains_english_word(tagbody):
        #     continue

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
        searches.sort(key=lambda x: x[1].start())

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
