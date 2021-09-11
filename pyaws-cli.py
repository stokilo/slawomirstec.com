import os
import sys
import traceback
import subprocess
import secrets
import json
from enum import Enum
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog
from ruamel.yaml import YAML
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d


class Action(Enum):
    DEPLOY = "deploy"
    UNDEPLOY = "undeploy"
    TEST = "test"
    DB_MIGRATE = "dbmigrate"
    KV_MIGRATE = "kvmigrate"

class Stage(Enum):
    DEV = "dev"
    PROD = "prod"

def _derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=100_000, backend=default_backend())
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt)
    iterations = 100_000
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    key = _derive_key(password.encode(), salt)
    return Fernet(key).decrypt(token)


def load_config() -> dict:
    """
    Import settings from YAML config
    """
    config_path = ".secret.config.yaml"
    if not config_path:
        raise RuntimeError("You need to copy .secret.config.yaml from template and configure credentials")
    with open(config_path) as config_file:
        config = YAML().load(config_file.read())
    return config


def load_release_version() -> dict:
    """Read release version
    """
    release_version = "release-version.json"
    with open(release_version) as release_version:
        file = json.load(release_version)
    return file


def action(stage: Stage, action: Action):
    """
    Deploy or undeploy application on system identified by stage (dev or prod)
    Undeploy is not allowed on prod
    """
    if action == Action.UNDEPLOY and stage == Stage.PROD:
        print("Undeploy is not allowed on production")
        exit(0)

    if action == Action.TEST and stage == Stage.PROD:
        print("Running tests against production is not allowed")
        exit(0)


    master_password = show_input("Master password", "Please enter master password")

    config = load_config()
    try:
       aws_access_key_id = password_decrypt(config['environments'][stage.value]
                           ['encrypted_aws_access_key_id'], master_password)
       aws_secret_access_key = password_decrypt(config['environments'][stage.value]
                               ['encrypted_aws_secret_access_key'], master_password)

       admin_secret_key = password_decrypt(config['environments'][stage.value]['admin-secret-key'], master_password)
       admin_ip = password_decrypt(config['environments'][stage.value]['admin-ip'], master_password)

       recaptcha = password_decrypt(config['environments'][stage.value]['recaptcha'], master_password)
       aws_region = config['environments'][stage.value]['region']
       sns_email_region = config['environments'][stage.value]['sns-email-region']
       domain = config['environments'][stage.value]['domain']
       cf_zone_id = config['environments'][stage.value]['cf-zone-id']
       cf_account_id = password_decrypt(config['environments'][stage.value]['cf-account-id'], master_password)
       cf_api_token = password_decrypt(config['environments'][stage.value]['cf-api-token'], master_password)
       kv_autocomplete_namespace_id = config['environments'][stage.value]['kv-autocomplete-namespace-id']
       kv_cache_namespace_id = config['environments'][stage.value]['kv-cache-namespace-id']
       subprocess.call(['bash', './pyaws-cli.sh'], env=dict(os.environ,
          PYAWS_CLI_ENV_ALLOW_EXECUTE_SHELL_SCRIPT="true",
          PYAWS_CLI_ENV_ACTION=action.value,
          PYAWS_CLI_AWS_STAGE=stage.value,
          PYAWS_CLI_AWS_ACCESS_KEY_ID=aws_access_key_id,
          PYAWS_CLI_AWS_SECRET_ACCESS_KEY=aws_secret_access_key,
          PYAWS_ADMIN_SECRET_KEY=admin_secret_key,
          PYAWS_ADMIN_IP=admin_ip,
          PYAWS_CLI_RECAPTCHA=recaptcha,
          PYAWS_CLI_AWS_REGION=aws_region,
          PYAWS_CLI_AWS_SNS_EMAIL_REGION=sns_email_region,
          PYAWS_CLI_DOMAIN=domain,
          PYAWS_CLI_IMAGE_SUBDOMAIN="img",
          PYAWS_CLI_CF_ZONE_ID=cf_zone_id,
          PYAWS_CLI_CF_ACCOUNT_ID=cf_account_id,
          PYAWS_CLI_CF_API_TOKEN=cf_api_token,
          PYAWS_CLI_KV_AUTOCOMPLETE_NAMESPACE_ID=kv_autocomplete_namespace_id,
          PYAWS_CLI_KV_CACHE_NAMESPACE_ID=kv_cache_namespace_id
       ))
    except Exception as e:
        print("Please check your master password, decrypt or deploy/undeploy operation failed")
        print(e)
        print(traceback.format_exc())
        exit(0)


def start_app():

    """
    Run pyaws command line app
    """
    main_command = select_main_command()

    if main_command == "deploy-prod":
        check_prod_settings_filled()

    if main_command == "deploy-dev":
        action(Stage.DEV, Action.DEPLOY)

    if main_command == "undeploy-dev":
        action(Stage.DEV, Action.UNDEPLOY)

    if main_command == "db-migrate-dev":
        action(Stage.DEV, Action.DB_MIGRATE)

    if main_command == "kv-migrate-dev":
        action(Stage.DEV, Action.KV_MIGRATE)

    if main_command == "set-credentials-dev":
        set_credentials(Stage.DEV)

    if main_command == "set-recaptcha-dev":
        set_recaptcha(Stage.DEV)

    if main_command == "test":
        action(Stage.DEV, Action.TEST)

    if main_command == "admin-secret-and-ip":
        set_admin_key_ip(Stage.DEV)

    if main_command == "cf-worker-secrets-dev":
        set_cf_worker_secrets(Stage.DEV)

    # PROD

    if main_command == "deploy-prod":
        retype_production_sentence()
        action(Stage.PROD, Action.DEPLOY)

    if main_command == "db-migrate-prod":
       action(Stage.PROD, Action.DB_MIGRATE)

    if main_command == "kv-migrate-prod":
        action(Stage.PROD, Action.KV_MIGRATE)

    if main_command == "set-credentials-prod":
        set_credentials(Stage.PROD)

    if main_command == "set-recaptcha-prod":
        set_recaptcha(Stage.PROD)

    if main_command == "set-retype-prod":
        set_prod_deploy_retype_confirmation()

    if main_command == "admin-secret-and-ip-prod":
        set_admin_key_ip(Stage.PROD)

    if main_command == "cf-worker-secrets-prod":
        set_cf_worker_secrets(Stage.PROD)


def select_main_command() -> str:
    """
    Select main action
    :return: action id
    """
    return radiolist_dialog(
        title="PYAWS CLI",
        text="Select action to perform",
        values=[
            ("DEV", "------------------------- DEV SYSTEM ---------------------------------"),
            ("deploy-dev", "deploy-dev             (deploy aws cdk and client to dev system) "),
            ("undeploy-dev", "undeploy-dev           (undeploy aws infrastructure from dev)"),
            ("db-migrate-dev", "db-migrate-dev         (run migration scripts on dev system)"),
            ("kv-migrate-dev", "kv-migrate-dev         (run kv migration on dev system)"),
            ("set-credentials-dev", "set-credentials-dev    (set encrypted credentials for dev account)"),
            ("set-recaptcha-dev", "set-recaptcha-dev      (set encrypted recaptcha for dev account)"),
            ("admin-secret-and-ip", "admin-secret-and-ip    (set admin secret key and ip)"),
            ("cf-worker-secrets-dev", "cf-worker-secrets-dev  (set cf account id and api token for worker deployment"),
            ("test", "test                   (run tests against DEV environment, dev must be deployed before running this command)"),
            ("PROD", "------------------------- PROD SYSTEM --------------------------------"),
            ("deploy-prod", "deploy-prod            (deploy aws cdk and client to prod system)"),
            ("db-migrate-prod", "db-migrate-prod        (run migration scripts on prod system)"),
            ("kv-migrate-prod", "kv-migrate-prod        (run kv migration on prod system)"),
            ("set-credentials-prod", "set-credentials-prod   (set encrypted credentials for prod account)"),
            ("set-recaptcha-prod", "set-recaptcha-prod     (set encrypted recaptcha for prod account)"),
            ("admin-secret-and-ip-prod", "admin-secret-and-ip    (set admin secret key and ip)"),
            ("cf-worker-secrets-prod", "cf-worker-secrets-prod (set cf account id and api token for worker deployment"),
            ("set-retype-prod", "set-retype-prod        (set sentence that must be typed in before any prod deployment)"),
        ]
    ).run()


def show_input(title: str, text: str) -> str:
    """
    Show input and capture text entered on it
    :param title:
    :param text:
    :return:
    """
    return input_dialog(title=title, text=text).run()


def check_prod_settings_filled():
    config = load_config()
    prod_settings = config['environments'][Stage.PROD.value]
    for key in prod_settings:
        if not prod_settings[key]:
            raise Exception(f"Check settings, missing value for: {key}")


def set_credentials(stage: Stage):
    title = f"Enter set-credentials-{stage.value}"
    master_password = show_input(title, f"Enter master password for {stage.value} system credentials")
    aws_access_key_id = show_input(title, f"Enter [aws_access_key_id] for {stage.value}")
    aws_secret_access_key = show_input(title, f"Enter [aws_secret_access_key] for {stage.value}")
    encrypted_aws_access_key_id = password_encrypt(aws_access_key_id.encode(), master_password)
    encrypted_aws_secret_access_key = password_encrypt(aws_secret_access_key.encode(), master_password)

    config = load_config()
    config['environments'][stage.value]['encrypted_aws_access_key_id'] = encrypted_aws_access_key_id.decode()
    config['environments'][stage.value]['encrypted_aws_secret_access_key'] = encrypted_aws_secret_access_key.decode()

    config_path = ".secret.config.yaml"
    with open(config_path, "w") as config_file:
        YAML().dump(config, config_file)


def set_recaptcha(stage: Stage):
    title = f"Enter recaptcha secret key for {stage.value}"
    master_password = show_input(title, f"Enter master password for {stage.value} recaptcha")
    recaptcha = show_input(title, f"Enter [google recaptcha secret key] for {stage.value}")
    encrypted_recaptcha = password_encrypt(recaptcha.encode(), master_password)

    config = load_config()
    config['environments'][stage.value]['recaptcha'] = encrypted_recaptcha.decode()

    config_path = ".secret.config.yaml"
    with open(config_path, "w") as config_file:
        YAML().dump(config, config_file)


def set_admin_key_ip(stage: Stage):
    title = f"Enter admin key and ip-{stage.value}"
    master_password = show_input(title, f"Enter master password for {stage.value} admin key and ip")
    admin_secret_key = show_input(title, f"Enter [admin_secret_key] for {stage.value}")
    admin_ip = show_input(title, f"Enter [admin_ip] for {stage.value}")
    encrypted_admin_secret_key = password_encrypt(admin_secret_key.encode(), master_password)
    encrypted_admin_ip = password_encrypt(admin_ip.encode(), master_password)

    config = load_config()
    config['environments'][stage.value]['admin-secret-key'] = encrypted_admin_secret_key.decode()
    config['environments'][stage.value]['admin-ip'] = encrypted_admin_ip.decode()

    config_path = ".secret.config.yaml"
    with open(config_path, "w") as config_file:
        YAML().dump(config, config_file)


def set_cf_worker_secrets(stage: Stage):
    title = f"Enter admin key and ip-{stage.value}"
    master_password = show_input(title, f"Enter master password for {stage.value} cf account id and api toke")
    cf_account_id = show_input(title, f"Enter [cf-account-id] for {stage.value}")
    cf_api_token = show_input(title, f"Enter [cf-api-token] for {stage.value}")
    encrypted_cf_account_id = password_encrypt(cf_account_id.encode(), master_password)
    encrypted_cf_api_token = password_encrypt(cf_api_token.encode(), master_password)

    config = load_config()
    config['environments'][stage.value]['cf-account-id'] = encrypted_cf_account_id.decode()
    config['environments'][stage.value]['cf-api-token'] = encrypted_cf_api_token.decode()

    config_path = ".secret.config.yaml"
    with open(config_path, "w") as config_file:
        YAML().dump(config, config_file)


def set_prod_deploy_retype_confirmation():
    """
    Extra security before deploying change into PROD, set sentence that must be retyped each time user attempty to
    change PROD
    """
    sentence = show_input("Production deployment security",
                          "Enter sentence that must be retyped before any production deployment")

    config = load_config()
    config['production_deployment_confirm_sentence'] = sentence

    config_path = ".secret.config.yaml"
    with open(config_path, "w") as config_file:
        YAML().dump(config, config_file)


def retype_production_sentence():
    """
    Force user to retype sentence from .secret.config.yaml before any production deployment.
    """
    sentence = show_input("!!! WARNING !!! WARNING !!! WARNING !!!",
                          "This is PRODUCTION deployment, please retype security sentence to confirm the change")
    config = load_config()
    expected = config["production_deployment_confirm_sentence"]

    if expected is None or len(expected) <= 0 or len(sentence) <= 0:
       print("Production deployment confirmation sentence cannot be empty, skipping.")
       sys.exit()

    if sentence != expected:
       print("Entered sentence is not matching value from .secret.config.yaml, skipping deployment.")
       sys.exit()


if __name__ == '__main__':
    start_app()

