from address_book.model import AddressBook


class SearchCriteria(object):

    DEFAULT_TOP = 50

    def __init__(self, db, criteria):
        self.db = db
        self.__criteria = criteria or {}

    def search(self):
        address_book = self.db.session.query(AddressBook)
        for criterion in self.__criteria.keys():
            build_func = getattr(self, '_build_' + criterion, None)
            if build_func:
                address_book = build_func(address_book)

        # special pagination filters
        address_book = self.__build_after(address_book)
        address_book = self.__build_sort(address_book)
        address_book = self.__build_top(address_book)
        return list(address_book)

    def _build_name(self, address_book):
        name = self.__criteria.get('name', None)
        if name:
            return address_book.filter(AddressBook.name == name)
        return address_book

    def _build_email(self, address_book):
        email = self.__criteria.get('email', None)
        if email:
            return address_book.filter(AddressBook.email == email)
        return address_book

    def __build_sort(self, address_book):
        sort_by = self.__criteria.get('sort_by', AddressBook.id)
        sort_dir = self.__criteria.get('sort_dir', 'asc')
        return address_book.order_by(sort_by if sort_dir == 'asc' else sort_by.desc())

    def __build_top(self, address_book):
        return address_book.limit(self.__criteria.get('top', self.DEFAULT_TOP))

    def __build_after(self, address_book):
        after = self.__criteria.get('after', None)
        if after:
            return address_book.filter(AddressBook.id > after)
        return address_book
