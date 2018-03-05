from werkzeug.exceptions import HTTPException

import app
from mock import patch
from nose.tools import assert_equal, assert_raises

from app import main, upload


class TestApp(object):

    @patch('app.render_template')
    def test_main(self, render_template):
        # Setup
        render_template.return_value = '<html />'

        # Execute
        main()

        # Verify
        render_template.assert_called_once_with('app.html', title='Address Book')

    def test_upload_without_files(self):
        # Execute
        with assert_raises(HTTPException):
            with app.app.test_request_context():
                upload()

