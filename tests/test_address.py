from tests.testcase import TestCase
from unittest.mock import MagicMock
from geosupport import GeosupportError
from suggest import GeosupportSuggest


class TestSuggestions(TestCase):

    def test_no_suggestions(self):
        result = self.suggest.suggestions("100")
        self.assertListEqual(result, [])

    def test_has_suggestions(self):
        result = self.suggest.suggestions("100 Gold st")
        self.assertTrue(len(result) >= 1)
        # Verify the mock returned expected data
        self.assertEqual(result[0]["First Borough Name"], "MANHATTAN")

    def test_suggestions_have_values(self):
        # Create a dedicated mock for this test
        mock_geosupport = MagicMock()
        mock_func = MagicMock()
        mock_geosupport.__getitem__.return_value = mock_func

        # Create a test-specific instance
        test_suggest = GeosupportSuggest(mock_geosupport)

        # Create a proper GeosupportError with the result attribute structure
        # that matches what's expected in your _geocode method
        mock_error = GeosupportError({})
        mock_error.result = {
            "Message": "SIMILAR NAMES",
            "List of Street Names": ["GOLD STREET", "GOLD AVENUE"],
        }

        # Only need 3 side effects - one for the error, two for the similar streets
        mock_func.side_effect = [
            mock_error,
            {
                "First Borough Name": "MANHATTAN",
                "House Number - Display Format": "100",
                "First Street Name Normalized": "GOLD STREET",
            },
            {
                "First Borough Name": "BROOKLYN",
                "House Number - Display Format": "100",
                "First Street Name Normalized": "GOLD AVENUE",
            },
        ]

        # Use a single borough call to simplify the test
        result = test_suggest.suggestions("100 Gol", borough_code=1)

        self.assertTrue(len(result) >= 1)
        for s in result:
            self.assertTrue(len(s["First Borough Name"]) >= 1)
            self.assertTrue(len(s["House Number - Display Format"]) >= 1)
            self.assertTrue(len(s["First Street Name Normalized"]) >= 1)

    def test_suggestions_with_zip_code(self):
        result = self.suggest.suggestions("100 Gold st, 10038")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["First Borough Name"], "MANHATTAN")

    def test_suggestions_have_no_none(self):
        result = self.suggest.suggestions("100 Gold")
        self.assertTrue(None not in result)

    def test_borough_code_argument(self):
        result = self.suggest.suggestions("100 Gold st", borough_code=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["First Borough Name"], "MANHATTAN")
        self.assertIsNotNone(result[0]["House Number - Display Format"])
        self.assertIsNotNone(result[0]["First Street Name Normalized"])
