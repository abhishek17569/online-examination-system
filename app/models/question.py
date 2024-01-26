from flask_restx import Model, fields


def question_model() -> Model:
    from app.controllers.question import api

    return api.model(
        "question_model", {
            "question_statement": fields.String(title="Question statement", example="Who is the Prime Minister of India?"),
            "options": fields.List(fields.String(), example=["Narendra Modi", "APJ Abdul Kalam", "Rahul Gandhi"]),
            "correct_answer": fields.String(title="Correct answer", example="Narendra Modi")
        }
    )


def question_id_model() -> Model:
    from app.controllers.question import api

    return api.model(
        "question_id_model", {
            "id": fields.String(title="Id", example="65a5728b663d5c7050b6295a")
        }
    )


def extended_question_model() -> Model:
    extended_model = question_model()
    extended_model["id"] = fields.String(title="Id", example="65a5728b663d5c7050b6295a")

    return extended_model


def question_list_model() -> Model:
    from app.controllers.question import api

    return api.model(
        "question_list_model", {
            "questions": fields.List(fields.Nested(extended_question_model()))
        }
    )
