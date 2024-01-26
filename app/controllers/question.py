from flask import request
from flask_restx import Namespace, marshal, abort
from flask_restx import Resource

import app.models.question as qm
from app.schema.question import Question
from app.security.authenticate import authenticate_user

api = Namespace("questions", description="Questions API")

question_model = qm.question_model()
question_id_model = qm.question_id_model()
question_list_model = qm.question_list_model()
extended_question_model = qm.extended_question_model()


@api.route('/')
class QuestionResource(Resource):
    @api.expect(question_model)
    @api.response(201, "Question successfully added!", question_id_model)
    @authenticate_user
    def post(self):
        try:
            data = request.json
            question = Question(**data)
            question.save()
        except Exception as err:
            return abort(400, f"{err}")

        return marshal({"id": question.id}, question_id_model), 201

    @api.response(200, "Questions successfully fetched!")
    @authenticate_user
    def get(self):
        try:
            questions = Question.objects()
            return marshal({"questions": list(questions)}, question_list_model), 200
        except Exception as err:
            return abort(400, f"{err}")


@api.route('/<question_id>')
class QuestionDetailResource(Resource):
    @api.response(200, "Question successfully fetched", question_model)
    @api.response(404, "Question not found!")
    @authenticate_user
    def get(self, question_id):
        try:
            question = Question.objects(id=question_id).first()
            if not question:
                return abort(404, "Question not found!")
        except Exception as err:
            return abort(400, str(err))
        else:
            return marshal(question, extended_question_model), 200

    @api.response(404, "Question not found!")
    @api.expect(question_model)
    @authenticate_user
    def patch(self, question_id):
        try:
            data = request.json
            question = Question.objects(id=question_id).first()
            if not question:
                return abort(404, "Question not found!")

            question.update(**data)
        except Exception as err:
            return abort(400, str(err))
        else:
            return marshal({}, {}), 204
