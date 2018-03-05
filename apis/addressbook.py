import os

from flask_restplus import Namespace, Resource, fields
from flask import current_app as app
from flask import request
from werkzeug.exceptions import BadRequest

from address_book.service import AddressBookService
from address_book.model import CSVHandler
from apis.utils import (
    get_csv_metadata_fields,
    get_pagination_params
)

api = Namespace(
    'address-books',
    description='API for managing Address Books',
    path='/address_book'
)


@api.route('/')
class AddressBookList(Resource):

    DEFAULT_PAGE = 0
    DEFAULT_PAGE_SIZE = 50

    address_book = api.model('AddressBook', {
        'id': fields.Integer(required=True),
        'name': fields.String(),
        'email': fields.String()
    })

    pagination_params = get_pagination_params()

    @api.expect(pagination_params, validate=True)
    @api.marshal_list_with(address_book)
    def get(self):
        params = self.pagination_params.parse_args()
        keyword = params.get('keyword', None)
        page = params.get('page', self.DEFAULT_PAGE)
        size = params.get('size', self.DEFAULT_PAGE_SIZE)
        return AddressBookService.search(keyword, page, size)


@api.route('/import')
class AddressBookBulkImport(Resource):

    csv_params = api.model(name='AddressBookImportInputParams', model={
        'file_hash': fields.String(
            required=True,
            description='the returned file hash for uploaded file'
        ),
        'metadata': fields.Nested(
            api.model(
                name='AddressBookImportMetadata',
                model=get_csv_metadata_fields(required=True),
            ),
            required=True,
            description='metadata of the uploaded file'
        ),
        'resolve_conflicts': fields.String(
            required=True,
            default='keep_existing',
            enum=['keep_existing', 'replace_with_new'],
            description='to keep existing data or not to keep!'
        )
    })

    csv_returns = api.model('AddressBookImportReturnValues', {
        'success': fields.Boolean(required=True)
    })

    @api.expect(csv_params, validate=True)
    @api.marshal_with(csv_returns)
    def post(self):
        """
        save the information in the uploaded CSV file into db
        """
        params = request.get_json()
        metadata = params['metadata']
        try:
            handler = CSVHandler(os.path.join(
                os.path.dirname(__file__),
                '../',
                app.config['UPLOAD_FOLDER'],
                params['file_hash'],
            ),
                has_header=metadata['has_header'],
                delimiter=metadata['delimiter'],
                quotechar=metadata['quotechar'],
                encoding=metadata['encoding']
            )
            AddressBookService.import_data(handler, params['resolve_conflicts'])
        except FileNotFoundError:
            raise BadRequest('Could not locate file using the provided file hash.')
        return True


@api.route('/metadata/<page_size>')
class AddressBookMetadata(Resource):

    metadata = api.model('AddressBookMetadata', {
        'total_pages': fields.Integer(required=True),
    })

    @api.marshal_with(metadata)
    def get(self, page_size):
        return {
            'total_pages': AddressBookService.get_total_pages(int(page_size))
        }
