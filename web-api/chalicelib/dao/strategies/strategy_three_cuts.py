import json
from enum import Enum
import jsonpickle
import ksuid.ksuid
from botocore.session import Session
from pynamodb.attributes import UnicodeAttribute, MapAttribute
from pynamodb.models import Model
from chalicelib import REQUEST_SCOPE

""" Three cuts strategy 

It is simple strategy that uses 3 columns in DynamoDb table: 

pk
sk
client_model_json

pk : value is combination of enum value for EntityPkPrefix and unique client id from user table.
     This behavior can be overwritten, by default it was designed to store data for users.
     
sk : value is combinations of enum value for EntityPkPrefix and ksuid(), this can be overwritten depending
     on access pattern foreseen for the entity
     
client_model_json : value is a map, its key and values can be converted from any class annotated with dataclass_json.
                    empty and null fields are removed from the map before save.
                    
In result, we get 1-to-many relation where entity primary key is stored in sk suffix. Example:
{
  "client_model_json": {
    "crudType": "BOOK",
    "id": "0cc41e612200b9b5343ee79e558053e7f44dbc42",
    "title": "test_title_updated"
  },
  "pk": "BOOK#c50c68e6-1122-446e-9a6e-c683f6613387-696598051307043570",
  "sk": "BOOK#0cc41e612200b9b5343ee79e558053e7f44dbc42"
}

Access pattern:

- get entity by id  (because entity id is part of SK)
- get user last N entities by date (because of ksuid)

Note: this strategy allows to store any JSON data, see generic CRUD support in REST/Service/Dao layer.
"""

class EntityPkPrefix(Enum):
    """List all possible pk prefixes in three cuts strategy"""
    UNNAMED = "UNNAMED"
    BOOK = "BOOK"


class PyAwsEntity(Model):
    """ Pure (pure means with no fields, only table name and region) base entity for PynamoDb models.
    """

    class Meta:
        table_name = "PyAwsV1"
        region = Session().get_config_variable('region')


class JsonDynamoDbEntity(PyAwsEntity):
    """ Model for storing models objects as a json field (map attribute)
    """

    class Meta(PyAwsEntity.Meta):
        initialized = True

    def __init__(self,
                 entity_name: EntityPkPrefix = EntityPkPrefix.UNNAMED,
                 pk_unique_id: str = None,
                 sk_unique_id: str = None,
                 fields: dict = None,
                 **kwargs):
        """

        :param entity_name: enum value that is first part of pk value (entity_name#unique_id)
        :param pk_unique_id: unique value of pk, defaults to authenticated user id
        :param sk_unique_id: unique sort key, defaults to ksuid
        :param fields: client model object fields passed as dict
        """
        super().__init__()

        self.pk_unique_id = REQUEST_SCOPE.get().auth_client_id if pk_unique_id is None else pk_unique_id
        self.sk_unique_id = ksuid.ksuid().__str__() if sk_unique_id is None else sk_unique_id
        self.client_model_json = MapAttribute(**{}) if fields is None else MapAttribute(**fields)
        self.pk = f"{entity_name.value}#{self.pk_unique_id}"
        self.sk = f"{entity_name.value}#{self.sk_unique_id}"

        # PynamoDB will call the constructor with _user_instantiated=False while binding data from DynamoDb to the model
        if "_user_instantiated" in kwargs and not kwargs.get("_user_instantiated"):
            self.client_model_json = kwargs.get("client_model_json")

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    client_model_json = MapAttribute()

    def fetch(self):
        return self.get(hash_key=self.pk, range_key=self.sk)

    @staticmethod
    def object2dict(model):
        # conversion of the model to the dict, supports nested object (trick is json conversion first, then to dict)
        fields_dict = json.loads(jsonpickle.encode(model, unpicklable=False))
        # filter None and empty strings, map values are not null be default so we get an error if we pass empty value
        return {k: v for k, v in fields_dict.items() if v is not None and len(v)}
