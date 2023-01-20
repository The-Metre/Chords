from .base import FunctionalTest

from unittest import skip


class ItemValidationTest(FunctionalTest):

    def test_cannot_empty_list(self):
        """ Test cannot add empty element in the list """
        # End of the test
        self.fail('End of the test')

if __name__ == '__main__':
    pass