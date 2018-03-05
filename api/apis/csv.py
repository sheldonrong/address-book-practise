import os
from flask import current_app as app
from flask_restplus import Resource, Namespace, fields
from werkzeug.exceptions import BadRequest

from address_book.model import CSVHandler
from address_book.exceptions import CannotDetermineCSVMappingError
from apis.addressbook import AddressBookList
from apis.utils import get_csv_metadata_fields, get_csv_metadata_params


api = Namespace(
    'csv',
    description='API for managing CSVs',
    path='/csv'
)


@api.route('/<file_hash>')
class CSV(Resource):

    csv_params = get_csv_metadata_params(required=False)

    csv_returns = api.model(
        'CSVReturnValues',
        dict(get_csv_metadata_fields(required=True), **{
            'sample_data': fields.List(
                fields.Nested(AddressBookList.address_book),
                required=True,
                description='returned sample data',
            ),
        })
    )

    @api.expect(csv_params, validate=True)
    @api.marshal_with(csv_returns)
    def get(self, file_hash):
        """
        retrieve the CSV information from some samples of the uploaded file
        """
        params = self.csv_params.parse_args()
        try:
            handler = CSVHandler(os.path.join(
                os.path.dirname(__file__),
                '../',
                app.config['UPLOAD_FOLDER'],
                file_hash,
            ),
                has_header=params.get('has_header', None),
                delimiter=params.get('delimiter', None),
                quotechar=params.get('quotechar', None),
                encoding=params.get('encoding', None)
            )
            return handler.get_info()
        except FileNotFoundError:
            raise BadRequest('Could not locate file using the provided file hash.')
        except CannotDetermineCSVMappingError:
            raise BadRequest('Could not parse CSV file, please double check the encoding, delimiter of the file.')
        except UnicodeError:
            raise BadRequest('Invalid Unicode encoding, please check the encoding of the file.')
