from contextvars import ContextVar
from chalicelib.model.request import REQUEST_SCOPE

def t(translation_set: dict):
    """Closure for reusing functions across all translation sets.
    What we try to avoid here is to always import all translations into lambda runtime.
    Solution is to split translations per modules and import only the one that are really
    needed.

    :param translation_set: this is a dictionary with translations that will be used for translate function
    """
    def translate(translation_key: str, placeholders: dict = None) -> str:
        """Translate given key with optional placeholders
        """
        if placeholders is None:
            placeholders = {}
        translation = translation_set.get(translation_key, "")
        # language is determined by client request headers
        request_languages = REQUEST_SCOPE.get().language()
        # % replaces all %()s instances
        return translation[request_languages] % placeholders
    return translate


class DictWithUniqueKeys(dict):
    def __setitem__(self, key, value):
        """Dictionary that will raise an error when duplicate is detected.
        We want to get an error in case of mistake of adding same translation twice.
        """
        if key not in self and len(key):
            dict.__setitem__(self, key, value)
        else:
            raise KeyError(f"Key {key} already exists")


GLOBAL_SERVICE_ERROR_TRANSLATIONS = DictWithUniqueKeys(
    {
        "generic.error": {
            "en": "Unknown error, please contact administrator.",
            "pl": "Nieznany blad, prosze o kontakt z administratorem."
        }
    }
)

GLOBAL_FORM_VALIDATION_TRANSLATIONS = DictWithUniqueKeys(
    {
        "field.is.required": {
            "en": "Field is required",
            "pl": "Pole jest wymagane"
        },
        "field.len": {
            "en": "Min length is %(min)s, max %(max)s, provided %(current)s",
            "pl": "Minimalna dlugosc %(min)s, maksymalna %(max)s ale podana %(current)s",
        },
        "field.email": {
            "en": "Email is not valid",
            "pl": "Niepoprawny adres email",
        },
    }
)
