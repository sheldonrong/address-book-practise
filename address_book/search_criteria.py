from sqlalchemy import desc

from address_book.model import AddressBook


class SearchCriteria(object):
    """
    The SearchCriteria class helps build modular SQLAlchemy objects
    for advanced database queries.
    """

    DEFAULT_PAGE = 0
    DEFAULT_PAGE_SIZE = 50

    def __init__(self, db, criteria):
        self.db = db
        self.__criteria = criteria or {}

    def search(self):
        """construct search sql and execute to return a list of data"""
        address_book = self.db.session.query(AddressBook)
        for criterion in self.__criteria.keys():
            build_func = getattr(self, 'build_' + criterion, None)
            if build_func:
                address_book = build_func(address_book)

        # special pagination filters
        address_book = self._build_sort(address_book)
        address_book = self._build_pagination(address_book)
        return list(address_book)

    def build_keyword(self, address_book):
        keyword = self.__criteria.get('keyword', None)
        if keyword:
            return address_book.filter(
                AddressBook.name.ilike(keyword) | AddressBook.email.ilike(keyword)
            )
        return address_book

    def _build_sort(self, address_book):
        sort_by = self.__criteria.get('sort_by', AddressBook.id)
        sort_dir = self.__criteria.get('sort_dir', 'asc')
        return address_book.order_by(sort_by if sort_dir == 'asc' else desc(sort_by))

    def _build_pagination(self, address_book):
        page_size = self.__criteria.get('page_size', None) or self.DEFAULT_PAGE_SIZE
        page = self.__criteria.get('page', None) or self.DEFAULT_PAGE
        return address_book.limit(page_size).offset(page * page_size)
