import os
from flask import Flask, render_template, request, jsonify, abort, make_response
from flask.ext.migrate import Migrate
from config import DevConfig
from apis import api
from address_book.model import db

# init flask application
from utils import get_unique_filename

app = Flask(
    __name__,
    static_folder='frontend/static',
    static_url_path='/frontend/static'
)

@app.route('/')
def hello_world():
    return render_template('app.html', title='Address Book')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in DevConfig.ALLOWED_EXTENSIONS


def file_not_supported():
    abort(make_response(
        jsonify(message="The uploaded file does not exist or is not of supported type"),
        415
    ))


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


# init flask rest api application
api.init_app(app)

# init database integration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % DevConfig.POSTGRES
app.config['UPLOAD_FOLDER'] = DevConfig.UPLOAD_FOLDER
db.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
