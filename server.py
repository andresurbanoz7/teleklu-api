from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import os
import re

app = Flask(__name__)
CORS(app)

SESSION = requests.Session()

# URLs
WAUST_SCRIPT_URL = 'https://waust.at/d.js'
ACTIVATE_PAGE_URL = 'https://tv.teleclub.xyz/activar'
LIST_URL = 'https://tv.teleclub.xyz/tv/lista.m3u'

@app.route('/activate')
def activate():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tv.teleclub.xyz/activar"
    }

    try:
        # Ejecuta el script externo que activa (solo en navegador normalmente)
        script_resp = SESSION.get(WAUST_SCRIPT_URL, headers=headers)
        script_resp.raise_for_status()

        # Hace POST a la página de activación (simula formulario)
        activate_resp = SESSION.post(ACTIVATE_PAGE_URL, headers=headers)
        activate_resp.raise_for_status()

        # Busca si hay algún código visible en HTML
        match = re.search(r'Código de activación[:：]?\s*([A-Za-z0-9\-]+)', activate_resp.text, re.IGNORECASE)
        activation_code = match.group(1) if match else None

        return jsonify({
            "result": "ACTIVACIÓN EXITOSA (modo requests)",
            "code": activation_code
        })

    except Exception
