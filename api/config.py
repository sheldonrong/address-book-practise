
class _Config(object):
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    UPLOAD_FOLDER = 'tmp'
    POSTGRES = {
        'user': 'postgres',
        'pw': '123456',
        'db': 'addressbook',
        'host': 'localhost',
        'port': '5432',
    }

class DevConfig(_Config):
    DEBUG = True


class ProdConfig(_Config):
    DEBUG = False
