from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/activate')
def activate():
    result = asyncio.run(activar_teleclub())
    return jsonify(result)

async def activar_teleclub():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("https://tv.teleclub.xyz/activar", timeout=30000)

            # Espera al botón y hace clic dos veces (como en el navegador)
            await page.wait_for_selector("img", timeout=10000)
            await page.click("img")
            await page.wait_for_timeout(3000)
            await page.click("img")

            # Espera el mensaje de activación (puedes ajustar el selector según la estructura real)
            await page.wait_for_selector("body", timeout=10000)
            texto = await page.inner_text("body")

            await browser.close()
            return {"status": "Activación completa", "mensaje": texto}

        except Exception as e:
            await browser.close()
            return {"status": "Error", "detalle": str(e)}

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 8080))
app.run(host='0.0.0.0', port=port)


