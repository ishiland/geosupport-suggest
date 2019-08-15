from tests.testcase import TestCase


class TestSuggestions(TestCase):

    def test_no_suggestions(self):
        result = self.suggest.suggestions('100')
        self.assertListEqual(result, [])

    def test_has_suggestions(self):
        result = self.suggest.suggestions('100 Gold st')
        self.assertTrue(len(result) >= 1)

    def test_suggestions_have_values(self):
        result = self.suggest.suggestions('100 Gol')
        self.assertTrue(len(result) >= 1)
        for s in result:
            self.assertTrue(len(s['First Borough Name']) >= 1)
            self.assertTrue(len(s['House Number - Display Format']) >= 1)
            self.assertTrue(len(s['First Street Name Normalized']) >= 1)

    def test_suggestions_with_zip_code(self):
        result = self.suggest.suggestions('100 Gold st, 10038')
        self.assertTrue(len(result) == 1)

    def test_suggestions_have_no_none(self):
        result = self.suggest.suggestions('100 Gold')
        self.assertTrue(None not in result)

    def test_borough_code_argument(self):
        result = self.suggest.suggestions('100 Gold st', borough_code=1)
        self.assertTrue(len(result) == 1)
        self.assertIsNotNone(result[0]['First Borough Name'])
        self.assertIsNotNone(result[0]['House Number - Display Format'])
        self.assertIsNotNone(result[0]['First Street Name Normalized'])
