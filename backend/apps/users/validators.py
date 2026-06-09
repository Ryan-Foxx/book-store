import re

from django.core.exceptions import ValidationError


def normalize_ir_mobile(value):
    """
    Normalize an Iranian mobile number to E.164 format.

    Accepted input formats:
    - 09123456789
    - 989123456789
    - +989123456789
    - 9123456789

    Normalized output:
    - +989123456789
    """
    if not value:
        return value

    # Convert to string and remove leading/trailing spaces
    value = str(value).strip()

    # Remove spaces and dashes to support user-friendly input
    value = re.sub(r"[\s\-]", "", value)

    # Accept Iranian mobile numbers with or without country/local prefix
    # and capture the local mobile part starting with 9
    match = re.fullmatch(r"^(?:\+98|98|0)?(9\d{9})$", value)
    if not match:
        raise ValidationError("The mobile number entered is not valid.")

    # Return the normalized E.164 format
    return f"+98{match.group(1)}"


def validate_iranian_mobile(value):
    """
    Validate the Iranian mobile number format.

    This function relies on normalize_ir_mobile() to raise
    ValidationError if the input is invalid.
    """
    normalize_ir_mobile(value)
