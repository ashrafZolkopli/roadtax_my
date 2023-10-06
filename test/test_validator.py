import unittest
from src.roadtax_my.exception import (
    InvalidPostcode,
    InvalidVehicleCC,
    InvalidVehicleType,
)
from src.roadtax_my.validator import (
    validate_vehicle_cc,
    validate_postcode,
    validate_vehicle_type,
    validate_all,
)


class TestValidateVehicleCC(unittest.TestCase):
    def test_valid_vehicle_cc(self):
        self.assertEqual(validate_vehicle_cc(5000), 5000)
        self.assertEqual(validate_vehicle_cc(99999), 99999)

    def test_invalid_vehicle_cc_type(self):
        with self.assertRaises(TypeError):
            validate_vehicle_cc("5000")

    def test_invalid_vehicle_cc_range(self):
        with self.assertRaises(ValueError):
            validate_vehicle_cc(0)
        with self.assertRaises(ValueError):
            validate_vehicle_cc(100000)


class TestValidatePostcode(unittest.TestCase):
    def test_valid_postcode(self):
        self.assertEqual(validate_postcode(12345), 12345)

    def test_invalid_postcode_type(self):
        with self.assertRaises(TypeError):
            validate_postcode("12345")

    def test_invalid_postcode_range(self):
        with self.assertRaises(ValueError):
            validate_postcode(999)
        with self.assertRaises(ValueError):
            validate_postcode(100000)

    def test_upper_boundary_postcode(self):
        self.assertEqual(validate_postcode(99999), 99999)


class TestValidateVehicleType(unittest.TestCase):
    def test_validate_vehicle_type_valid(self):
        assert validate_vehicle_type("Saloon") == "Saloon"
        assert validate_vehicle_type("Non-Saloon") == "Non-Saloon"
        assert validate_vehicle_type("Motocycle") == "Motocycle"

    def test_validate_vehicle_type_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_vehicle_type(123)

    def test_validate_vehicle_type_invalid_value(self):
        with self.assertRaises(ValueError):
            validate_vehicle_type("Truck")


class TestValidateAll(unittest.TestCase):
    def test_valid_inputs(self):
        result = validate_all(12345, "Saloon", 1500)
        self.assertEqual(result, (12345, "Saloon", 1500))

    def test_invalid_postcode(self):
        with self.assertRaises(InvalidPostcode):
            validate_all("abcde", "Saloon", 1500)

    def test_invalid_vehicle_type(self):
        with self.assertRaises(InvalidVehicleType):
            validate_all(12345, "invalid_type", 1500)

    def test_invalid_vehicle_cc(self):
        with self.assertRaises(InvalidVehicleCC):
            validate_all(12345, "Saloon", "invalid_cc")
