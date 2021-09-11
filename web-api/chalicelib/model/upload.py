from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json
from chalicelib.model.shared import Status


@dataclass_json()
@dataclass()
class SignedUploadUrlResponse:
    upload: Dict
    status: Status


