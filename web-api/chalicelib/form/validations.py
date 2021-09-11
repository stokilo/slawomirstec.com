from email_validator import validate_email, EmailNotValidError


def validate_normalize_email(email: str) -> (bool, str):
    """Perform email validation and return tuple with boolean flag is_valid.
    Additionally it performs normalization of the email address described here:
    https://pypi.org/project/email-validator/

    """
    is_valid = False
    normalized = email
    try:
        valid = validate_email(email, check_deliverability=False)
        is_valid = True
        normalized = valid.email
    except EmailNotValidError as e:
        is_valid = False
    return is_valid, normalized
