from flask import abort
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests


app = Flask(__name__)
app.debug = True


def follow_bitly(url):
    try:
        response = requests.head(url, allow_redirects=True)
    except requests.exceptions.MissingSchema:
        return None
    if response.status_code == 200:
        return response.url
    else:
        return None


@app.route('/follow', methods=['POST'])
def follow():
    try:
        bitly_url = request.get_json().get('url')
    except AttributeError:
        abort(400)

    url = follow_bitly(bitly_url)
    if not url:
        abort(404)

    return jsonify({
        'url': url
    })


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(e):
    return '', 404


@app.errorhandler(400)
def invalid_request(e):
    return '', 400


if __name__ == '__main__':
    app.run(debug=True)
