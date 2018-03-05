import os
from address_book.model import db


class Config(object):
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    STATIC_FOLDER = 'frontend/static'
    STATIC_URL_PATH = '/frontend/static'
    UPLOAD_FOLDER = ''
    POSTGRES = {
        'user': 'postgres',
        'pw': '123456',
        'db': 'addressbook',
        'host': 'localhost',
        'port': '5432',
    }

    @classmethod
    def get_tmp_path(cls, filename):
        return os.path.join(cls.UPLOAD_FOLDER, filename)


class DevConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'tmp')


class ProdConfig(Config):
    DEBUG = False
    STATIC_FOLDER = 'frontend/build/static'
    STATIC_URL_PATH = '/frontend/build/static'
    UPLOAD_FOLDER = '/tmp'


def setup_app(app, config):
    # init database integration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % config.POSTGRES)

    db.init_app(app)

    # other settings
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

    return app


def get_config():
    env = os.environ.get('ADDRESSBOOK_ENV', None)
    if env == 'dev':
        return DevConfig
    else:
        return ProdConfig