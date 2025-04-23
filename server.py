from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

SESSION = requests.Session()

# URL del script activador real
WAUST_ACTIVATOR_URL = 'https://waust.at/d.js'
LIST_URL = 'https://tv.teleclub.xyz/tv/lista.m3u'

@app.route('/activate')
def activate():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://tv.teleclub.xyz/activar"
        }

        # Carga del script externo (esto gatilla la activación en el navegador normalmente)
        resp = SESSION.get(WAUST_ACTIVATOR_URL, headers=headers)
        resp.raise_for_status()

        return jsonify({ "result": "Activación simulada correctamente (waust.at/d.js cargado)" })
    except Exception as e:
        return jsonify({ "error": "Falló la activación", "details": str(e) }), 500

@app.route('/playlist')
def playlist():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://tv.teleclub.xyz/activar"
        }

        resp = SESSION.get(LIST_URL, headers=headers)
        resp.raise_for_status()

        return Response(resp.text, mimetype='application/x-mpegURL')
    except Exception as e:
        return jsonify({ "error": "No se pudo obtener la lista", "details": str(e) }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
