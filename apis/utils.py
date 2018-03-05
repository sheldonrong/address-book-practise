from flask_restplus import reqparse, fields


def get_pagination_params():
    parser = reqparse.RequestParser()
    parser.add_argument('keyword', type=str, help='keyword to search for')
    parser.add_argument('page', type=int, help='page to start from')
    parser.add_argument('size', type=int, help='how many to retrieve each page')
    return parser


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
        # TODO: this library does not handle boolean well, using Integer for now as workaround
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
