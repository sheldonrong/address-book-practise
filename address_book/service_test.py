from mock import patch, MagicMock
from nose.tools import assert_equal

from address_book.model import AddressBook
from address_book.service import AddressBookService


class TestAddressBookService(object):

    @patch('address_book.model.AddressBook.search')
    def test_search(self, search):
        # Setup
        search.return_value = 'random_data'
        keyword = 'abc@aaa.org'
        page = 2
        page_size = 50

        # Execute
        result = AddressBookService.search(keyword, page, page_size)

        # Verify
        assert_equal(result, 'random_data')
        search.assert_called_once_with(keyword, page, page_size)

    @patch('address_book.model.AddressBook.bulk_insert_addressbooks')
    def test_import_data(self, bulk_insert_addressbooks):
        # Setup
        raw_data = [
            AddressBook(id=1, name='Smith John', email='smith.john@gmail.com'),
            AddressBook(id=2, name='Jane Stewart', email='jstewart@gmail.com'),
            AddressBook(id=3, name='Tom Hanks', email='thanks@gmail.com'),
            AddressBook(id=4, name='Jennifer Lawrence', email='jlawrence@aol.com'),
        ]
        csv_handler = MagicMock(get_data=lambda: raw_data)
        AddressBookService.import_data(csv_handler)

        bulk_insert_addressbooks.assert_called_once_with(
            raw_data, AddressBook.__table__, on_duplicate='keep_existing'
        )
