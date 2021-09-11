from chalicelib import logger
from chalicelib.dao.crud import CrudDao
from chalicelib.model.crud import Crud, CrudCreateResult, CrudGetResult, crud_model_by_type
from chalicelib.model.shared import Status


class CrudService:

    def __init__(self) -> None:
        self.crud_dao = CrudDao()

    def create(self, crud: Crud) -> CrudCreateResult:
        result = CrudCreateResult(crud, Status(), {})
        try:

            validator = crud.validator().validate(crud)

            if not validator.passed:
                result.errors = validator.errors
            else:
                self.crud_dao.save(crud)
                result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result

    def update(self, crud: Crud) -> CrudCreateResult:
        result = CrudCreateResult(crud, Status(), {})
        try:
            self.crud_dao.update(crud)
            result.status.success = True

            validator = crud.validator().validate(crud)

            if not validator.passed:
               result.errors = validator.errors
            else:
               self.crud_dao.update(crud)
               result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result


    def get(self, id: str, crud_type: str) -> CrudGetResult:
        result = CrudGetResult(crud_model_by_type(crud_type), Status())
        try:
            result.crud = self.crud_dao.get(id, crud_type)
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result



crudService = CrudService()
