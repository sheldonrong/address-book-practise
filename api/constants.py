from enum import Enum


class ConflictsResolveStrategy(Enum):

    KEEP_EXISTING = 'keep_existing'
    USE_NEW = 'use_new'

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return str(self.value) == str(other.value)

    def __ne__(self, other):
        return not self.__eq__(other)
