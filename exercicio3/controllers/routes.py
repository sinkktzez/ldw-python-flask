from flask import render_template, request, redirect, url_for, flash  
import requests
from werkzeug.utils import secure_filename  
from models.database import db, Foto, Album  
import os  
from math import ceil  
  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  
  
def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  
  
def init_app(app):  
  
    @app.route('/')  
    def home():  
        return render_template('index.html')  
  
    @app.route('/albuns')  
    def albuns():  
        page = request.args.get('page', 1, type=int)  
        per_page = 5  
        albuns_pag = Album.query.paginate(page=page, per_page=per_page, error_out=False)  
        return render_template('albuns.html', albuns=albuns_pag.items, pagination=albuns_pag)  
  
    @app.route('/album/new', methods=['GET', 'POST'])
    def newAlbum():
        if request.method == 'POST':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            if nome:
                album = Album(nome=nome, descricao=descricao)
                db.session.add(album)
                db.session.commit()
                flash("Álbum criado com sucesso!", "success")
                return redirect(url_for('photos', album_id=album.id))
        return render_template('newAlbum.html')  
  
    @app.route('/album/edit/<int:album_id>', methods=['GET', 'POST'])  
    def editAlbum(album_id):  
        album = Album.query.get_or_404(album_id)  
        if request.method == 'POST':  
            album.nome = request.form.get('nome')  
            album.descricao = request.form.get('descricao')  
            db.session.commit()  
            flash("Álbum atualizado com sucesso!", "success")  
            return redirect(url_for('albuns'))  
        return render_template('editAlbum.html', album=album)  
  
    @app.route('/album/delete/<int:album_id>', methods=['POST'])  
    def deleteAlbum(album_id):  
        album = Album.query.get_or_404(album_id)  
        db.session.delete(album)  
        db.session.commit()  
        flash("Álbum removido com sucesso!", "success")  
        return redirect(url_for('albuns'))  
  
    @app.route('/photos/<int:album_id>')  
    def photos(album_id):  
        page = request.args.get('page', 1, type=int)  
        per_page = 5  
        fotos_pag = Foto.query.filter_by(album_id=album_id).paginate(page=page, per_page=per_page, error_out=False)  
        album = Album.query.get_or_404(album_id)  
        return render_template('photos.html', fotos=fotos_pag.items, pagination=fotos_pag, album=album)  
  
    from flask import request, redirect, url_for, flash, render_template

    @app.route('/photo/new/<int:album_id>', methods=['GET', 'POST'])
    def newPhoto(album_id):
        album = Album.query.get_or_404(album_id)

        if request.method == 'POST':
            titulo = request.form.get('titulo')
            file = request.files.get('arquivo')

            if not titulo or not file:
                flash("Título e arquivo são obrigatórios!", "danger")
                return redirect(url_for('newPhoto', album_id=album_id))

            filename = secure_filename(file.filename)
            file.save(os.path.join('static/uploads', filename))

            foto = Foto(titulo=titulo, arquivo=filename, album_id=album_id)
            db.session.add(foto)
            db.session.commit()

            flash("Foto cadastrada com sucesso!", "success")
            return redirect(url_for('photos', album_id=album_id))

        return render_template('newPhoto.html', album=album)  
  
    @app.route('/photo/edit/<int:photo_id>', methods=['GET', 'POST'])  
    def editPhoto(photo_id):  
        foto = Foto.query.get_or_404(photo_id)  
        albuns = Album.query.all()  
        if request.method == 'POST':  
            foto.titulo = request.form.get('titulo')  
            foto.ano = request.form.get('ano', type=int)  
            foto.descricao = request.form.get('descricao')  
            foto.album_id = request.form.get('album_id', type=int)  
  
            file = request.files.get('imagem')  
            if file and allowed_file(file.filename):  
                filename_secure = secure_filename(file.filename)  
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))  
                foto.imagem = f"/static/uploads/{filename_secure}"  
  
            db.session.commit()  
            flash("Foto atualizada com sucesso!", "success")  
            return redirect(url_for('photos', album_id=foto.album_id))  
  
        return render_template('editPhoto.html', foto=foto, albuns=albuns)  
  
    @app.route('/photo/delete/<int:photo_id>', methods=['POST'])  
    def deletePhoto(photo_id):  
        foto = Foto.query.get_or_404(photo_id)  
        album_id = foto.album_id  
        db.session.delete(foto)  
        db.session.commit()  
        flash("Foto removida com sucesso!", "success")  
        return redirect(url_for('photos', album_id=album_id))

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