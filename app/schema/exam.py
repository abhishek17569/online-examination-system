import mongoengine
from bson import ObjectId, DBRef
from flask_restx import ValidationError
from mongoengine import Document

from app.schema.question import Question
from app.utils.date_utils import get_datetime_object_from_string


def verify_questions(questions: list):
    for question in questions:
        if type(question) == DBRef or type(question) == Question:
            q_id = question.id
        elif type(question) == str or type(question) == ObjectId:
            q_id = question
        else:
            raise ValidationError(f"Invalid question type!")

        ques = Question.objects(id=q_id).only("id").first()

        if not ques:
            raise ValidationError(f"Invalid question {question} present in the list")


class Exam(Document):
    title = mongoengine.StringField(required=True)
    questions = mongoengine.ListField(mongoengine.ReferenceField(Question), default=[], validation=verify_questions)
    start_time = mongoengine.DateTimeField(required=True)
    end_time = mongoengine.DateTimeField(required=True)

    def get_updated_questions(self, questions: dict):
        add_questions = questions.get("add", [])
        remove_questions = questions.get("remove", [])

        if not add_questions and not remove_questions:
            return

        existing_questions = set([question.id for question in self.questions])

        for question in add_questions:
            existing_questions.add(ObjectId(question))

        return list(existing_questions - set([ObjectId(question) for question in remove_questions]))

    def update(self, **kwargs):
        if "questions" in kwargs:
            kwargs["questions"] = self.get_updated_questions(kwargs["questions"])

        if "start_time" in kwargs:
            kwargs["start_time"] = get_datetime_object_from_string(kwargs["start_time"])

        if "end_time" in kwargs:
            kwargs["end_time"] = get_datetime_object_from_string(kwargs["end_time"])

        super().update(**kwargs)

    def save(
            self,
            force_insert=False,
            validate=True,
            clean=True,
            write_concern=None,
            cascade=None,
            cascade_kwargs=None,
            _refs=None,
            save_condition=None,
            signal_kwargs=None,
            **kwargs,
    ):
        self.questions = list(set(self.questions))
        self.start_time = get_datetime_object_from_string(self.start_time)
        self.end_time = get_datetime_object_from_string(self.end_time)

        super().save(
            force_insert,
            validate,
            clean,
            write_concern,
            cascade,
            cascade_kwargs,
            _refs,
            save_condition,
            signal_kwargs,
            **kwargs
        )
