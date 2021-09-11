from typing import List

import boto3
import requests

from botocore.session import Session

from chalicelib.model.appointment import AppointmentModel

session = boto3.session.Session()

def kv_put(appointment_id: str, appointments: List[AppointmentModel]) -> bool:
    region_name = Session().get_config_variable('region')
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )
    account_id = client.get_secret_value(
        SecretId='PYAWS_CLI_CF_ACCOUNT_ID'
    )["SecretString"]

    namespace_id = client.get_secret_value(
        SecretId='PYAWS_CLI_KV_CACHE_NAMESPACE_ID'
    )["SecretString"]

    api_token = client.get_secret_value(
        SecretId='PYAWS_CLI_CF_API_TOKEN'
    )["SecretString"]

    kv_key = f"__APPOINTMENT__{appointment_id}"
    print(f"kv_key {kv_key}")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{kv_key}?expiration_ttl=99999999"

    headers = {
        'Content-Type' : 'text/plain',
        'Authorization' : f"Bearer {api_token}"
    }

    cache_data = AppointmentModel.schema().dumps(appointments, many=True)
    r = requests.put(url, data = f"{cache_data}", headers=headers, timeout=4)
    return r.status_code == 200