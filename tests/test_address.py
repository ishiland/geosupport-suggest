from tests.testcase import TestCase


class TestSuggestions(TestCase):
    def test_no_results(self):
        result = self.suggest.get_suggestions('100')
        self.assertListEqual(result['suggestions'], [])

    def test_has_suggestions_and_no_matches(self):
        result = self.suggest.get_suggestions('100 G')
        self.assertTrue(len(result['suggestions']) >= 1)
        self.assertTrue(len(result['matches']) == 0)
        for r in result['suggestions']:
            self.assertIsNotNone(r['phn'])
            self.assertIsNotNone(r['street'])
            self.assertIsNotNone(r['boro_name'])
            self.assertIsNotNone(r['boro_code'])
            self.assertIsNotNone(r['display'])

    def test_has_suggestions_and_matches(self):
        result = self.suggest.get_suggestions('100 Gold st')
        self.assertTrue(len(result['suggestions']) >= 2)
        self.assertTrue(len(result['matches']) >= 2)

    def test_suggestions_have_values(self):
        result = self.suggest.get_suggestions('100 Go')
        for r in result['suggestions']:
            self.assertIsNotNone(r['phn'])
            self.assertIsNotNone(r['street'])
            self.assertIsNotNone(r['boro_name'])
            self.assertIsNotNone(r['boro_code'])
            self.assertIsNotNone(r['display'])

    def test_suggestions_with_boro_name(self):
        result = self.suggest.get_suggestions('100 Gold st, Manhattan')
        self.assertTrue(len(result['suggestions']) == 0)
        self.assertTrue(len(result['matches']) == 1)

    def test_suggestions_with_zip_code(self):
        result = self.suggest.get_suggestions('100 Gold st, 10038')
        self.assertTrue(len(result['suggestions']) == 0)
        self.assertTrue(len(result['matches']) == 1)
