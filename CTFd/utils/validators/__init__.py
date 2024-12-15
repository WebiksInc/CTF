import re
from urllib.parse import urljoin, urlparse

from flask import request
from marshmallow import ValidationError

from CTFd.constants.languages import LANGUAGE_NAMES
from CTFd.models import Users
from CTFd.utils.countries import lookup_country_code
from CTFd.utils.user import get_current_user, is_admin

EMAIL_REGEX = r"(^[^@\s]+@[^@\s]+\.[^@\s]+$)"


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def validate_url(url):
    return urlparse(url).scheme.startswith("http")


def validate_email(email):
    # https://github.com/django/django/blob/bc9b6251e0b54c3b5520e3c66578041cc17e4a28/django/core/validators.py#L257
    if not email or "@" not in email or len(email) > 320:
        return False
    return bool(re.match(EMAIL_REGEX, email))


def unique_email(email, model=Users):
    obj = model.query.filter_by(email=email).first()
    if is_admin():
        if obj:
            raise ValidationError("Email address has already been used")
    if obj and obj.id != get_current_user().id:
        raise ValidationError("Email address has already been used")


def validate_country_code(country_code):
    if country_code.strip() == "":
        return
    if lookup_country_code(country_code) is None:
        raise ValidationError("Invalid Country")


def validate_language(language):
    if language.strip() == "":
        return
    if LANGUAGE_NAMES.get(language) is None:
        raise ValidationError("Invalid Language")

def validate_and_format_israeli_phone_number_strict(phone_number):
    """
    Validates and formats an Israeli phone number with strict rules:
    - Starts with +972 and matches valid Israeli mobile/landline formats.
    - Starts with 05 and matches valid Israeli mobile formats.
    
    Args:
        phone_number (str): The phone number to validate.
        
    Returns:
        str: The phone number in the +972... format if valid.
        None: If the phone number is invalid.
    """
    # Regular expression for the two formats
    pattern_plus972 = r"^\+9725[01234578]-?\d{7}$"  # Matches +972 mobile format
    pattern_zero_prefix = r"^05[01234578]-?\d{7}$"  # Matches 0... mobile format with optional -

    # Validate and format +972 format
    if re.match(pattern_plus972, phone_number):
        return phone_number  # Already in +972 format

    # Validate and format 0... format
    elif re.match(pattern_zero_prefix, phone_number):
        # Remove "-" from phone_number
        cleaned_phone_number = phone_number.replace("-", "")
        # Convert 0... to +972...
        return "+972" + cleaned_phone_number[1:]

    # If neither format matches, return None (invalid number)
    return False