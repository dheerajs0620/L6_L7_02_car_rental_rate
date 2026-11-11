import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


# --- Line Coverage Tests: process_rental_fleet ---

def test_invalid_input_types():
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet("not_a_list", 10.0)
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet([], -5.0)


def test_unconfirmed_and_invalid_days():
    rentals = [
        {"is_confirmed": False},
        {"is_confirmed": True, "days": 0}  # Triggers risk_flags += 1
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_luxury_young_driver_high_miles():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 20,
            "days": 2,
            "trip_segments": [350]  # triggers miles > 300 & age < 21 break
        }
    ]
    # (120*2) + 10 + 250 + (50*2) = 240 + 10 + 250 + 100 = 600.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 600.0
    assert result["status"] == "STANDARD"


def test_suv_young_driver_normal_miles():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 24,
            "days": 1,
            "trip_segments": [-5, 350, 50]  # triggers miles < 0 and miles > 300 (age >= 21)
        }
    ]
    # (70*1) + 10 + (350 * 0.40) + (50 * 0.20) + (20*1) = 70 + 10 + 140 + 10 + 20 = 250.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 250.0
    assert result["status"] == "STANDARD"


def test_high_risk_audit_status():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0}
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["status"] == "HIGH_RISK_AUDIT"


# --- Line Coverage Tests: check_fleet_telematics ---

def test_telematics_empty():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_ground_vehicle():
    matrix = [[80, 105, 110]]
    assert check_fleet_telematics(matrix) == "GROUND_VEHICLE"


def test_telematics_safe():
    matrix = [[80, 105, 90, 105]]
    assert check_fleet_telematics(matrix) == "SAFE"