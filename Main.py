from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/noticias')
def obtener_noticias():
    url = 'https://www.investing.com/economic-calendar/'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    noticias = []
    filas = soup.select('tr.js-event-item')

    for fila in filas:
        pais = fila.get('data-country')
        importancia = fila.get('data-impact')
        fecha = fila.get('data-event-datetime')
        evento = fila.select_one('.event').get_text(strip=True)
        hora = fila.select_one('.time').get_text(strip=True)

        if pais != 'United States':
            continue

        importancia_texto = {
            '3': 'alta',
            '2': 'media',
            '1': 'baja'
        }.get(importancia, 'desconocida')

        noticias.append({
            'hora': hora,
            'evento': evento,
            'importancia': importancia_texto,
            'fecha': fecha[:10]
        })

    hoy = datetime.utcnow().strftime('%Y-%m-%d')
    noticias_hoy = [n for n in noticias if n['fecha'] == hoy]
    noticias_semana = [n for n in noticias if n['fecha'] != hoy]

    return jsonify({
        'hoy': noticias_hoy,
        'semana': noticias_semana
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
