import os
from flask import Flask, jsonify, Response
import requests

app = Flask(__name__)
SESSION = requests.Session()

ACTIVATE_URL = 'https://tv.teleclub.xyz/api/activar'
LIST_URL     = 'https://tv.teleclub.xyz/tv/lista.m3u'

@app.route('/activate')
def activate():
    resp = SESSION.get(ACTIVATE_URL)
    resp.raise_for_status()
    try:
        return jsonify(resp.json())
    except ValueError:
        return jsonify({"result": resp.text})

@app.route('/playlist')
def playlist():
    resp = SESSION.get(LIST_URL)
    resp.raise_for_status()
    return Response(resp.text, mimetype='application/x-mpegURL')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
