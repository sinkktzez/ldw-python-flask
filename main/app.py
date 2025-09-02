# Importando o Flask
from flask import Flask, render_template
# Importando o Controller
from controllers import routes
# Importando os Models
from models.database import db
# Importando a biblioteca para manipulação do S.O.
import os

# Criando uma instância do Flask
# A variável __name__ representa o nome da aplicação
app = Flask(__name__, template_folder='views')

routes.init_app(app)

# Extraindo o diretório absoluto absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Criando o arquivo do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')
 
# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # Enviando o Flask para SqlAlchemy
    db.init_app(app=app)
    # Verificar no inicio da apliacação se o BD já existe, senão, ele cria.
    with app.test_request_context():
        db.create_all()
    # Iniciando o servidor
    app.run(host='localhost', port=5000, debug=True)
