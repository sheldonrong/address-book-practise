from flask_restplus import Api

from .addressbook import api as ns1
from .csv import api as ns2

api = Api(
    title='Address Book API',
    version='1.0',
    description='Manage address books',
    doc='/api_doc'
)

api.add_namespace(ns1, path='/api/address-book')
api.add_namespace(ns2, path='/api/csv')
