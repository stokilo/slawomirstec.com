from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List
from dataclasses_json import dataclass_json

from chalicelib.model.shared import Status


class DashboardLogItemType(Enum):
    USER_CREATION = "USER_CREATION"
    TODO_CREATION = "TODO_CREATION"
    CONTACT_CREATION = "CONTACT_CREATION"


@dataclass_json
@dataclass
class DashboardStats:
    contactCount: int
    userCount: int
    todoCount: int


@dataclass_json
@dataclass
class DashboardLogItem:
    type: str
    time: date


@dataclass_json
@dataclass
class Dashboard:
    stats: DashboardStats
    logs: List[DashboardLogItem]


@dataclass_json()
@dataclass(eq=True, order=True)
class DashboardGetResult:
    dashboard: Dashboard
    status: Status