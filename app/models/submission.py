from flask_restx import fields

from app.models.common_model_fields import id


def answer_submission_model():
    from app.controllers.submission import api

    answer_model = api.model(
        "answer_model",
        {
            "question_id": fields.String(title="Question ID", example="65a5728b663d5c7050b6295a"),
            "answer": fields.String(title="Answer", example="Narendra Modi"),
        }
    )

    return api.model(
        "submission_model",
        {
            "answers": fields.List(fields.Nested(answer_model)),
        }
    )


def start_exam_model():
    from app.controllers.submission import api

    return api.model(
        "start_exam_model",
        {
            "student_id": id,
            "exam_id": id,
        }
    )


def start_exam_success_model():
    from app.controllers.submission import api

    return api.model(
        "start_exam_success_model",
        {
            "submission_id": id,
        }
    )


def result_model():
    from app.controllers.submission import api

    return api.model(
        "result_model",
        {
            "result": fields.Integer(title="Result", example=99),
        }
    )
