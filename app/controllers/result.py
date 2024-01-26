from flask import request
from flask_restx import Namespace, marshal, abort
from flask_restx import Resource

import app.models.result as rm
from app.schema.submission import Submission
from app.schema.user import User
from app.security.authenticate import authenticate_user

api = Namespace("result", description="Results API")


results_model = rm.results_model()


@api.route('/')
class Results(Resource):
    @api.response(200, "Past results successfully fetched!")
    @api.response(400, "Invalid input data!")
    @authenticate_user
    def get(self):
        try:
            student = User.objects(email=request.headers.get("email")).first()
            submissions = Submission.objects(student_id=student.id, status="ended")
        except Exception as err:
            return abort(400, f"{err}")

        return marshal({"results": list(submissions)}, results_model), 200