from typing import Any, Literal

from .data import roadtax_data
from .exception import (
    InvalidPostcode,
    InvalidVehicleCC,
    InvalidVehicleType,
)

from .validator import (
    validate_postcode,
    validate_vehicle_cc,
    validate_all,
)


def filter_data(data: dict[str, dict[str, list[dict[str, float | int]]]], region: str, vehicle_type: str, vehicle_cc: int, *args, **kwargs) -> dict[str, float | int] | dict:
    """
    Filter data based on region, vehicle type, and vehicle cc.

    Args:
        data (dict[str, dict[str, list[dict[str, float | int]]]]): The data to filter.
        region (str): The region to filter by.
        vehicle_type (str): The vehicle type to filter by.
        vehicle_cc (int): The vehicle cc to filter by.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        dict[str, float | int] | dict: The filtered data.

    """
    return next(filter(lambda x: x.get("start_range", 0) <= vehicle_cc <= x.get("end_range", 0), data.get(vehicle_type, {}).get(region, [])), {})


def get_region(postcode: int, *args: tuple, **kwargs: dict[str, Any]) -> Literal["East", "West"]:
    """
    Determines the region based on a given postcode.

    Args:
        postcode (int): The postcode to be validated and used for determining the region.
        *args (tuple): Additional positional arguments.
        **kwargs (dict[str, Any]): Additional keyword arguments.

    Returns:
        Literal["East", "West"]: The region determined based on the postcode.

    Raises:
        InvalidPostcode: If the postcode is invalid.

    """
    try:
        postcode = validate_postcode(postcode=postcode)
        return "East" if 80000 <= postcode <= 99999 else "West"
    except (ValueError, TypeError) as error:
        raise InvalidPostcode(
            f"{error.__class__.__name__}: {error}") from error


def base_calculation(
    vehicle_cc: int,
    start_range: int,
    base_rate: float,
    progressive_rate: float,
    *args: tuple,
    **kwargs: dict[str, Any]
) -> float:
    """
    Calculate the cost of vehicle road tax based on the vehicle's cc, start range, and rate.

    Args:
        vehicle_cc (int): The cc of the vehicle.
        start_range (int): The start range for calculating the road tax cost.
        base_rate (float): The base rate for calculating the road tax cost.
        progressive_rate (float): The progressive rate for calculating the road tax cost.
        *args (tuple): Additional positional arguments.
        **kwargs (dict[str, Any]): Additional keyword arguments.

    Returns:
        float: The calculated cost of vehicle road tax.
    Raises:
        InvalidVehicleCC: If the vehicle_cc is invalid.
    """
    try:
        vehicle_cc = validate_vehicle_cc(vehicle_cc=vehicle_cc)
        return base_rate + progressive_rate * (vehicle_cc - start_range)
    except (ValueError, TypeError) as error:
        raise InvalidVehicleCC(
            f"{error.__class__.__name__}: {error}") from error


def can_discount(postcode: int, vehicle_type: str, vehicle_cc: int, *args: tuple, **kwargs: dict[str, Any]) -> bool:
    """
    Checks if a discount can be applied based on the given parameters.

    Parameters:
        postcode (int): The postcode of the customer.
        vehicle_type (str): The type of the vehicle.
        vehicle_cc (int): The cubic centimeters of the vehicle.
        *args (tuple): Variable length argument list.
        **kwargs (dict[str, Any]): Arbitrary keyword arguments.

    Returns:
        bool: True if a discount can be applied, False otherwise.
    Raises:
        InvalidVehicleCC: If the vehicle_cc is invalid.
        InvalidVehicleType: If the vehicle_type is invalid.
        InvalidPostcode: If the postcode is invalid.
    """
    try:
        postcode, vehicle_type, vehicle_cc = validate_all(
            postcode=postcode,
            vehicle_type=vehicle_type,
            vehicle_cc=vehicle_cc,
        )
        return all({
            vehicle_cc > 1_000,
            vehicle_type != "Motocycle",
            postcode in {7000, 7100, 32300, 87000}
        })
    except (InvalidPostcode, InvalidVehicleCC, InvalidVehicleType) as error:
        raise error


def calculate(
    postcode: int,
    vehicle_type: str,
    vehicle_cc: int,
    data: dict[str, dict[str, list[dict[str, float | int]]]] = roadtax_data,
    *args: tuple,
    **kwargs: dict[str, Any],
) -> float:
    """
    Calculate the road tax based on the given postcode, vehicle type, and vehicle cc.

    Args:
        postcode (int): The postcode of the location where the vehicle is registered.
        vehicle_type (str): The type of the vehicle.
        vehicle_cc (int): The cubic centimeter (cc) of the vehicle engine.
        data (dict[str, dict[str, list[dict[str, float | int]]]], optional): The road tax data used for calculation. Defaults to roadtax_data.
        *args (tuple): Additional positional arguments.
        **kwargs (dict[str, Any]): Additional keyword arguments.

    Returns:
        float: The calculated road tax.

    Raises:
        InvalidPostcode: If the postcode is invalid.
        InvalidVehicleCC: If the vehicle cc is invalid.
        InvalidVehicleType: If the vehicle type is invalid.
    """
    try:
        postcode, vehicle_type, vehicle_cc = validate_all(
            postcode=postcode,
            vehicle_type=vehicle_type,
            vehicle_cc=vehicle_cc,
        )
    except (InvalidPostcode, InvalidVehicleCC, InvalidVehicleType) as error:
        raise error
    filtered_data = filter_data(data=data, region=get_region(
        postcode=postcode), vehicle_type=vehicle_type, vehicle_cc=vehicle_cc)
    base_value = base_calculation(
        vehicle_cc=vehicle_cc,
        start_range=filtered_data.get("start_range", 0),
        base_rate=filtered_data.get("base_rate", 0),
        progressive_rate=filtered_data.get("progressive_rate", 0),
    )
    return base_value / 2 if can_discount(postcode=postcode, vehicle_type=vehicle_type, vehicle_cc=vehicle_cc) else base_value
