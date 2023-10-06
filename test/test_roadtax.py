import unittest
from unittest.mock import MagicMock

from src.roadtax_my.exception import (
    InvalidPostcode,
    InvalidVehicleCC,
    InvalidVehicleType,
)
from src.roadtax_my.roadtax_my import (
    filter_data,
    get_region,
    base_calculation,
    can_discount,
    calculate
)


class TestFilterData(unittest.TestCase):
    def setUp(self):
        self.data = {
            "car": {
                "USA": [
                    {"start_range": 0, "end_range": 100, "value": 10},
                    {"start_range": 101, "end_range": 200, "value": 20},
                    {"start_range": 201, "end_range": 300, "value": 30},
                ],
                "Europe": [
                    {"start_range": 0, "end_range": 100, "value": 50},
                    {"start_range": 101, "end_range": 200, "value": 100},
                    {"start_range": 201, "end_range": 300, "value": 150},
                ],
            },
            "bike": {
                "USA": [
                    {"start_range": 0, "end_range": 50, "value": 5},
                    {"start_range": 51, "end_range": 100, "value": 10},
                    {"start_range": 101, "end_range": 150, "value": 15},
                ],
                "Europe": [
                    {"start_range": 0, "end_range": 50, "value": 10},
                    {"start_range": 51, "end_range": 100, "value": 20},
                    {"start_range": 101, "end_range": 150, "value": 30},
                ],
            },
        }

    def test_filter_data_within_range(self):
        result = filter_data(self.data, "USA", "car", 150)
        self.assertEqual(result, {"start_range": 101,
                         "end_range": 200, "value": 20})

        result = filter_data(self.data, "Europe", "car", 250)
        self.assertEqual(result, {"start_range": 201,
                         "end_range": 300, "value": 150})

        result = filter_data(self.data, "USA", "bike", 75)
        self.assertEqual(
            result,
            {
                "start_range": 51,
                "end_range": 100, "value": 10
            }
        )

        result = filter_data(self.data, "Europe", "bike", 125)
        self.assertEqual(result, {"start_range": 101,
                         "end_range": 150, "value": 30})

    def test_filter_data_outside_range(self):
        result = filter_data(self.data, "USA", "car", 9000)
        self.assertEqual(result, {})

        result = filter_data(self.data, "Europe", "car", 350)
        self.assertEqual(result, {})

        result = filter_data(self.data, "USA", "bike", 200)
        self.assertEqual(result, {})

        result = filter_data(self.data, "Europe", "bike", 300)
        self.assertEqual(result, {})

    def test_filter_data_not_found(self):
        result = filter_data(self.data, "Asia", "car", 150)
        self.assertEqual(result, {})

        result = filter_data(self.data, "USA", "truck", 150)
        self.assertEqual(result, {})

        result = filter_data(self.data, "Europe", "bike", 500)
        self.assertEqual(result, {})

    def test_filter_data_empty_data(self):
        result = filter_data({}, "USA", "car", 150)
        self.assertEqual(result, {})


class TestGetRegion(unittest.TestCase):
    def test_valid_postcodes_east(self):
        self.assertEqual(get_region(80000), "East")
        self.assertEqual(get_region(85000), "East")
        self.assertEqual(get_region(99999), "East")

    def test_valid_postcodes_west(self):
        self.assertEqual(get_region(10000), "West")
        self.assertEqual(get_region(50000), "West")
        self.assertEqual(get_region(79999), "West")

    def test_invalid_postcode(self):
        with self.assertRaises(InvalidPostcode):
            get_region("ABC")

    def test_invalid_postcode_type(self):
        with self.assertRaises(InvalidPostcode):
            get_region(None)


class TestBaseCalculation(unittest.TestCase):
    def test_base_calculation_valid_cc(self):
        # Test valid vehicle_cc
        self.assertEqual(base_calculation(1500, 1000, 10.0, 0.01), 15.0)
        self.assertEqual(base_calculation(2000, 1000, 10.0, 0.01), 20.0)

    def test_base_calculation_invalid_cc(self):
        # Test invalid vehicle_cc
        with self.assertRaises(InvalidVehicleCC):
            base_calculation("abc", 1000, 10.0, 0.01)
        with self.assertRaises(InvalidVehicleCC):
            base_calculation(1500, "abc", 10.0, 0.01)

    def test_base_calculation_edge_cases(self):
        # Test edge cases
        self.assertEqual(base_calculation(1000, 1000, 10.0, 0.01), 10.0)
        self.assertEqual(base_calculation(999, 1000, 10.0, 0.01), 9.99)
        self.assertEqual(base_calculation(2000, 2000, 10.0, 0.01), 10.0)


class TestCanDiscount(unittest.TestCase):

    def test_can_discount_valid_parameters(self):
        # Test case with valid parameters
        self.assertTrue(can_discount(7000, "Saloon", 1500))

    def test_can_discount_invalid_postcode(self):
        # Test case with invalid postcode
        with self.assertRaises(InvalidPostcode):
            can_discount("8000", "Saloon", 1500)

    def test_can_discount_invalid_vehicle_cc(self):
        # Test case with invalid vehicle cc
        with self.assertRaises(InvalidVehicleCC):
            can_discount(7000, "Saloon", -1500)

    def test_can_discount_invalid_vehicle_type(self):
        # Test case with invalid vehicle type
        with self.assertRaises(InvalidVehicleType):
            can_discount(7000, "InvalidType", 1500)


class TestCalculate(unittest.TestCase):

    def test_valid_input(self):
        # Testing with valid input
        postcode = 12345
        vehicle_type = "Saloon"
        vehicle_cc = 1500
        expected_result = 9
        0.0

        result = calculate(postcode, vehicle_type, vehicle_cc)

        self.assertEqual(result, expected_result)

    def test_invalid_postcode(self):
        # Testing with invalid postcode
        postcode = "invalid"
        vehicle_type = "Saloon"
        vehicle_cc = 1500

        with self.assertRaises(InvalidPostcode):
            calculate(postcode, vehicle_type, vehicle_cc)

    def test_invalid_vehicle_cc(self):
        # Testing with invalid vehicle cc
        postcode = 12345
        vehicle_type = "Saloon"
        vehicle_cc = "invalid"

        with self.assertRaises(InvalidVehicleCC):
            calculate(postcode, vehicle_type, vehicle_cc)

    def test_invalid_vehicle_type(self):
        # Testing with invalid vehicle type
        postcode = 12345
        vehicle_type = "invalid"
        vehicle_cc = 1500

        with self.assertRaises(InvalidVehicleType):
            calculate(postcode, vehicle_type, vehicle_cc)

    def test_discount_applicable(self):
        # Testing when discount is applicable
        postcode = 7100
        vehicle_type = "Saloon"
        vehicle_cc = 1500
        expected_result = 45.0

        # Mocking can_discount function to return True
        with MagicMock() as mock_can_discount:
            mock_can_discount.return_value = True

            result = calculate(postcode, vehicle_type, vehicle_cc)

            self.assertEqual(result, expected_result)

    def test_discount_not_applicable(self):
        # Testing when discount is not applicable
        postcode = 12345
        vehicle_type = "Saloon"
        vehicle_cc = 1500
        expected_result = 90.0

        # Mocking can_discount function to return False
        with MagicMock() as mock_can_discount:
            mock_can_discount.return_value = False

            result = calculate(postcode, vehicle_type, vehicle_cc)

            self.assertEqual(result, expected_result)
