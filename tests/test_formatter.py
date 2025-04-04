import unittest
from suggest.suggest import AddressFormatter


class TestAddressFormatter(unittest.TestCase):

    def test_format_borough_normal(self):
        """Test formatting normal borough names."""
        self.assertEqual(AddressFormatter.format_borough("Manhattan"), "MANHATTAN")
        self.assertEqual(AddressFormatter.format_borough("queens"), "QUEENS")
        self.assertEqual(AddressFormatter.format_borough("Brooklyn"), "BROOKLYN")

    def test_format_borough_edge_cases(self):
        """Test formatting edge cases for borough names."""
        self.assertEqual(AddressFormatter.format_borough(None), "")
        self.assertEqual(AddressFormatter.format_borough(""), "")
        self.assertEqual(AddressFormatter.format_borough("   "), "   ")

    def test_format_bbl_dict(self):
        """Test formatting BBL from dictionary."""
        bbl_dict = {"BOROUGH BLOCK LOT (BBL)": "1002501001"}
        self.assertEqual(AddressFormatter.format_bbl(bbl_dict), "1002501001")

    def test_format_bbl_string(self):
        """Test formatting BBL from string."""
        self.assertEqual(AddressFormatter.format_bbl("1002501001"), "1002501001")

    def test_format_bbl_edge_cases(self):
        """Test formatting edge cases for BBL."""
        self.assertIsNone(AddressFormatter.format_bbl(None))
        self.assertEqual(AddressFormatter.format_bbl({}), None)
        self.assertEqual(AddressFormatter.format_bbl({"other_key": "value"}), None)

    def test_format_coordinates_normal(self):
        """Test formatting normal coordinates."""
        coords = AddressFormatter.format_coordinates(40.7128, -74.0060)
        self.assertEqual(coords["latitude"], 40.7128)
        self.assertEqual(coords["longitude"], -74.0060)

    def test_format_coordinates_strings(self):
        """Test formatting string coordinates."""
        coords = AddressFormatter.format_coordinates("40.7128", "-74.0060")
        self.assertEqual(coords["latitude"], 40.7128)
        self.assertEqual(coords["longitude"], -74.0060)

    def test_format_coordinates_edge_cases(self):
        """Test formatting edge cases for coordinates."""
        self.assertIsNone(AddressFormatter.format_coordinates(None, -74.0060))
        self.assertIsNone(AddressFormatter.format_coordinates(40.7128, None))
        self.assertIsNone(AddressFormatter.format_coordinates(None, None))

    def test_format_coordinates_invalid(self):
        """Test formatting invalid coordinates."""
        self.assertIsNone(AddressFormatter.format_coordinates("invalid", -74.0060))
        self.assertIsNone(AddressFormatter.format_coordinates(40.7128, "invalid"))
        self.assertIsNone(
            AddressFormatter.format_coordinates("invalid", "also_invalid")
        )
