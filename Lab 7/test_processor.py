import pytest
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice

# Edge cases for sanitize_license_plate
@pytest.mark.parametrize("invalid_input", [
    None, 12345, [], {}, "", "   ", "---___###"
])
def test_sanitize_license_plate_edge_cases(invalid_input):
    try:
        sanitize_license_plate(invalid_input)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        pytest.fail(f"sanitize_license_plate crashed unexpectedly with: {e}")

# Edge cases for parse_trip_mileage
@pytest.mark.parametrize("invalid_input", [
    None, 12345, [], {}, "", "abc, def", "100.5,,50.0", "-100"
])
def test_parse_trip_mileage_edge_cases(invalid_input):
    try:
        parse_trip_mileage(invalid_input)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        pytest.fail(f"parse_trip_mileage crashed unexpectedly with: {e}")

# Edge cases for format_rental_invoice
@pytest.mark.parametrize("invalid_input", [
    None, 12345, [], {}, "", "DriverOnly", "Driver:Days", "Alice:-5:Luxury", "Alice:abc:Luxury"
])
def test_format_rental_invoice_edge_cases(invalid_input):
    try:
        format_rental_invoice(invalid_input)
    except (ValueError, TypeError):
        pass
    except Exception as e:
        pytest.fail(f"format_rental_invoice crashed unexpectedly with: {e}")