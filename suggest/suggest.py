from geosupport import GeosupportError
from nycparser import Parser

parser = Parser()


class GeosupportSuggest(object):
    def __init__(self, geosupport=None, func='AP'):
        """
        This object has a single public method, `suggestions` which provide a list of valid address suggestions.
        :param geosupport: A Geosupport object to geocode with
        :param func: Which Geosupport function to execute. Tested with 'AP' and '1B'
        """
        self._g = geosupport
        self.geofunction = func
        self.results = []
        self.similiar_names = []
        if self._g is None:
            raise Exception('You must initialize GeosupportSuggest with a Geosupport object.')

    def _geocode(self, phn, street, borough_code=None, zip=None):
        """
        geocodes or fails to geocode any address
        :param phn: house number
        :param street: street
        :param borough_code: borough code (1-5)
        :param zip: zip code
        :return: None
        """
        try:
            r = self._g[self.geofunction](house_number=phn, street=street, borough_code=borough_code, zip=zip)
            self.results.append(r)
        except GeosupportError as ge:
            if 'SIMILAR NAMES' in ge.result["Message"]:
                list_of_street_names = ge.result['List of Street Names']
                r = [{
                    'street': s,
                    'borough_code': borough_code
                } for s in list_of_street_names]
                self.similiar_names.extend(r)

    def suggestions(self, input, borough_code=None):
        """
        Get valid address suggestions from Geosupport based on user input.
        :param input: Single string address
        :param borough_code: Borough Code (1-5)
        :return: List of valid addresses that closely resemble user input.
        """
        parsed = parser.address(input)
        if borough_code:
            parsed['BOROUGH_CODE'] = borough_code
        self.similiar_names = []
        self.results = []
        if parsed['PHN'] and parsed['STREET']:
            if not parsed['BOROUGH_CODE'] and not parsed['ZIP']:
                # iterate borocodes
                for x in range(1, 6):
                    self._geocode(phn=parsed['PHN'], street=parsed['STREET'], borough_code=x)
            # try address with borough code if present
            elif parsed['BOROUGH_CODE']:
                self._geocode(phn=parsed['PHN'], street=parsed['STREET'], borough_code=parsed['BOROUGH_CODE'])
            # try address with zip code if present
            elif parsed['ZIP']:
                self._geocode(phn=parsed['PHN'], street=parsed['STREET'], zip=parsed['ZIP'])
            # validate and retrieve any addresses
            if len(self.similiar_names):
                for name in self.similiar_names:
                    self._geocode(phn=parsed['PHN'], street=name['street'], borough_code=name['borough_code'])
                if None in self.results:
                    self.results = list(filter(lambda v: v is not None, self.results))

        return self.results
