from chalicelib.routes.constants import *
from .lib.helpers import *


class TestContactCreate(object):

    @staticmethod
    def test_create_contact(gateway_factory):
        gateway = gateway_factory()
        payload_string = json.dumps({})
        response = post(gateway, ROUTE_CONTACT, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json["status"]["success"] == False
        assert len(body_as_json['formValidation']['errors']) == 3
        assert body_as_json['formValidation']['errors']['name'][0] == 'Field is required'
        assert body_as_json['formValidation']['errors']['email'][0] == 'Field is required'
        assert body_as_json['formValidation']['errors']['email'][1] == 'Email is not valid'
        assert body_as_json['formValidation']['errors']['details'][0] == 'Field is required'

        payload_string = json.dumps({"name": "a", "email": "b", "details": "c"})
        response = post(gateway, ROUTE_CONTACT, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert len(body_as_json['formValidation']['errors']) == 3
        assert body_as_json['formValidation']['errors']['name'][0] == 'Min length is 5, max 250, provided 1'
        assert body_as_json['formValidation']['errors']['email'][0] == 'Min length is 3, max 250, provided 1'
        assert body_as_json['formValidation']['errors']['email'][1] == 'Email is not valid'
        assert body_as_json['formValidation']['errors']['details'][0] == 'Min length is 5, max 250, provided 1'

        email = generate_email()
        payload_string = json.dumps({"name": "John Doe", "email": email, "details": "Hello there"})
        response = post(gateway, ROUTE_CONTACT, payload_string)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['formValidation']['passed'] == True
        assert len(body_as_json['formValidation']['errors']) == 0
        assert body_as_json['status']['success'] == True

        payload_string = json.dumps({"name": "John Doe", "email": email, "details": "Hello there"})
        response = post(gateway, ROUTE_CONTACT, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json['status']['success'] == False
        assert body_as_json['status']['error_code'] == 'form-processing-error'
        assert body_as_json['status']['error_message'] == 'Contact already exists'
