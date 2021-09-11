from dataclasses import dataclass, field
from enum import Enum
from typing import List
from dataclasses_json import dataclass_json

from chalicelib.dao.strategies.strategy_three_cuts import EntityPkPrefix
from chalicelib.form.form import FormValidation
from chalicelib.model.shared import Status


class CrudType(Enum):
    NONE = "NONE"
    BOOK = "BOOK"


crud_type_2_entity_prefix: dict = {
    CrudType.NONE.value: EntityPkPrefix.UNNAMED,
    CrudType.BOOK.value: EntityPkPrefix.BOOK
}


def crud_model_by_type(crud_type: str):
    if crud_type == CrudType.BOOK.value:
        return CrudBook()
    return Crud()


@dataclass_json
@dataclass
class Crud:
    crudType: str = CrudType.NONE.value

    def validator(self) -> FormValidation:
        pass


@dataclass_json()
@dataclass()
class CrudCreateResult:
    crud: Crud
    status: Status
    errors: dict


@dataclass_json()
@dataclass()
class CrudGetResult:
    crud: Crud
    status: Status


@dataclass_json
@dataclass
class CrudBook(Crud):
    crudType: str = CrudType.BOOK.value
    arr: List[str] = field(default_factory=lambda: [])
    id: str = ""
    title: str = ""
    isbn: str = ""

    def validator(self) -> FormValidation:
        return CrudBookValidation()



@dataclass()
class CrudBookValidation(FormValidation):

    def validate(self, crud_book: CrudBook) -> FormValidation:
        self.passed = True
        super().required("title", crud_book.title)
        super().len("title", crud_book.title, 2, 50)
        return self