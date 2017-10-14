from flask import Flask, request, jsonify
import urllib.request
from html2object import parser

app = Flask(__name__)


@app.route('/analyse')
def analyse():
    url = request.args.get('url', default="")

    if url:
        html = get_html_as_string(url)
        parsed = parser.parsehtml(html)
        print(parsed)
        return jsonify(parsed)
    else:
        return "400", 400


def get_html_as_string(url):
    opener = urllib.request.FancyURLopener({})
    # url = "http://stackoverflow.com/"
    url = url
    f = opener.open(url)
    content = f.read()
    return content


# def test():
#     opener = urllib.request.FancyURLopener({})
#     url = "http://stackoverflow.com/"
#     f = opener.open(url)
#     content = f.read()
#     return content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
