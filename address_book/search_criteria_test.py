from mock import patch, MagicMock
from nose.tools import assert_equal

from address_book.model import db, AddressBook
from address_book.search_criteria import SearchCriteria


class TestSearchCriteria(object):

    @patch('address_book.search_criteria.SearchCriteria._build_pagination')
    @patch('address_book.search_criteria.SearchCriteria._build_sort')
    @patch('address_book.search_criteria.SearchCriteria.build_keyword')
    @patch('address_book.model.db.session.query')
    def test_search(self, query, build_keyword,
        _build_sort, _build_pagination,):
        # Setup
        query.return_value = True

        sc = SearchCriteria(db, {
            'keyword': 'sample text',
            'page': 0,
            'page_size': 20
        })
        # Execute
        sc.search()
        # Verify
        build_keyword.assert_called_once()
        _build_sort.assert_called_once()
        _build_pagination.assert_called_once()

    def test_build_keywprd(self):
        sc = SearchCriteria(db, {
            'keyword': 'sample text',
        })
        address_book = MagicMock()
        sc.build_keyword(address_book)
        assert_equal(str(address_book.filter.call_args[0][0]),
            'lower(address_book.name) LIKE lower(:name_1) OR lower(address_book.email) LIKE lower(:email_1)')

    def test__build_sort(self):
        sc = SearchCriteria(db, {
            'name': 'sample name',
            'email': 'sample email',
            'sort_by': 'name',
            'sort_dir': 'desc'
        })
        address_book = MagicMock()
        sc._build_sort(address_book)
        assert_equal(str(address_book.order_by.call_args[0][0]), 'name DESC')

    def test__build_pagination_default(self):
        sc = SearchCriteria(db, {

        })
        address_book = MagicMock()
        sc._build_pagination(address_book)
        assert_equal(str(address_book.limit.call_args[0][0]), '50')

    def test__build_pagination_specific_page(self):
        sc = SearchCriteria(db, {
            'page': 2,
            'page_size': 100
        })
        address_book = MagicMock()
        sc._build_pagination(address_book)
        assert_equal(str(address_book.limit.call_args[0][0]), '100')

