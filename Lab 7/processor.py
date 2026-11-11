import re

def sanitize_license_plate(plate_input):
    if not isinstance(plate_input, str):
        raise TypeError("Input must be a string")
    plate_input = plate_input.strip()
    if not plate_input:
        raise ValueError("License plate cannot be empty")
    return re.sub(r'[\-_#]', '', plate_input).upper()

def parse_trip_mileage(csv_input):
    if not isinstance(csv_input, str):
        raise TypeError("Input must be a string")
    mileages = []
    for item in csv_input.split(','):
        item = item.strip()
        if not item:
            continue
        mileages.append(float(item))
    return mileages

def format_rental_invoice(record_input):
    if not isinstance(record_input, str):
        raise TypeError("Input must be a string")
    parts = record_input.split(':')
    if len(parts) != 3:
        raise ValueError("Invalid format. Expected 'Driver:Days:Category'")
    driver, days_str, category = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not driver or not category:
        raise ValueError("Driver and Category cannot be empty")
    days = int(days_str)
    if days <= 0:
        raise ValueError("Days must be positive")
    return f"Driver: {driver} | Days: {days} | Category: {category}"

def main():
    print("==== Running sanitize_license_plate ====")
    try:
        plate = input("Enter license plate with delimiters (-, _, #): ")
        print("Sanitized Plate:", sanitize_license_plate(plate))
    except Exception as e:
        print("Error:", e)

    print("\n==== Running parse_trip_mileage ====")
    try:
        mileage = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
        print("Parsed Mileage List:", parse_trip_mileage(mileage))
    except Exception as e:
        print("Error:", e)

    print("\n==== Running format_rental_invoice ====")
    try:
        record = input("Enter rental record (Driver:Days:Category): ")
        print("Invoice:", format_rental_invoice(record))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()