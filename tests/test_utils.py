from unittest import TestCase

from utils._utils import remove_whitespaces


class UtilsTest(TestCase):
    def test_remove_whitespaces(self):
        # case 1: spaces at the beginning
        s1 = "    1"
        self.assertEqual("1", remove_whitespaces(s1))

        # case 2: spaces at the end
        s2 = "2    "
        self.assertEqual("2", remove_whitespaces(s2))

        # case 3: spaces in the middle
        s3 = "    3"
        self.assertEqual("3", remove_whitespaces(s3))

        # case 4: newline characters
        s4 = "\n\n4"
        self.assertEqual("4", remove_whitespaces(s4))

        # case 5: tab characters
        s5 = "\t5\t"
        self.assertEqual("5", remove_whitespaces(s5))

        # case 6: all kind of whitespaces
        s6 = s1 + s2 + s3 + s4 + s5
        self.assertEqual("12345", remove_whitespaces(s6))
