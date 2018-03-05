from apis.utils import get_csv_metadata_fields, get_csv_metadata_params
from nose.tools import assert_equal


class TestUtils(object):

    def test_get_csv_metadata_fields(self):
        # Execute
        fields = get_csv_metadata_fields(required=True)

        # Verify
        assert_equal(set(fields.keys()), {'delimiter', 'quotechar', 'has_header', 'encoding'})
        assert_equal(fields['delimiter'].enum, [' ', ';', ',', ':', '|'])
        assert_equal(fields['delimiter'].required, True)

        assert_equal(fields['quotechar'].enum, [" ", "\"", "\'"])
        assert_equal(fields['quotechar'].required, True)

        assert_equal(fields['has_header'].minimum, 0)
        assert_equal(fields['has_header'].maximum, 1)
        assert_equal(fields['has_header'].required, True)

        assert_equal(fields['encoding'].enum, [
            'ascii', 'utf-8', 'utf-16', 'cp1250', 'cp1251', 'cp1252', 'gbk'])
        assert_equal(fields['encoding'].required, True)

    def test_get_csv_metadata_params(self):
        # Execute
        parser = get_csv_metadata_params(required=True)

        # Verify
        assert_equal(len(parser.args), 4)
        assert_equal({arg.name for arg in parser.args}, {
            'quotechar', 'delimiter', 'encoding', 'has_header'
        })
