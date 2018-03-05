import os
from flask import render_template, request, jsonify, Flask
from flask_migrate import Migrate
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
        filename = get_unique_filename(file.filename)
        file.save(
            os.path.join(
                os.path.dirname(__file__),
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )
        return jsonify({
            'success': True,
            'file': filename
        })
    else:
        file_not_supported()


migrate = Migrate(app, db)
# init flask rest api application
api.init_app(app)

if __name__ == '__main__':
    app.run()
