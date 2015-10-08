from app import db

class Location(db.Document):
    location_name = db.StringField()
    address = db.StringField()
    latitude = db.FloatField(max_value=90, min_value=-90)
    longitude = db.FloatField(max_value=180, min_value=-180)

    water = db.StringField()
    food = db.StringField()
    supplies = db.StringField()
    shelter = db.StringField()

    resources = db.StringField()