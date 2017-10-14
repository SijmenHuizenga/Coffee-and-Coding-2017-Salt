from flask import Flask, request

app = Flask(__name__)


@app.route('/analyse')
def analyse():
    url = request.args.get('url', default="")

    if url:
        return url
    else:
        return "400", 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
