import io
from mock import patch, mock_open
from address_book.exceptions import CannotDetermineCSVMappingError, FileInfoNotCompleteError, InvalidEmailAddress
from address_book.model import CSVHandler, AddressBook
from nose.tools import (
    assert_equal, assert_raises,
    assert_true, assert_false,
    assert_not_equal
)

from constants import ConflictsResolveStrategy


class TestCSVHandler(object):

    def test__guess_fieldnames_with_header_email_name(self):
        """should return fieldsname as ['email', 'name']"""
        result = CSVHandler._guess_fieldnames("""
            email name
            abc@google.com abc
            acd@yahoo.com acd
            def@outlook.com def""", ' ')
        assert_equal(result, ['email', 'name'])

    def test__guess_fieldnames_with_header_name_email(self):
        """should return fieldsname as ['name', 'email']"""
        result = CSVHandler._guess_fieldnames("""
            name email
            abc abc@google.com
            acd acd@yahoo.com
            def def@outlook.com""", ' ')
        assert_equal(result, ['name', 'email'])

    def test__guess_fieldnames_without_header_name_email(self):
        """should return fieldsname as ['name', 'email']"""
        result = CSVHandler._guess_fieldnames("""
            abc abc@google.com
            acd acd@yahoo.com
            def def@outlook.com""", ' ')
        assert_equal(result, ['name', 'email'])

    def test__guess_fieldnames_with_invalid_delimiter(self):
        """invalid delimiter, should raise exception"""
        with assert_raises(CannotDetermineCSVMappingError):
            CSVHandler._guess_fieldnames("""
                abc abc@google.com
                acd acd@yahoo.com
                def def@outlook.com""", ';')

    def test__guess_fieldnames_with_no_email(self):
        with assert_raises(CannotDetermineCSVMappingError):
            CSVHandler._guess_fieldnames("""
                abc aaaaa
                bbb bbbbb
                ccc ccccc
            """, ' ')

    def test__get_reader(self):
        """should return the space as delimiter and no header"""
        f = io.StringIO("""
            abc abc@google.com
            acd acd@yahoo.com
            def def@outlook.com"""
        )
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=')
        reader, has_header = handler._get_reader(f)
        assert_false(has_header)
        assert_equal(reader.dialect.delimiter, ' ')
        assert_equal(reader.dialect.quotechar, '"')

    def test__get_reader_has_header_with_semicol(self):
        """should return semicolon as delimiter and has header"""
        f = io.StringIO("""
            name;email
            abc;abc@google.com
            acd;acd@yahoo.com
            def;def@outlook.com"""
        )
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', has_header=True)
        reader, has_header = handler._get_reader(f)
        assert_true(has_header)
        assert_equal(reader.dialect.delimiter, ';')
        assert_equal(reader.dialect.quotechar, '"')

    def test__get_data_from_file(self):
        """should ignore header row and return three AddressBook entries with correct data"""
        f = io.StringIO("""
            name;email
            abc;abc@google.com
            acd;acd@yahoo.com
            def;def@outlook.com"""
        )
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', has_header=True)
        handler._get_data_from_file(f)

        assert_equal(len(handler.data), 3)
        data = set(handler.data)
        assert_true(AddressBook(id=None, email='abc@google.com', name='abc') in data)
        assert_true(AddressBook(id=None, email='acd@yahoo.com', name='acd') in data)
        assert_true(AddressBook(id=None, email='def@outlook.com', name='def') in data)

    def test__get_data_from_file_without_header(self):
        """should return three AddressBook entries with correct data"""
        f = io.StringIO("""
            abc,abc@google.com
            acd,acd@yahoo.com
            def,def@outlook.com"""
        )
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', has_header=False)
        handler._get_data_from_file(f)

        assert_equal(len(handler.data), 3)
        data = set(handler.data)
        assert_true(AddressBook(id=None, email='abc@google.com', name='abc') in data)
        assert_true(AddressBook(id=None, email='acd@yahoo.com', name='acd') in data)
        assert_true(AddressBook(id=None, email='def@outlook.com', name='def') in data)

    def test__validate_file_info(self):
        """if any of the metadata is set to None, exceptions will be raised"""
        with assert_raises(FileInfoNotCompleteError) as ex:
            handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=')
            handler._validate_file_info()
            assert_equal(ex.exception.args[0], 'Quote char information not specified.')

        with assert_raises(FileInfoNotCompleteError) as ex:
            handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', quotechar='./')
            handler._validate_file_info()
            assert_equal(ex.exception.args[0], 'Has header information not specified.')

        with assert_raises(FileInfoNotCompleteError) as ex:
            handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', quotechar='./', has_header=True)
            handler._validate_file_info()
            assert_equal(ex.exception.args[0], 'Delimiter information not specified.')

        with assert_raises(FileInfoNotCompleteError) as ex:
            handler = CSVHandler(
                filepath='dG1wNGsyY3o5MjU=', quotechar='./', has_header=True,
                delimiter=' ', encoding=None
            )
            handler._validate_file_info()
            assert_equal(ex.exception.args[0], 'Encoding information not specified.')

    def test_get_data(self):
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=')
        with patch.object(handler, '_validate_file_info') as _validate_file_info:
            with patch.object(handler, '_get_data_from_file') as _get_data_from_file:
                with patch('builtins.open', mock_open()) as f:
                    # Execute
                    handler.get_data()

                    # Verify
                    _validate_file_info.called_once()
                    _get_data_from_file.called_once_with_args(f)

    def test__guess_encoding_no_encoding(self):
        with patch(
                'builtins.open',
                mock_open(read_data=b'name email\nabc abc@aa.com')):
            handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', encoding=None)
            handler._guess_encoding()
            # Verify
            assert_equal(handler.encoding, 'ascii')

    def test__guess_encoding_already_has_encoding(self):
        with patch(
                'builtins.open',
                mock_open(read_data=b'name email\nabc abc@aa.com')):
            handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', encoding='cp1230')
            handler._guess_encoding()
            # Verify, used provided encoding rather than the guessed one
            assert_equal(handler.encoding, 'cp1230')

    @patch('address_book.model.CSVHandler._guess_encoding')
    def test_get_info(self, _guess_encoding):
        _guess_encoding.return_value = None
        handler = CSVHandler(filepath='dG1wNGsyY3o5MjU=', encoding='utf-8')
        with patch('builtins.open', mock_open(read_data='email name\nabc abc@aa.com\n')):
            info = handler.get_info()
            assert_equal(info, {
                'delimiter': ' ',
                'encoding': 'utf-8',
                'has_header': True,
                'quotechar': '"',
                'sample_data': []
            })


class TestAddressBook(object):

    def test___eq__(self):
        a = AddressBook(id=1, name='abc', email='abc@abc.com')
        b = AddressBook(id=1, name='abc', email='abc@abc.com')
        assert_equal(a, b)

    def test__eq__not_eq(self):
        a = AddressBook(id=1, name='abc', email='abc@abc.com')
        b = AddressBook(id=2, name='abc', email='abc@abc.com')
        c = AddressBook(id=1, name='abcd', email='abc@abc.com')
        d = AddressBook(id=1, name='abc', email='abcd@abc.com')
        assert_not_equal(a, b)
        assert_not_equal(a, c)
        assert_not_equal(a, d)
        assert_not_equal(b, c)
        assert_not_equal(b, d)
        assert_not_equal(c, d)

    def test__validate_invalid_email(self):
        with assert_raises(InvalidEmailAddress):
            AddressBook._validate('abc@aaa')
        with assert_raises(InvalidEmailAddress):
            AddressBook._validate('abc.aa.com')
        with assert_raises(InvalidEmailAddress):
            AddressBook._validate('$%#%abc@aa.org')

    def test__validate_valid_email(self):
        AddressBook._validate('abc@aa.com')
        AddressBook._validate('abc@aa.org')

    @patch('address_book.model.db.session.commit')
    @patch('address_book.model.db.session.execute')
    @patch('address_book.model.AddressBook._validate')
    def test_bulk_insert_addressbooks(self, _validate, execute, commit):
        # Setup
        _validate.return_value = True
        address_books = [
            AddressBook(id=None, name='abc', email='abc@abc.org'),
            AddressBook(id=None, name='def', email='def@def.com'),
        ]
        # Execute
        AddressBook.bulk_insert_addressbooks(
            address_books,
            AddressBook.__table__,
            ConflictsResolveStrategy.KEEP_EXISTING
        )
        # Verify
        execute.assert_called()
        commit.assert_called()
