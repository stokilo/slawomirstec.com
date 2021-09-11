from aws_cdk import core as cdk
from stacks.web_api import WebApi

app = cdk.App()
WebApi(app, 'WebApiDev')
app.synth()
