from chalice import Rate
from chalicelib.routes.auth import auth_routes
from chalicelib.routes.authorizer import authorizer_blueprint
from chalicelib.routes.contact import contact_routes
from chalicelib.routes.crud import crud_routes
from chalicelib.routes.todo import todo_routes
from chalicelib.routes.dashboard import dashboard_routes
from chalicelib.routes.upload import upload_route
from chalicelib.routes.appointment import appointment_routes
from chalice import CORSConfig
from chalicelib import logger
from chalicelib.services.env import get_dynamodb_stream_arn, is_chalice_debug_enabled
from chalicelib.services.monitoring.email_monitoring import on_table_update_handler
from chalicelib.services.monitoring.lambda_monitoring import lambda_invocation_count_monitoring
from chalicelib import app


#enable both lines to debug the app on docker env, disable that after debugging, pydevd is dev dependency!
if is_chalice_debug_enabled():
    logger.info("Chalice python logger plugin enabled.")
    import pydevd_pycharm
    pydevd_pycharm.settrace('host.docker.internal', port=8090, stdoutToServer=True, stderrToServer=True)

app.api.cors = CORSConfig(
    allow_origin='http://localhost:3000',
    allow_headers=['X-Language']
)
app.experimental_feature_flags.update([
    'BLUEPRINTS'
])
app.register_blueprint(auth_routes)
app.register_blueprint(authorizer_blueprint)
app.register_blueprint(contact_routes)
app.register_blueprint(todo_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(upload_route)
app.register_blueprint(appointment_routes)
app.register_blueprint(crud_routes)


@app.schedule(Rate(1, unit=Rate.HOURS))
def periodic_task(event):
    lambda_invocation_count_monitoring(max_sms_allowed_to_be_send=30,
                                       sms_nr="+990000")
    return {}


@app.on_dynamodb_record(stream_arn=get_dynamodb_stream_arn(), batch_size=50)
def on_table_update(event):
    on_table_update_handler(event)
