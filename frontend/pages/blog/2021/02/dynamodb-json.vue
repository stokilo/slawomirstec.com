<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Storing JSON as a map attribute in the DynamoDB">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/02/dynamodb-json.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="DynamoDb JSON column"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Map attribute colum</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Storing JSON as a map attribute in the DynamoDB</h3>
                <p></p>
                <p>
                PynamoDB defines a MapAttribute class to store raw key-value pairs. It is possible to use it in two ways.
                The first option is to define each map attribute as an instance of the Attribute class. For example,
                I've used this approach for the appointment item definition like below:
                </p>

                <client-only>
                  <highlightjs langugage="python" :code="snippet1"/>
                </client-only>
                <p></p>
                <p>
                The second option is to define a Map and fill it with raw data, it can be for example a serialized object
                in the JSON format passed as python dict. This post contains the code I've written for it.
                </p>

                <p>
                What I wanted to achieve is a quite common scenario for CRUD operations on simple entities.
                The javascript client-side defines a model object that should be stored on the backend. Let's assume it is implemented
                in TypeScript and all field types are defined. Such an object is serialized to the JSON format and send to the backend.
                The backend has the same definition of the model implemented in python. The field types are well defined, same as on the client-side,
                the model class is annotated with @dataclass_json and @dataclass annotations. We get working IDE autocomplete and a type check support
                on both, client and backend side. However, there is another mapping required, from the backend model to a DynamoDB entity model.
                If I would use the model with fields described with the Attribute class, like in AppointmentItem, I have to maintain a mapping for it.
                So the backend model is like following:
                </p>

                <client-only>
                  <highlightjs langugage="python" :code="snippet_model"/>
                </client-only>
                <p></p>
                <p>
                The MapAttribute raw values can be mapped automatically when being passed a dict instance. Empty values are not allowed and cause an error
                on entity save action. I've defined a testcase for CRUD operations, a strategy to implement storing raw MapAttributes and
                a DAO layer to use it. Sample code below.
                </p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet_test"/>
                </client-only>

                <client-only>
                  <highlightjs langugage="python" :code="snippet_strategy"/>
                </client-only>

                <client-only>
                  <highlightjs langugage="python" :code="snippet_dao"/>
                </client-only>

                <p></p>
                <p>
                I've decided to use a trick for converting nested objects to python dict. Firstly, I convert it to JSON, then to python dict.
                Empty values and None values are deleted from the model. Please note, this is testing code only, however, allowed me to
                save automatically my client objects without maintaining any mappings.
                </p>

                <p>
                Additionally, I've defined a strategy for storing entities with MapAttribute column, each row in DynamoDb consist of
                three columns, PK (prefix + unique client id), SK (prefix + entity id), client_model_json (MapAttribute).
                This is for modeling a 1-to-many relationship for entities created by the user. This is another common scenario that
                is nice to have automatically handled on the backend side.
                </p>
              </div>

            </b-card-body>
          </b-card>
        </b-row>
      </div>
    </b-tab>
  </b-tabs>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import ResponsiveImageTag from '~/components/common/ResponsiveImageTag.vue'
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";


@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag
  },
  head: {
    title: 'Storing JSON as a map attribute in the DynamoDB',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Storing JSON as a map attribute in the DynamoDB'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'dynamodb, json, mapattribute, map, pynamodb, column'
      }
    ]
  }
})
export default class CloudflareKvCache extends Vue {

  snippet1: String = `
class AppointmentItem(MapAttribute):
    id = UnicodeAttribute()
    startDate = UnicodeAttribute()
    endDate = UnicodeAttribute()
    title = UnicodeAttribute()
    priority = UnicodeAttribute()

`
 snippet_model: String = `
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
`

 snippet_test: String = `
from chalicelib.model.crud import CrudType
from chalicelib.routes.constants import *
from .lib.helpers import *
import pytest


@pytest.mark.usefixtures('class_client')
class TestCrud(object):

    def test_crud(self, gateway_factory):
        gateway = gateway_factory()

        crudType = CrudType.BOOK.value
        payload = {
            "crudType": crudType,
            "id": uuid.uuid4().__str__(),
            "title": "",
            "isbn": "99921-58-10-7",
            "arr": ["1", "2"]
        }

        payload_string = json.dumps(payload)
        response = post(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json['status']['success'] == False
        assert body_as_json['errors']['title'][0] == 'Field is required'

        payload['title'] = 'test_title'
        payload_string = json.dumps(payload)
        response = post(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True

        payload['id'] = body_as_json['crud']['id']
        payload['title'] = "test_title_updated"
        payload_string = json.dumps(payload)
        response = put(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True
        assert body_as_json['crud']['title'] == "test_title_updated"

        id = body_as_json['crud']['id']
        response = get(gateway, f"{ROUTE_CRUD}?id={id}&crudType={crudType}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True
        assert body_as_json['crud']['title'] == "test_title_updated"
        assert body_as_json['crud']['isbn'] == "99921-58-10-7"


 `

  snippet_strategy: String = `
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
`

   snippet_dao: String = `
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



`

}
</script>

