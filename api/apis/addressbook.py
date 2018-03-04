import os

from flask.ext.restplus import Namespace, Resource, fields
from flask import current_app as app
from flask import request
from address_book.service import AddressBookService
from address_book.model import CSVHandler
from apis.utils import get_csv_metadata_fields
from werkzeug.exceptions import BadRequest

api = Namespace(
    'address-books',
    description='API for managing Address Books',
    path='/address_book'
)

address_book = api.model('AddressBook', {
    'id': fields.Integer(required=True),
    'name': fields.String(),
    'email': fields.String()
})


@api.route('/')
class AddressBookList(Resource):

    @api.marshal_list_with(address_book)
    def get(self):
        return AddressBookService.search()


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
        try:
            handler = CSVHandler(os.path.join(
                os.path.dirname(__file__),
                '../',
                app.config['UPLOAD_FOLDER'],
                params['file_hash'],
            ),
                has_header=params['metadata']['has_header'],
                delimiter=params['metadata']['delimiter'],
                quotechar=params['metadata']['quotechar'],
                encoding=params['metadata']['encoding']
            )
            AddressBookService.import_data(handler, params['resolve_conflicts'])
        except FileNotFoundError:
            raise BadRequest('Could not locate file using the provided file hash.')
        return True


@api.route('/<id>', endpoint='address-book')
@api.param('id', 'the address book id')
@api.response(404, 'Address book not found')
class AddressBook(Resource):

    @api.marshal_with(address_book)
    def get(self, id):
        return AddressBookService.get(id)
