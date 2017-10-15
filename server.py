from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import re
import htmlcleaner
from custom_errors import *
import CSR

app = Flask(__name__)
CORS(app)

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
    return analyzeurl(url)


def analyzeurl(url):
    valid_url = regex.search(url)
    if not (url and valid_url):
        return "400", 400

    try:
        html = get_html_as_string(url)
    except FileNotFoundError:
        return "Url ont found", 404

    try:
        parsed = htmlcleaner.parsehtml(html)
        point_string = ' '.join(parsed[1])
        points = CSR.csr(point_string) + CSR.csr(parsed[0])
        print(points)
        return response_to_json(parsed, points)
    except CustomFrameError as e:
        print("going to " + e.get_url())
        return analyzeurl(e.get_url())
    except Exception as e:
        print(e)
        return "500", 500


def response_to_json(parsed, points):
    # return jsonify(parsed, points)
    return jsonify({'points': points, 'lines': parsed})


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
