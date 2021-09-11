from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json, config

from chalicelib.model.shared import Status

@dataclass_json
@dataclass
class AppointmentModel:
    startDate: str = ""
    endDate: str = ""
    id: str = ""
    title: str = ""
    priority: str = ""


@dataclass_json()
@dataclass()
class AppointmentSubmitResult:
    appointment: AppointmentModel
    status: Status


@dataclass_json()
@dataclass()
class AppointmentForMonthResult:
    appointments: List[AppointmentModel]
    status: Status






