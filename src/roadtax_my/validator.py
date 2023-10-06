from typing import Any

from .exception import (
    InvalidPostcode,
    InvalidVehicleCC,
    InvalidVehicleType
)


def validate_vehicle_cc(vehicle_cc: int, *args: tuple, **kwargs: dict[str, Any]) -> int:
    if not isinstance(vehicle_cc, int):
        raise TypeError("Vehicle CC must be an integer")
    if not 0 < vehicle_cc < 100000:
        raise ValueError("Vehicle CC not in range (0, 99999)")
    return vehicle_cc


def validate_postcode(postcode: int, *args: tuple, **kwargs: dict[str, Any]) -> int:
    if not isinstance(postcode, int):
        raise TypeError("Postcode must be an integer")
    if not 1000 < postcode < 100000:
        raise ValueError("Postcode not in range (1000, 99999)")
    return postcode


def validate_vehicle_type(vehicle_type: str, *args: tuple, **kwargs: dict[str, Any]) -> str:
    if not isinstance(vehicle_type, str):
        raise TypeError("Vehicle type must be a string")
    if not vehicle_type in {"Saloon", "Non-Saloon", "Motocycle"}:
        raise ValueError(
            "Vehicle type not in {'Saloon', 'Non-Saloon', 'Motocycle'}"
        )
    return vehicle_type


def validate_all(
    postcode: int,
    vehicle_type: str,
    vehicle_cc: int,
    *args: tuple,
    **kwargs: dict[str, Any],
) -> tuple[int, str, int]:
    try:
        postcode = validate_postcode(postcode=postcode)
    except (ValueError, TypeError) as error:
        raise InvalidPostcode(
            f"{error.__class__.__name__}: {error}") from error
    try:
        vehicle_type = validate_vehicle_type(vehicle_type=vehicle_type)
    except (ValueError, TypeError) as error:
        raise InvalidVehicleType(
            f"{error.__class__.__name__}: {error}") from error
    try:
        vehicle_cc = validate_vehicle_cc(vehicle_cc=vehicle_cc)
    except (ValueError, TypeError) as error:
        raise InvalidVehicleCC(
            f"{error.__class__.__name__}: {error}") from error
    return postcode, vehicle_type, vehicle_cc
