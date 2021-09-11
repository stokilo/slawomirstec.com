from chalicelib.i18n.shared import DictWithUniqueKeys

AUTH_TRANSLATIONS = DictWithUniqueKeys(
    {
        "user.already.exists": {
            "en": "User already exists",
            "pl": "User juz istnieje"
        },
        "user.not.found": {
            "en": "Could not find the user",
            "pl": "Nie znaleziono uzytkownika"
        },
        "invalid.password": {
            "en": "Invalid password",
            "pl": "Nieprawidlowe haslo"
        }
    }
)

