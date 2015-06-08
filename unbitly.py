from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import requests


app = Flask(__name__)


def follow_bitly(url):
    response = requests.head(url, allow_redirects=True)
    return response.url


@app.route('/follow', methods=['POST'])
def follow():
    bitly_url = request.get_json().get('url')
    return jsonify({
        'url': follow_bitly(bitly_url)
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
