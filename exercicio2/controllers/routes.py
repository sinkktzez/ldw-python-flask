from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import requests 

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

fotos = [
    {'Título': 'Reflexos', 'Ano': 2023, 'Descrição': 'O Rio Ribeira refletindo o céu em suas águas', 'Imagem': '/static/uploads/IMG_20230617_155733.jpg'},
    {'Título': 'Conexão', 'Ano': 2022, 'Descrição': 'Ponte Hiroshi Sumida sob a luz de um lindo dia', 'Imagem': '/static/uploads/IMG_2530.jpg'}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/photos', methods=['GET', 'POST'])
    def photos():
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            ano = request.form.get('ano')
            descricao = request.form.get('descricao')
            file = request.files.get('imagem')

            filename = 'foto-default.jpg'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = f"/static/uploads/{filename}"

            if titulo and ano and descricao:
                fotos.append({
                    'Título': titulo,
                    'Ano': ano,
                    'Descrição': descricao,
                    'Imagem': filename
                })
                return redirect(url_for('photos'))

        return render_template('photos.html', fotos=fotos)

    @app.route('/newphoto', methods=['GET', 'POST'])
    def newphoto():
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            ano = request.form.get('ano')
            descricao = request.form.get('descricao')
            file = request.files.get('imagem')

            filename = 'foto-default.jpg'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = f"/static/uploads/{filename}"

            if titulo and ano and descricao:
                fotos.append({
                    'Título': titulo,
                    'Ano': ano,
                    'Descrição': descricao,
                    'Imagem': filename
                })
                return redirect(url_for('newphoto'))

        return render_template('newphoto.html', fotos=fotos)

    @app.route('/catalog')
    def catalog():
        response = requests.get("https://picsum.photos/v2/list?page=1&limit=1000")
        fotos_api = response.json()
        return render_template("catalog.html", fotos=fotos_api)

    @app.route('/catalogdetail/<int:foto_id>')
    def catalogdetail(foto_id):
        response = requests.get(f"https://picsum.photos/id/{foto_id}/info")
        foto = response.json()
        return render_template("catalogdetail.html", foto=foto)
