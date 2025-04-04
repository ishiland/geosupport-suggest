import unittest
from unittest.mock import MagicMock
from geosupport import GeosupportError

from suggest import GeosupportSuggest


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create mock Geosupport object
        mock_geosupport = MagicMock()

        # Configure the mock function with appropriate returns based on inputs
        def mock_geocode(**kwargs):
            house_number = kwargs.get("house_number")
            street = kwargs.get("street", "")
            borough_code = kwargs.get("borough_code")
            zip_code = kwargs.get("zip")

            # Case: Insufficient input (just '100')
            if house_number == "100" and not street:
                return None

            # Case: Gold st with borough code 1 (Manhattan)
            if (
                house_number
                and street
                and "GOLD" in street.upper()
                and borough_code == 1
            ):
                return {
                    "First Borough Name": "MANHATTAN",
                    "House Number - Display Format": house_number,
                    "First Street Name Normalized": "GOLD STREET",
                }

            # Case: Gold st with ZIP 10038 (Manhattan)
            if (
                house_number
                and street
                and "GOLD" in street.upper()
                and zip_code == "10038"
            ):
                return {
                    "First Borough Name": "MANHATTAN",
                    "House Number - Display Format": house_number,
                    "First Street Name Normalized": "GOLD STREET",
                }

            # Case: Similar names for 'Gol'
            if house_number and street and street.upper() == "GOL":
                # Important: Create GeosupportError correctly
                error = GeosupportError({})
                error.result = {
                    "Message": "SIMILAR NAMES",
                    "List of Street Names": ["GOLD STREET", "GOLD AVENUE"],
                }
                raise error

            # Default case for Gold st (multiple results by borough)
            if house_number and street and "GOLD" in street.upper():
                # For test_has_suggestions, ensure we return MANHATTAN for any GOLD search
                return {
                    "First Borough Name": "MANHATTAN",
                    "House Number - Display Format": house_number,
                    "First Street Name Normalized": "GOLD STREET",
                }

            return None

        # Set up the mock_function to be returned by __getitem__
        mock_function = MagicMock(side_effect=mock_geocode)
        mock_geosupport.__getitem__.return_value = mock_function

        cls.suggest = GeosupportSuggest(mock_geosupport)
