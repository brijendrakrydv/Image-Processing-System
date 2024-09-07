def validate_csv(csv_rows):
    if len(csv_rows[0]) != 3:  # Ensure CSV has 3 columns
        return False
    for row in csv_rows[1:]:
        if not row[1] or not row[2]:  # Check for product name and image URLs
            return False
    return True
