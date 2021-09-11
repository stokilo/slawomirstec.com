from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from chalicelib.model.shared import Status


@dataclass_json
@dataclass
class TodoModel:
    id: str = ""
    date: str = ""
    subject: str = ""
    details: str = ""
    status: str = ""
    category: str = ""
    label: str = ""


@dataclass_json
@dataclass
class TodosArray:
    todos: List[TodoModel]


@dataclass_json()
@dataclass()
class TodoSubmitResult:
    todoModel: TodoModel
    status: Status



@dataclass_json()
@dataclass(eq=True, order=True)
class TodoGetResult:
    items: object
    status: Status
