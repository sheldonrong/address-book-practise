class CannotDetermineCSVMappingError(ValueError):

    def __init__(self):
        self.message = 'Cannot determine the mapping of data in the CSV file, check your files and try again?'


class FileInfoNotCompleteError(ValueError):
    pass


class InvalidEmailAddress(ValueError):

    def __init__(self, email):
        self.message = 'Invalid email address: {}'.format(email)
