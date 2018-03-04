from address_book.model import AddressBook, CSVHandler
from constants import ConflictsResolveStrategy


class AddressBookService(object):

    @staticmethod
    def search(email=None, name=None, top=None, after=None):
        return AddressBook.search(email, name, top, after)

    @staticmethod
    def get(id_):
        return AddressBook.get_by_id(id_)

    @staticmethod
    def import_data(csv_handler, resolve_conflicts=ConflictsResolveStrategy.KEEP_EXISTING):
        data = csv_handler.get_data()
        if data:
            AddressBook.bulk_insert_addressbooks(
                data, AddressBook.__table__,
                on_duplicate=resolve_conflicts
            )
        return True
