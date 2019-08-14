import unittest

from geosupport import Geosupport
from suggest import GeosupportSuggest

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        g = Geosupport()
        cls.suggest = GeosupportSuggest(g)