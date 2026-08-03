"""BMI calculation and validation helpers."""

CATEGORY_DETAILS = {
    "Underweight": ("#3B82F6", "A balanced, nourishing diet may help you reach a healthy range."),
    "Normal": ("#16A34A", "Great—maintain your healthy habits with regular activity and sleep."),
    "Overweight": ("#F59E0B", "Small, sustainable nutrition and activity changes can make a difference."),
    "Obese": ("#DC2626", "Consider discussing a personalised health plan with a qualified professional."),
}


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Return BMI rounded to two decimal places."""
    return round(weight_kg / height_m**2, 2)


def get_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def validate_input(weight: float, height: float, age: int | None = None) -> tuple[bool, str]:
    """Validate inputs before calculating BMI."""
    if not 10 <= weight <= 500:
        return False, "Weight must be between 10 and 500 kg."
    if not 0.5 <= height <= 3.0:
        return False, "Height must be between 0.50 and 3.00 metres."
    if age is not None and not 1 <= age <= 120:
        return False, "Age must be between 1 and 120 years."
    return True, "Valid input"


def healthy_weight_range(height_m: float) -> tuple[float, float]:
    """Return the WHO adult healthy-weight range for a height."""
    return round(18.5 * height_m**2, 1), round(24.9 * height_m**2, 1)


def imperial_to_metric(weight_lb: float, height_ft: int, height_in: float) -> tuple[float, float]:
    """Convert pounds and feet/inches to kilograms and metres."""
    return round(weight_lb * 0.45359237, 2), round((height_ft * 12 + height_in) * 0.0254, 2)
