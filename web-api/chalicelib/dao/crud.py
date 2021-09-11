from chalicelib.dao.strategies.strategy_base import BaseDao
from chalicelib.dao.strategies.strategy_three_cuts import JsonDynamoDbEntity
from chalicelib.model.crud import Crud, crud_type_2_entity_prefix, crud_model_by_type


class CrudDao(BaseDao[JsonDynamoDbEntity]):

    def save(self, crud: Crud) -> Crud:
        crud_entity = JsonDynamoDbEntity(entity_name=crud_type_2_entity_prefix[crud.crudType],
                                         fields=JsonDynamoDbEntity.object2dict(crud))
        crud_entity.save()
        crud.id = crud_entity.sk_unique_id
        return crud

    def update(self, crud: Crud) -> Crud:
        crud_entity = JsonDynamoDbEntity(entity_name=crud_type_2_entity_prefix[crud.crudType],
                                         sk_unique_id=crud.id,
                                         fields=JsonDynamoDbEntity.object2dict(crud))
        crud_entity.save()
        return crud

    @staticmethod
    def get(crud_id: str, crud_type: str) -> Crud:
        crud_entity = JsonDynamoDbEntity(entity_name=crud_type_2_entity_prefix[crud_type],
                                         sk_unique_id=crud_id).fetch()
        return crud_model_by_type(crud_type).from_dict(crud_entity.client_model_json.attribute_values)


