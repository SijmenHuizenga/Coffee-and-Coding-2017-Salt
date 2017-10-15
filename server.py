from flask import Flask, request, jsonify
import urllib.request
import re
import htmlcleaner

app = Flask(__name__)

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@app.route('/analyse')
def analyse():
    url = request.args.get('url', default="")
    valid_url = regex.search(url)
    if url and valid_url:
        try:
            html = get_html_as_string(url)
        except FileNotFoundError:
            return "Url ont found", 404
        parsed = htmlcleaner.parsehtml(html)
        return jsonify(parsed)
    else:
        return "400", 400


def get_html_as_string(url):
    try:
        opener = urllib.request.FancyURLopener({})
        f = opener.open(url)
        content = f.read()
        return content.decode('utf-8')
    except Exception:
        raise FileNotFoundError


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
