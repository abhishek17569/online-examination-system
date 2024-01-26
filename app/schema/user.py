import mongoengine


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    role = mongoengine.StringField(choices=["student", "admin"])



