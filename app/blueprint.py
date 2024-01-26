from flask import Blueprint
from flask_restx import Api

from app.controllers.question import api as question_ns
from app.controllers.exam import api as exam_ns
from app.controllers.submission import api as submission_ns
from app.controllers.result import api as result_ns


v1_blueprint = Blueprint("v1_blueprint", __name__, url_prefix="/api/v1")

api = Api(
    v1_blueprint,
    version="1.0",
    title="Examination REST APIs",
    contact_email="abhishek17569@gmail.com",
)

api.namespaces = []
api.add_namespace(question_ns, path="/questions")
api.add_namespace(exam_ns, path="/exams")
api.add_namespace(submission_ns, path="/submissions")
api.add_namespace(result_ns, path="/results")
