import io
from address_book.exceptions import CannotDetermineCSVMappingError
from address_book.model import CSVHandler, AddressBook
from nose.tools import assert_equal, assert_raises, assert_true, assert_false


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

    def test__get_reader(self):
        f = io.StringIO("""
            abc abc@google.com
            acd acd@yahoo.com
            def def@outlook.com"""
        )
        handler = CSVHandler(filepath='./')
        reader, has_header = handler._get_reader(f)
        assert_false(has_header)
        assert_equal(reader.dialect.delimiter, ' ')
        assert_equal(reader.dialect.quotechar, '"')

    def test__get_reader_has_header_with_semicol(self):
        f = io.StringIO("""
            name;email
            abc;abc@google.com
            acd;acd@yahoo.com
            def;def@outlook.com"""
        )
        handler = CSVHandler(filepath='./', has_header=True)
        reader, has_header = handler._get_reader(f)
        assert_true(has_header)
        assert_equal(reader.dialect.delimiter, ';')
        assert_equal(reader.dialect.quotechar, '"')

    def test__get_data_from_file(self):
        f = io.StringIO("""
            name;email
            abc;abc@google.com
            acd;acd@yahoo.com
            def;def@outlook.com"""
        )
        handler = CSVHandler(filepath='./', has_header=True)
        handler._get_data_from_file(f)

        assert_equal(len(handler.data), 3)
        data = set(handler.data)
        assert_true(AddressBook(id=None, email='abc@google.com', name='abc') in data)
        assert_true(AddressBook(id=None, email='acd@yahoo.com', name='acd') in data)
        assert_true(AddressBook(id=None, email='def@outlook.com', name='def') in data)

    def test__get_data_from_file_without_header(self):
        f = io.StringIO("""
            abc,abc@google.com
            acd,acd@yahoo.com
            def,def@outlook.com"""
        )
        handler = CSVHandler(filepath='./', has_header=False)
        handler._get_data_from_file(f)

        assert_equal(len(handler.data), 3)
        data = set(handler.data)
        assert_true(AddressBook(id=None, email='abc@google.com', name='abc') in data)
        assert_true(AddressBook(id=None, email='acd@yahoo.com', name='acd') in data)
        assert_true(AddressBook(id=None, email='def@outlook.com', name='def') in data)
