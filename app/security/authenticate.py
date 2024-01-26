from functools import wraps

from flask import request
from flask_restx import abort

from app.schema.user import User
from app.security.rbac import rbac_rules


def authenticate_user(f):
    @wraps(f)
    def _authenticate_user(*args, **kwargs):
        request_method = request.method
        request_url = str(request.url_rule)
        if request_method == "OPTIONS":
            return

        email = request.headers.get("email")
        password = request.headers.get("password")

        if email is None or password is None:
            return abort(401, "Missing auth headers!")

        user = User.objects(email=email).first()
        if not user:
            return abort(404, "User not found!")

        if user.password != password:
            return abort(404, "Invalid password!")

        if request_url not in rbac_rules:
            return abort(404, "Invalid route requested")

        if request_method not in rbac_rules[request_url]:
            return abort(404, "Invalid method for the URL!")

        if user.role not in rbac_rules[request_url][request_method]:
            return abort(403, "Insufficient access level!")

        return f(*args, **kwargs)

    return _authenticate_user
