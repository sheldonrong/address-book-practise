import base64
from flask import jsonify, abort, make_response


def get_unique_filename(filename):
    return base64.b64encode(
        bytearray(filename, encoding='utf-8')
    ).decode('utf-8')


def decode_unique_filename(filename):
    return base64.b64decode(bytearray(filename, encoding='utf-8')).decode('utf-8')


def allowed_file(filename):
    from config import get_config
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in get_config().ALLOWED_EXTENSIONS


def file_not_supported():
    abort(make_response(
        jsonify(message="The uploaded file does not exist or is not of supported type"),
        415
    ))
