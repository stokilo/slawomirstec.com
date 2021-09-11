"""Shared constants on controller level

Constants with ROUTE_PATH prefix define controller URL path
"""

"""
##################################
############# UNAUTHENTICATED ####
##################################
"""
ROUTE_PATH_AUTH = "/auth"
ROUTE_PATH_AUTH_SIGNUP = f"{ROUTE_PATH_AUTH}/signup"
ROUTE_PATH_AUTH_LOGIN = f"{ROUTE_PATH_AUTH}/login"
ROUTE_PATH_REFRESH_TOKEN = f"{ROUTE_PATH_AUTH}/refresh"
ROUTE_CONTACT = "/contact"

"""
##################################
############# AUTHENTICATED ######
##################################
"""
ROUTE_TODO= "/todo"
ROUTE_TODO_BATCH = f"{ROUTE_TODO}/batch"
ROUTE_DASHBOARD = "/dashboard"
ROUTE_UPLOAD = "/upload"
ROUTE_PROFILE = f"{ROUTE_PATH_AUTH}/profile"
ROUTE_APPOINTMENT = "/appointment"
ROUTE_CRUD = "/crud"
"""
##################################
############# SPECIAL CARE! ######
############# ALWAYS UPDATE! #####
##################################
"""

ROUTES_WITH_REQUIRED_AUTH_GET = [ROUTE_TODO, ROUTE_DASHBOARD, ROUTE_UPLOAD, ROUTE_APPOINTMENT, ROUTE_CRUD]
ROUTES_WITH_REQUIRED_AUTH_POST = [ROUTE_TODO, ROUTE_TODO_BATCH, ROUTE_PROFILE, ROUTE_APPOINTMENT, ROUTE_CRUD]

# duplicates not allowed, some resources handle both, GET and POST
ROUTES_WITH_REQUIRED_AUTH_ALL = list(dict.fromkeys(ROUTES_WITH_REQUIRED_AUTH_GET + ROUTES_WITH_REQUIRED_AUTH_POST))
