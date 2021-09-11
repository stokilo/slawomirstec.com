from botocore.session import Session
from pynamodb.connection import Connection
from pynamodb.transactions import TransactWrite

from chalicelib.dao.dashboard import DashboardDao
from chalicelib.dao.strategies.strategy_base import BaseEntityForPyAwsV1, BaseDao
from chalicelib.model.contact import ContactModel
from pynamodb.attributes import UnicodeAttribute

from chalicelib.model.dashboard import DashboardLogItemType


class ContactEntity(BaseEntityForPyAwsV1):
    """Entity for Contact me page
    """
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)

    name = UnicodeAttribute()
    email = UnicodeAttribute()
    details = UnicodeAttribute(null=True)

    def prefix(self) -> str:
        return "CONTACT#"


class ContactDao(BaseDao[ContactEntity]):

    def create_contact(self, contact_model: ContactModel) -> ContactModel:
        contact = ContactEntity(contact_model.email)
        contact.name = contact_model.name
        contact.email = contact_model.email
        contact.details = contact_model.details
        dashboard_dao = DashboardDao()

        connection = Connection(region=Session().get_config_variable('region'))
        with TransactWrite(connection=connection) as transaction:
            transaction.save(contact)
            dashboard_dao.add_audit_event(transaction, DashboardLogItemType.CONTACT_CREATION)
            dashboard_dao.update_dashboard(transaction, update_contact=True)
        return contact_model

    @staticmethod
    def get_contact(email: str) -> ContactEntity:
        contact: ContactEntity = ContactEntity()
        return BaseDao.get(contact, contact.get_pk(email), contact.get_sk(email))

    @staticmethod
    def exists(email: str) -> bool:
        return ContactDao.get_contact(email).email == email

