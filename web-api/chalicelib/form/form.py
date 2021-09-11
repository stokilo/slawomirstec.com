from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import TypeVar, Dict, List
from chalicelib.i18n import tf
from chalicelib.form.validations import validate_normalize_email

T = TypeVar('T')


@dataclass_json
@dataclass
class FormValidation:
    """Server side form field errors wrapper
    """
    errors: Dict[str, List] = field(default_factory=dict)
    passed: bool = False

    def add_error(self, field_name: str, field_error: str):
        self.passed = False
        if not field_name in self.errors:
            self.errors[field_name] = [field_error]
        else:
            self.errors[field_name].append(field_error)

    def required(self, field_name: str, field_value: str):
        if not len(field_value):
            self.add_error(field_name, tf("field.is.required", dict(field=field_name)))

    def len(self, field_name: str, field_value: str, min: int = 0, max: int = 250):
        value_length = len(field_value)
        if (value_length > 0) and (value_length < min or value_length > max):
            self.add_error(field_name, tf("field.len", dict(field=field_name,
                                                            min=min,
                                                            max=max,
                                                            current=value_length)))

    def email(self, field_name: str, field_value: str):
        (is_valid, _) = validate_normalize_email(field_value)
        if not is_valid:
            self.add_error(field_name, tf("field.email"))
