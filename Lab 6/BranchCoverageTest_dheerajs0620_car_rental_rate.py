import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

# --- Branch Coverage: Input Validation ---

def test_invalid_rentals_type_branch():
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet(12345, 10.0)

def test_invalid_admin_fee_branch():
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet([], -1.0)


# --- Branch Coverage: Rental Filter & Defaults ---

def test_unconfirmed_rental_branch():
    # Branch: is_confirmed is False
    rentals = [{"is_confirmed": False}]
    result = process_rental_fleet(rentals, 5.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}

def test_invalid_days_branch():
    # Branch: days <= 0 is True
    rentals = [{"is_confirmed": True, "days": -1}]
    result = process_rental_fleet(rentals, 5.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


# --- Branch Coverage: Vehicle Types ---

def test_luxury_vehicle_branch():
    # Branch: vehicle_type == "luxury"
    rentals = [{"is_confirmed": True, "vehicle_type": "luxury", "days": 1, "driver_age": 30}]
    # (120*1) + 10 = 130.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 130.0

def test_suv_vehicle_branch():
    # Branch: vehicle_type == "suv"
    rentals = [{"is_confirmed": True, "vehicle_type": "suv", "days": 1, "driver_age": 30}]
    # (70*1) + 10 = 80.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 80.0

def test_economy_vehicle_branch():
    # Branch: vehicle_type defaults to "economy" (else path)
    rentals = [{"is_confirmed": True, "vehicle_type": "economy", "days": 1, "driver_age": 30}]
    # (40*1) + 10 = 50.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0


# --- Branch Coverage: Trip Segments & Driver Age ---

def test_trip_segment_negative_miles_branch():
    # Branch: miles < 0
    rentals = [{"is_confirmed": True, "days": 1, "trip_segments": [-10]}]
    result = process_rental_fleet(rentals, 10.0)
    # Risk flag triggered, no segment miles added -> (40*1) + 10 = 50.0
    assert result["total_revenue"] == 50.0

def test_trip_segment_under_300_miles_branch():
    # Branch: miles <= 300 (else path)
    rentals = [{"is_confirmed": True, "days": 1, "trip_segments": [100]}]
    # 40 + 10 + (100 * 0.20) = 70.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 70.0

def test_trip_segment_over_300_young_driver_branch():
    # Branch: miles > 300 AND driver_age < 21
    rentals = [{"is_confirmed": True, "days": 1, "driver_age": 19, "trip_segments": [350]}]
    # 40 + 10 + 250 + (20*1) = 320.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 320.0

def test_trip_segment_over_300_older_driver_branch():
    # Branch: miles > 300 AND driver_age >= 21
    rentals = [{"is_confirmed": True, "days": 1, "driver_age": 22, "trip_segments": [350]}]
    # 40 + 10 + (350 * 0.40) + (20*1) = 40 + 10 + 140 + 20 = 210.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 210.0


# --- Branch Coverage: Driver Surcharges ---

def test_young_driver_luxury_surcharge_branch():
    # Branch: driver_age < 25 AND vehicle_type == "luxury"
    rentals = [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 24, "days": 2}]
    # (120*2) + 10 + (50*2) = 240 + 10 + 100 = 350.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 350.0

def test_young_driver_non_luxury_surcharge_branch():
    # Branch: driver_age < 25 AND vehicle_type != "luxury"
    rentals = [{"is_confirmed": True, "vehicle_type": "economy", "driver_age": 24, "days": 2}]
    # (40*2) + 10 + (20*2) = 80 + 10 + 40 = 130.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 130.0

def test_older_driver_no_surcharge_branch():
    # Branch: driver_age >= 25 (False path for driver_age < 25)
    rentals = [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 25, "days": 1}]
    # (120*1) + 10 = 130.0
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 130.0


# --- Branch Coverage: Return Statuses ---

def test_high_risk_audit_branch():
    # Branch: risk_flags > 4
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0}
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["status"] == "HIGH_RISK_AUDIT"

def test_empty_batch_branch():
    # Branch: total_revenue == 0.0
    result = process_rental_fleet([], 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


# --- Branch Coverage: check_fleet_telematics ---

def test_telematics_empty_matrix_branch():
    # Branch: not telematics_matrix is True
    assert check_fleet_telematics([]) == "NO_DATA"

def test_telematics_ground_vehicle_branch():
    # Branch: speed > 100 True twice in a row
    assert check_fleet_telematics([[120, 110]]) == "GROUND_VEHICLE"

def test_telematics_reset_streak_branch():
    # Branch: speed > 100 followed by speed <= 100 (resets streak)
    assert check_fleet_telematics([[120, 90, 110]]) == "SAFE"