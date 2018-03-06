from __future__ import absolute_import

import csv
from math import ceil

import chardet
import itertools
import re

from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

from sqlalchemy import Column, String, Integer, func
from sqlalchemy.dialects.postgresql import insert as pg_insert

from constants import ConflictsResolveStrategy
from address_book.exceptions import CannotDetermineCSVMappingError, FileInfoNotCompleteError, InvalidEmailAddress
from utils import decode_unique_filename

db = SQLAlchemy()


class CSVHandler(object):
    """
    CSV handler that helps to parse strings into tabular data structure.
    """

    CSV_SAMPLE_SIZE = 512
    CSV_DELIMITER_LIST = (' ', ',', ':', '|', ';')
    CSV_SAMPLE_ROWS = 5

    def __init__(self, filepath, has_header=None, delimiter=None, quotechar=None, encoding='utf-8'):
        self.has_header = has_header
        self.filepath = decode_unique_filename(filepath)
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding
        self.data = []

    def get_data(self):
        """open the temp file according to path, read and return a list of address book objects

        Returns:
            list of Address Book object
        """
        self._validate_file_info()

        with open(self.filepath, mode='rt', encoding=self.encoding) as csvfile:
            self._get_data_from_file(csvfile)

        return self.data

    def get_info(self):
        """
        Read a sample of the temp file, guess the metadata information using both Python's
        CSV sniffer and the chardet library.

        Returns:
            dict: a dict with meta information:
                encoding (str): the encoding of the file, i.e. utf-8, ascii, etc;
                delimiter (str): delimiter of the records, i.e. colon(:), space( ), comma(,), etc;
                quotechar (str): quote character that is used around each cell data
                sample_data (list of AddressBook): a preview of the data parsed using the above
                    metadata. this helps to give user an feeling of whether they chose the correct
                    metadata to parse the file or not.

        Raises:
            UnicodeError: if cannot parse the file using the encoding selected.
        """
        self._guess_encoding()

        with open(self.filepath, mode='rt', encoding=self.encoding) as csvfile:
            reader, has_header = self._get_reader(csvfile)

            sample_data = [
                AddressBook(email=row['email'].strip(), name=row['name'].strip(), id=None)
                    for row in itertools.islice(reader, self.CSV_SAMPLE_ROWS)
            ]
            has_header_ = self.has_header if self.has_header is not None else has_header
            return {
                'encoding': self.encoding,
                'delimiter': self.delimiter if self.delimiter is not None else reader.dialect.delimiter,
                'quotechar': self.quotechar if self.quotechar is not None else reader.dialect.quotechar,
                'has_header': has_header_,
                'sample_data': sample_data[1:] if has_header_ else sample_data
            }

    def _validate_file_info(self):
        if self.quotechar is None:
            raise FileInfoNotCompleteError('Quote char information not specified.')
        if self.has_header is None:
            raise FileInfoNotCompleteError('Has header information not specified.')
        if self.delimiter is None:
            raise FileInfoNotCompleteError('Delimiter information not specified.')
        if self.encoding is None:
            raise FileInfoNotCompleteError('Encoding information not specified.')

    def _get_reader(self, csvfile):
        sample = csvfile.read(self.CSV_SAMPLE_SIZE)
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(sample) \
            if self.has_header is None else self.has_header
        dialect = sniffer.sniff(
            sample,
            delimiters=self.CSV_DELIMITER_LIST,
        )
        fieldnames = self._guess_fieldnames(sample, self.delimiter or dialect.delimiter)
        # rewind to beginning of file
        csvfile.seek(0)
        reader = csv.DictReader(
            csvfile,
            dialect=dialect,
            fieldnames=fieldnames,
            delimiter=self.delimiter or dialect.delimiter,
            quotechar=self.quotechar or dialect.quotechar,
            skipinitialspace=dialect.skipinitialspace,
        )
        return reader, has_header

    def _get_data_from_file(self, csvfile):
        reader, has_header = self._get_reader(csvfile)
        if has_header:
            # if there is header, skip it
            next(reader, None)
        for row in reader:
            self.data.append(AddressBook(
                id=None,
                email=row['email'].strip(),
                name=row['name'].strip(),
            ))

    def _guess_encoding(self):
        # if no encoding is specified, we will guess it first
        if not self.encoding:
            with open(self.filepath, mode='rb') as csvfile:
                sample = csvfile.read(self.CSV_SAMPLE_SIZE)
                self.encoding = chardet.detect(sample)['encoding']

    @staticmethod
    def _guess_fieldnames(sample, delimiter):
        possible_fieldnames = []
        for row in sample.splitlines():
            row = row.strip()
            if not row:
                continue
            # it is possible there are invalid data in the samples
            # if we don't find it, look for the next row
            cells = row.strip().split(delimiter)
            if len(cells) < 2:
                raise CannotDetermineCSVMappingError()

            if '@' in cells[0]:
                possible_fieldnames = ['email', 'name']
                break
            elif '@' in cells[1]:
                possible_fieldnames = ['name', 'email']
                break

        # worst case scenario, no data in the sample rows are valid, raise exception
        if not possible_fieldnames:
            raise CannotDetermineCSVMappingError()
        return possible_fieldnames


class AddressBook(db.Model):

    __tablename__ = 'address_book'

    MAXLENGTH_EMAIL_ADDRESS = 254  # according to google
    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(MAXLENGTH_EMAIL_ADDRESS), unique=True, index=True)
    name = Column(String(64), index=True)

    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

    def __repr__(self):
        return '<AddressBook email={email} name={name}>'.format(
            email=self.email, name=self.name[0:12]
        )

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.email == other.email and
            self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.name, self.email))

    @staticmethod
    def get_total_pages(page_size):
        """
        retrieve the number of pages it will have provided by the page_size.

        Args:
            page_size (int)

        Returns:
            int: number of pages
        """
        return ceil(db.session.execute(func.count(AddressBook.id)).scalar() / page_size)

    @staticmethod
    def search(keyword=None, page=None, page_size=None):
        """
        general search functionality, that search for keyword and return paginated data.

        Returns:
            list of AddressBook instances: a list of objects satisfying the search criteria.
        """
        from address_book.search_criteria import SearchCriteria
        return SearchCriteria(db, {
            'keyword': keyword,
            'page': page,
            'page_size': page_size,
        }).search()

    @classmethod
    def bulk_insert_addressbooks(cls, address_books, table, on_duplicate):
        """
        Given a list of AddressBook instances, insert the data into database.

        When `on_duplicate` is set to ConflictsResolveStrategy.KEEP_EXISTING, any new
        address_books instances that has email already in the database will be skipped, whereas
        when `on_duplicate` is set to ConflictsResolveStrategy.REPLACE_WITH_NEW, it will
        replace the data in db with the one from the new objects.

        Args:
            address_books (list of AddressBook instances): a list of objects to be inserted
            table (SQLAlchemy.Table): the target table object
            on_duplicate (ConflictsResolveStrategy): one of the two strategy

        Returns:
            bool: indicating everything went fine.
                  program will continue when encountering errors, and only error info will be logged.
        """
        for i, row in enumerate(address_books):
            try:
                cls._validate(row.email)
                insert_sql = pg_insert(table).values(name=row.name, email=row.email)
                if on_duplicate == ConflictsResolveStrategy.KEEP_EXISTING:
                    insert_sql = insert_sql.on_conflict_do_nothing(index_elements=[table.c.email])
                elif on_duplicate == ConflictsResolveStrategy.REPLACE_WITH_NEW:
                    insert_sql = insert_sql.on_conflict_do_update(
                        index_elements=[table.c.email],
                        set_={'name': row.name}
                    )
                db.session.execute(insert_sql)
            except InvalidEmailAddress as ex:
                app.logger.info(ex)
            except Exception as e:
                app.logger.error(e)
            if i % 100 == 0:
                db.session.commit()
        db.session.commit()
        return True

    @classmethod
    def _validate(cls, email):
        if not re.search(cls.EMAIL_REGEX, email):
            raise InvalidEmailAddress(email)
