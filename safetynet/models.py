from peewee import Model, CharField, FloatField, TextField, ForeignKeyField

from .database import db


class Profile(Model):
    name = CharField()
    latitude = FloatField()
    longitude = FloatField()
    status = TextField()

    class Meta:
        database = db

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": {"latitude": self.latitude, "longitude": self.longitude},
            "status": self.status,
        }

    def token(self):
        pt = ProfileToken.get(ProfileToken.profile == self)
        return str(pt.token)


class ProfileToken(Model):
    profile = ForeignKeyField(Profile)
    token = CharField()

    class Meta:
        database = db


db.create_tables([Profile, ProfileToken])
