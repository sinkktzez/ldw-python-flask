from flask import Flask
import os

app = Flask(__name__, template_folder='views')

upload_folder = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

from controllers import routes
routes.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
