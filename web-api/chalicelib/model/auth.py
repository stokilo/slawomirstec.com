from dataclasses import dataclass
from dataclasses_json import dataclass_json
from chalicelib.form.form import FormValidation
from chalicelib.model.shared import Status, Auth


@dataclass_json
@dataclass
class SignUpModel:
    email: str = ""
    password: str = ""


@dataclass()
class SignUpFormValidation(FormValidation):
    """Validation form for signup
    """

    def validate_signup(self, sign_up: SignUpModel):
        """Validate signup model
        """

        self.passed = True
        super().required("email", sign_up.email)
        super().required("password", sign_up.password)

        super().len("email", sign_up.email, 3, 250)
        super().len("password", sign_up.password, 7, 250)

        super().email("email", sign_up.email)



@dataclass_json()
@dataclass()
class SignUpSubmitResult:
    formValidation: SignUpFormValidation
    status: Status

@dataclass_json
@dataclass
class UserProfileModel:
    firstName: str = ""
    lastName: str = ""
    profileImagePath: str = ""

@dataclass_json
@dataclass
class LoginModel:
    email: str = ""
    password: str = ""


@dataclass()
class LoginFormValidation(FormValidation):
    """Validation form for login
    """

    def validate_login(self, login: LoginModel):
        """Validate login model
        """

        self.passed = True
        super().required("email", login.email)
        super().required("password", login.password)

        super().len("email", login.email, 3, 250)
        super().len("password", login.password, 7, 250)

        super().email("email", login.email)


@dataclass_json()
@dataclass()
class LoginSubmitResult:
    formValidation: LoginFormValidation
    status: Status
    auth: Auth
    userProfile: UserProfileModel


@dataclass_json()
@dataclass()
class UserProfileUpdateResult:
    status: Status
    userProfile: UserProfileModel


@dataclass_json
@dataclass
class RefreshTokenModel:
    refreshToken: str = ""


@dataclass_json()
@dataclass()
class RefreshTokenSubmitResult:
    status: Status
    auth: Auth