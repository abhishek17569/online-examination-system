from flask_restx import fields


def results_model():
    from app.controllers.exam import api

    result = api.model(
        "result",
        {
            "title": fields.String(title="Exam title", example="Math Quiz", attribute="exam_id.title"),
            "score": fields.Integer(title="Score", example=99),
        }
    )

    return api.model(
        "results_model",
        {
            "results": fields.List(fields.Nested(result)),
        }
    )
