from flask import Flask, jsonify, Response
from flask_cors import CORS        # ← añade esto
import requests
import os

app = Flask(__name__)
CORS(app)                          # ← y esto para habilitar CORS globalmente

SESSION = requests.Session()
ACTIVATE_URL = 'https://tv.teleclub.xyz/activar'
LIST_URL     = 'https://tv.teleclub.xyz/tv/lista.m3u'

@app.route('/activate')
def activate():
    # 1) Hace un POST a /activar para que Teleclub devuelva la cookie de activación
    resp = SESSION.post(ACTIVATE_URL)
    resp.raise_for_status()
    # 2) Si quieres ver el HTML de confirmación, podrías devolver resp.text,
    #    pero lo más limpio es devolver un JSON claro al cliente:
    return jsonify({ "result": "ACTIVACIÓN EXITOSA" })


@app.route('/playlist')
def playlist():
    resp = SESSION.get(LIST_URL)
    resp.raise_for_status()
    return Response(resp.text, mimetype='application/x-mpegURL')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
