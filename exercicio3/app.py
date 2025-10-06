from flask import Flask
import os
from models.database import db

app = Flask(__name__, template_folder='views')
app.secret_key = "159753"

upload_folder = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:159753@localhost/fotografia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from controllers import routes
routes.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)