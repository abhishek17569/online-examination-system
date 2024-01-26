from datetime import datetime

from flask import request
from flask_restx import Namespace, marshal, abort
from flask_restx import Resource

import app.models.submission as sm
from app.schema.exam import Exam
from app.schema.user import User
from app.schema.submission import Submission
from app.security.authenticate import authenticate_user

api = Namespace("submission", description="Submission API")


submission_model = sm.answer_submission_model()
start_exam_model = sm.start_exam_model()
start_exam_success_model = sm.start_exam_success_model()
result_model = sm.result_model()


@api.route('/start-test')
class SubmissionResource(Resource):
    @api.expect(start_exam_model)
    @api.response(201, "Test successfully started!")
    @api.response(400, "Invalid input data!")
    @api.response(404, "Exam or Student not found!")
    @authenticate_user
    def post(self):
        data = request.json
        try:
            required_keys = ["student_id", "exam_id"]
            for key in required_keys:
                if key not in data:
                    return abort(400, f"Missing required {key} in payload!")

            exam = Exam.objects(id=data["exam_id"]).only("id", "start_time", "end_time").first()
            if not exam:
                return abort(404, "Exam with the specified id not found!")

            time_now = datetime.utcnow()
            if time_now < exam.start_time:
                return abort(400, "Test is yet to start!")
            elif time_now > exam.end_time:
                return abort(400, "Test is ended!")

            student = User.objects(id=data["student_id"]).first()
            if not student:
                return abort(404, "Student with the specified id not found!")

            on_going_tests = Submission.objects(id=student.id, status="started").only("id").first()
            if on_going_tests:
                return abort(400, "Student has an ongoing test!")

            submission = Submission(
                student_id=student.id,
                exam_id=exam.id
            )
            submission.save()
        except Exception as err:
            return abort(400, f"{err}")

        return marshal({"submission_id": submission.id}, start_exam_success_model), 201


@api.route('/<submission_id>/submit-answers')
class SubmissionEdit(Resource):
    @api.expect(submission_model)
    @api.response(200, "Test successfully started!")
    @api.response(400, "Invalid input data!")
    @api.response(404, "Exam or Student not found!")
    @authenticate_user
    def patch(self, submission_id):
        data = request.json
        try:
            student = User.objects(email=request.headers.get("email")).first()
            if not student:
                return abort(404, "Student with the specified id not found!")

            submission = Submission.objects(id=submission_id).first()
            if not submission:
                return abort(404, "Submission with the specified id not found!")

            if submission.student_id.id != student.id:
                return abort(403, "Forbidden to access submission")

            time_now = datetime.utcnow()
            if time_now > submission.exam_id.end_time:
                return abort(400, "Test is ended!")

            submission.update(**data)
        except Exception as err:
            return abort(400, f"{err}")

        return marshal({"result": submission.score}, result_model), 200
