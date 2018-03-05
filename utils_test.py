import base64

from mock import patch
from nose.tools import assert_equal, assert_true, assert_false
from utils import get_unique_filename, allowed_file


class TestUtils(object):

    @patch('time.time')
    def test_get_unique_filename(self, time_):
        # Setup
        time_.return_value = 11111122222

        # Execute
        filename = get_unique_filename('abc.txt')
        origin_filename = base64.b64decode(filename)\
            .decode('utf-8').split('|')

        # Verify
        assert_equal(len(origin_filename), 2)
        assert_equal(origin_filename[0], str(11111122222))
        assert_equal(origin_filename[1], 'abc.txt')

    def allowed_file(self):
        # Valid cases
        assert_true(allowed_file('a.csv'), True)
        assert_true(allowed_file('_@#b1.csv'), True)
        assert_true(allowed_file('a.txt'), True)
        assert_true(allowed_file('_@#b1.txt'), True)
        assert_true(allowed_file('_@#b1.csv'), True)

        assert_true(allowed_file('_@#b1'), False)
        assert_true(allowed_file('csv'), False)
        assert_true(allowed_file('txt'), False)
        assert_true(allowed_file('a.jpg'), False)

