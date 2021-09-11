from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pynamodb.attributes import UTCDateTimeAttribute

from chalicelib.model.shared import Status
from chalicelib.form.form import FormValidation


@dataclass_json
@dataclass
class ContactModel:
    name: str = ""
    email: str = ""
    details: str = ""
    creation_date = UTCDateTimeAttribute()


@dataclass()
class ContactFormValidation(FormValidation):
    """Validation form for contact
    """

    def validate_contact(self, contact_model: ContactModel):
        """Validate contact model
        :param contact_model:
        :return:
        """

        self.passed = True

        super().required("name", contact_model.name)
        super().required("email", contact_model.email)
        super().required("details", contact_model.details)

        super().len("name", contact_model.name, 5, 250)
        super().len("email", contact_model.email, 3, 250)
        super().len("details", contact_model.details, 5, 250)

        super().email("email", contact_model.email)


@dataclass_json()
@dataclass()
class ContactModelSubmitResult:
    contactModel: ContactModel
    formValidation: ContactFormValidation
    status: Status
