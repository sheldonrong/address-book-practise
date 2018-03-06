from address_book.model import AddressBook
from constants import ConflictsResolveStrategy


class AddressBookService(object):
    """The public AddressBook interface. This class defines APIs the external
       application can call."""

    @staticmethod
    def search(keyword, page, page_size):
        """Perform search on the AddressBooks and return a list of AddressBook instances.

        Args:
            keyword (str): keyword to search on.
            page (int): current page index, used for pagination.
            page_size (int): number of records returned per page, used for pagination.

        Returns:
            list of AddressBook instances
        """
        return AddressBook.search(keyword, page, page_size)

    @staticmethod
    def get_total_pages(page_size):
        """
        Given number of records for each page, return total number pages needed.
        This helps front-end devs to build a table of address book data.

        Args:
            page_size (int): number of records per page

        Returns:
            int: number of pages.
        """
        return AddressBook.get_total_pages(page_size)

    @staticmethod
    def import_data(csv_handler, resolve_conflicts=ConflictsResolveStrategy.KEEP_EXISTING):
        """
        Import the Address Book data from the given temporary CSV file,
        using the `resolve_conflicts` strategy to handle data conflicts.

        Args:
            csv_handler (CSVHandler instance): handler pointing to the target import file
            resolve_conflicts (Enum): how to handle data conflicts

        Returns:
            bool: always true even if something went wrong. incorrect data will be ignored.
        """
        data = csv_handler.get_data()
        if data:
            return AddressBook.bulk_insert_addressbooks(
                data, AddressBook.__table__,
                on_duplicate=resolve_conflicts
            )
        return True
