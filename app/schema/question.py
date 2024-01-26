import mongoengine


class Question(mongoengine.Document):
    question_statement = mongoengine.StringField(required=True)
    options = mongoengine.ListField(mongoengine.StringField(), required=True)
    correct_answer = mongoengine.StringField(required=True)
