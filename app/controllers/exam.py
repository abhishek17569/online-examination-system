from flask import request
from flask_restx import Namespace, marshal, abort
from flask_restx import Resource

import app.models.exam as em
from app.schema.exam import Exam
from app.security.authenticate import authenticate_user

api = Namespace("exams", description="Exams API")

exam_model = em.exam_model()
exam_id_model = em.exam_id_model()
exam_list_model = em.exam_list_model()
fetch_exam_model = em.fetch_exam_model()
exam_update_model = em.exam_update_model()


@api.route('/')
class ExamResource(Resource):
    @api.expect(exam_model)
    @api.response(201, "Exam successfully created!", exam_id_model)
    @authenticate_user
    def post(self):
        try:
            data = request.json
            exam = Exam(**data)
            exam.save()
        except Exception as err:
            return abort(400, f"{err}")

        return marshal({"id": exam.id}, exam_id_model), 201

    @api.response(200, "Exams successfully fetched!")
    @authenticate_user
    def get(self):
        try:
            exams = Exam.objects()
            return marshal({"exams": list(exams)}, exam_list_model), 200
        except Exception as err:
            return abort(400, f"{err}")


@api.route('/<exam_id>')
class ExamDetailResource(Resource):
    @api.response(200, "Exam successfully fetched", exam_model)
    @api.response(404, "Exam not found!")
    @authenticate_user
    def get(self, exam_id):
        try:
            exam = Exam.objects(id=exam_id).first()
            if not exam:
                return abort(404, "Exam not found!")
        except Exception as err:
            return abort(400, str(err))
        else:
            return marshal(exam, fetch_exam_model), 200

    @api.response(404, "Exam not found!")
    @api.expect(exam_update_model)
    @authenticate_user
    def patch(self, exam_id):
        try:
            data = request.json
            exam = Exam.objects(id=exam_id).first()
            if not exam:
                return abort(404, "Exam not found!")

            exam.update(**data)
        except Exception as err:
            return abort(400, str(err))
        else:
            return marshal({}, {}), 204
