from flask_restx import Model, fields
from app.models.common_model_fields import id, tz_datetime
from app.models.question import extended_question_model


def exam_model() -> Model:
    from app.controllers.exam import api

    return api.model(
        "exam_model", {
            "title": fields.String(title="Exam title", example="Math Quiz"),
            "questions": fields.List(id),
            "start_time": tz_datetime,
            "end_time": tz_datetime
        }
    )


def exam_id_model() -> Model:
    from app.controllers.exam import api

    return api.model(
        "exam_id_model", {
            "id": fields.String(title="Exam ID", example="65a5728b663d5c7050b6295a")
        }
    )


def fetch_exam_model() -> Model:
    from app.controllers.exam import api

    question = extended_question_model()
    question.pop("correct_answer")

    return api.model(
        "exam_model", {
            "title": fields.String(title="Exam title", example="Math Quiz"),
            "questions": fields.List(fields.Nested(question)),
            "start_time": tz_datetime,
            "end_time": tz_datetime
        }
    )


def exam_list_model() -> Model:
    from app.controllers.exam import api

    exam = api.model(
        "exam", {
            "title": fields.String(title="Exam title", example="Math Quiz"),
            "start_time": tz_datetime,
            "end_time": tz_datetime
        }
    )
    return api.model(
        "exam_list_model", {
            "exams": fields.List(fields.Nested(exam))
        }
    )


def exam_update_model() -> Model:
    from app.controllers.exam import api

    edit_questions = api.model(
        "edit_questions", {
            "add": fields.List(id),
            "remove": fields.List(id)
        }
    )

    return api.model(
        "exam_model", {
            "title": fields.String(title="Exam title", example="Math Quiz"),
            "questions": fields.Nested(edit_questions),
            "start_time": tz_datetime,
            "end_time": tz_datetime
        }
    )
