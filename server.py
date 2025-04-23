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

# Simulación de activación sin navegador
@app.route('/activate')
def activate():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tv.teleclub.xyz/activar"
    }

    try:
        # Paso 1: Ejecutar script remoto que normalmente carga en el navegador
        script_resp = SESSION.get(WAUST_SCRIPT_URL, headers=headers)
        script_resp.raise_for_status()

        # Paso 2: Simular el POST al formulario de activación
        activate_resp = SESSION.post(ACTIVATE_PAGE_URL, headers=headers)
        activate_resp.raise_for_status()

        # Paso 3: Buscar código de activación (si es visible)
        match = re.search(r'Código de activación[:：]?\s*([A-Za-z0-9\-]+)', activate_resp.text, re.IGNORECASE)
        activation_code = match.group(1) if match else None

        return jsonify({
            "result": "ACTIVACIÓN EXITOSA (modo requests)",
            "code": activation_code
        })

    except Exception as e:
        return jsonify({
            "result": "ERROR EN LA ACTIVACIÓN",
            "details": str(e)
        }), 500

# Activación real con navegador (Playwright)
@app.route('/activate-browser')
def activate_browser():
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Ir a la página de activación y hacer clic
            page.goto("https://tv.teleclub.xyz/activar", timeout=15000)
            page.click('#activaID')  # Emula clic en el botón
            page.wait_for_timeout(5000)  # Espera que la activación se complete

            # Ir a la lista .m3u y capturar su contenido
            page.goto("https://tv.teleclub.xyz/tv/lista.m3u", timeout=15000)
            lista = page.content()

            browser.close()
            return Response(lista, mimetype='application/x-mpegURL')

    except Exception as e:
        return jsonify({
            "error": "Error al activar usando navegador Playwright",
            "details": str(e)
        }), 500

# Obtener la lista directamente (requiere activación previa)
@app.route('/playlist')
def playlist():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tv.teleclub.xyz/activar"
    }

    try:
        resp = SESSION.get(LIST_URL, headers=headers)
        resp.raise_for_status()
        return Response(resp.text, mimetype='application/x-mpegURL')

    except Exception as e:
        return jsonify({
            "error": "No se pudo obtener la lista",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
