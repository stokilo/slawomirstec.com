from stacks.web_api import WebApi
from aws_cdk import core as cdk

class TestCdkStack(object):

    @staticmethod
    def test_chalice_stack():
        app= cdk.App()
        WebApi(app, 'WebApiDev')
