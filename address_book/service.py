from address_book.model import AddressBook, CSVHandler
from constants import ConflictsResolveStrategy


class AddressBookService(object):

    @staticmethod
    def search(keyword, page, page_size):
        return AddressBook.search(keyword, page, page_size)

    @staticmethod
    def get_total_pages(page_size):
        return AddressBook.get_total_pages(page_size)

    @staticmethod
    def import_data(csv_handler, resolve_conflicts=ConflictsResolveStrategy.KEEP_EXISTING):
        data = csv_handler.get_data()
        if data:
            AddressBook.bulk_insert_addressbooks(
                data, AddressBook.__table__,
                on_duplicate=resolve_conflicts
            )
        return True
