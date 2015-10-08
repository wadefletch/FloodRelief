from flask.ext.wtf import Form
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired


class FilterMapForm(Form):
    water = BooleanField('Water')
    food = BooleanField('Prepared Food')
    supplies = BooleanField('Supplies')
    shelter = BooleanField('Shelter')


class AddDataForm(Form):
    location_name = StringField('Location Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    water = BooleanField('Water')
    food = BooleanField('Prepared Food')
    supplies = BooleanField('Supplies')
    shelter = BooleanField('Shelter')
