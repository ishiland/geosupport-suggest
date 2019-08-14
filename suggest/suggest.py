from geosupport import GeosupportError
from nycparser import Parser

parser = Parser()


class GeosupportSuggest(object):
    def __init__(self, geosupport=None, func='AP'):
        self.g = geosupport
        self.geofunction = func
        self.borough_dict_reverse = parser.borough_dict_reverse
        if self.g is None:
            raise Exception('You must initialize GeosupportSuggest with a Geosupport object.')

    def get_suggestions(self, input):
        res = parser.address(input)
        result = {
            'matches': [],
            'suggestions': []
        }

        if res['PHN'] and res['STREET']:

            if not res['BOROUGH_CODE'] and not res['ZIP']:

                # iterate borocodes
                for x in range(1, 6):
                    try:
                        match = self.g[self.geofunction](house_number=res['PHN'], street=res['STREET'], borough_code=x)
                        result['matches'].append(match)
                    except GeosupportError as ge:
                        if 'SIMILAR NAMES' in str(ge.result):
                            list_of_street_names = ge.result['List of Street Names']
                            boro_name = self.borough_dict_reverse[x]
                            r = [{
                                'phn': res['PHN'],
                                'street': s,
                                'boro_code': x,
                                'boro_name': boro_name,
                                'display': '{} {}, {}'.format(res['PHN'], s, boro_name)
                            } for s in list_of_street_names]
                            result['suggestions'].extend(r)

            elif res['BOROUGH_CODE']:
                try:
                    match = self.g[self.geofunction](house_number=res['PHN'], street=res['STREET'],
                                                     borough_code=res['BOROUGH_CODE'])
                    result['matches'].append(match)
                except GeosupportError as ge:
                    if 'SIMILAR NAMES' in str(ge.result):
                        list_of_street_names = ge.result['List of Street Names']
                        boro_name = self.borough_dict_reverse[res['BOROUGH_CODE']]
                        r = [{
                            'phn': res['PHN'],
                            'street': s,
                            'boro_code': res['BOROUGH_CODE'],
                            'boro_name': boro_name,
                            'display': '{} {}, {}'.format(res['PHN'], s, boro_name)
                        } for s in list_of_street_names]
                        result['suggestions'].extend(r)

            elif res['ZIP']:
                try:
                    match = self.g[self.geofunction](house_number=res['PHN'], street=res['STREET'], zip_code=res['ZIP'])
                    result['matches'].append(match)
                except GeosupportError:
                    pass

        return result
