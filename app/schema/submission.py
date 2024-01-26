from datetime import datetime

import mongoengine

from app.schema.exam import Exam
from app.schema.question import Question
from app.schema.user import User


class Answer(mongoengine.EmbeddedDocument):
    question_id = mongoengine.ReferenceField(Question, required=True)
    answer = mongoengine.StringField()


class Submission(mongoengine.Document):
    student_id = mongoengine.ReferenceField(User, required=True)
    exam_id = mongoengine.ReferenceField(Exam, required=True)
    answers = mongoengine.EmbeddedDocumentListField(Answer, default=[])
    status = mongoengine.StringField(default="started", choices=["started", "ended"])
    score = mongoengine.IntField(default=0)
    start_time = mongoengine.DateTimeField(default=datetime.utcnow)
    submission_time = mongoengine.DateTimeField()

    def calculate_score(self, answers) -> int:
        exam_answers = {}
        score = 0
        for ques in self.exam_id.questions:
            exam_answers[str(ques.id)] = ques.correct_answer

        for answer in answers:
            try:
                if answer["answer"] == exam_answers[answer["question_id"]]:
                    score += 4
                else:
                    score -= 1
            except:
                continue

        return score

    def update(self, **kwargs):
        kwargs["status"] = "ended"
        kwargs["score"] = self.calculate_score(kwargs["answers"])
        kwargs["submission_time"] = datetime.utcnow()

        super().update(**kwargs)
