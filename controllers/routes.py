from flask import render_template


def init_app(app):
    # Definindo a rota principal da aplicação '/'
    @app.route('/')
    def home():  # Função que será executada ao acessar a rota
        return render_template('index.html')

    @app.route('/games')
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        players = ['Yan', 'Ferrari', 'Valéria', 'Amanda']
        # Dicionário em python (Objeto)
        console = {'Nome': 'Playstation 5', 'Fabricante': 'Sony', 'Ano': 2020}
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)
