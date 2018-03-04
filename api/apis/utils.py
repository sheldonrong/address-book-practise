from flask.ext.restplus import fields
from flask_restplus import reqparse


def get_csv_metadata_fields(required=False):
    return {
        'delimiter': fields.String(
            required=required,
            description='delimiter used in CSV file',
            enum=[' ', ';', ',', ':', '|']
        ),
        'quotechar': fields.String(
            required=required,
            description='quote char used in CSV file',
            enum=[" ", "\"", "\'"]
        ),
        'has_header': fields.Integer(
            required=required,
            description='is the first row a header row?',
            min=0, max=1
        ),
        'encoding': fields.String(
            required=required,
            description='the encoding of the file',
            enum=['ascii', 'utf-8', 'utf-16', 'cp1250', 'cp1251', 'cp1252', 'gbk']
        )
    }


def get_csv_metadata_params(required=False):
    fields_ = get_csv_metadata_fields(required=required)
    parser = reqparse.RequestParser()
    for key, field in fields_.items():
        parser.add_argument(key, type=field.format, required=required)
    return parser
