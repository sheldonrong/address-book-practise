import time
import base64

from werkzeug.utils import secure_filename


def get_unique_filename(filename):
    return base64.b64encode(
        bytearray(str(time.time()) + '|' + secure_filename(filename), encoding='utf-8')
    ).decode('utf-8')
