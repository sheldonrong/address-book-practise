import tempfile
from flask import render_template, request, jsonify, Flask
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix
from config import setup_app, get_config
from address_book.model import db
from utils import get_unique_filename, file_not_supported, allowed_file
from apis import api

# Initialise Flask
config = get_config()
app = Flask(
    __name__,
    static_folder=config.STATIC_FOLDER,
    static_url_path=config.STATIC_URL_PATH
)
app = setup_app(app, config)


@app.route('/')
def main():
    return render_template('app.html', title='Address Book')


@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files or not request.files['file']:
        file_not_supported()
    file = request.files['file']
    if file and allowed_file(file.filename):
        # disable temp folder auto deletion
        with tempfile.NamedTemporaryFile(delete=False) as t:
            file.save(t)
            return jsonify({
                'success': True,
                'file': get_unique_filename(t.name)
            })
    else:
        file_not_supported()


migrate = Migrate(app, db)
# init flask rest api application
api.init_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app) # fix https issue for api documentation

if __name__ == '__main__':
    app.run()
