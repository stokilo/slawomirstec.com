from chalicelib.dao.contact import ContactDao
from chalicelib.i18n import tc
from chalicelib.model.constants import ErrorCode
from chalicelib.model.contact import ContactModel
from chalicelib.model.contact import ContactModelSubmitResult, ContactFormValidation, Status
from chalicelib.form.validations import validate_normalize_email
from chalicelib import logger

class ContactService:

    def __init__(self) -> None:
        self.contact_dao = ContactDao()

    def save_contact(self, contact_model: ContactModel) -> ContactModelSubmitResult:
        result = ContactModelSubmitResult(contact_model, ContactFormValidation(), Status())
        try:
            result.formValidation.validate_contact(contact_model)
            if not result.formValidation.passed:
                return result

            if self.contact_dao.exists(contact_model.email):
                result.status.error(ErrorCode.FORM_PROCESSING_ERROR, tc("contact.already.exists"))
            else:
                self.normalize_email(contact_model)
                self.contact_dao.create_contact(contact_model)
                result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result

    @staticmethod
    def normalize_email(contact_model: ContactModel):
        (is_valid, normalized_email) = validate_normalize_email(contact_model.email)
        if is_valid:
            contact_model.email = normalized_email


contactService = ContactService()
