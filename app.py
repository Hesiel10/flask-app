from flask import Flask, render_template, request, make_response, redirect, url_for
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Obtener las cookies de preferencias y enlaces visitados
    font = request.cookies.get('font', 'Arial')
    color = request.cookies.get('color', '#000000')
    visited_links = request.cookies.get('visited_links', '')

    # Convertir los enlaces visitados en una lista
    visited_links = visited_links.split(',') if visited_links else []

    return render_template('index.html', font=font, color=color, visited_links=visited_links)

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    font = request.form.get('font')
    color = request.form.get('color')

    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    resp = make_response(redirect(url_for('index')))  # Redirigir en lugar de renderizar directamente

    resp.set_cookie('font', font, expires=expires)
    resp.set_cookie('color', color, expires=expires)

    return resp

@app.route('/visit_link/<path:link>')  # Se usa <path:link> para manejar URLs completas
def visit_link(link):
    visited_links = request.cookies.get('visited_links', '')

    # Convertir la cadena de enlaces en una lista
    visited_links = visited_links.split(',') if visited_links else []

    if link not in visited_links:
        visited_links.append(link)

    resp = make_response(redirect(url_for('index')))  # Redirigir para actualizar la vista
    resp.set_cookie('visited_links', ','.join(visited_links), expires=datetime.datetime.now() + datetime.timedelta(days=30))

    return resp

if __name__ == '__main__':
    app.run(debug=True)
