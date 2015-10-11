from collections import OrderedDict

from flask import Flask, render_template, redirect, url_for, flash
from flask.ext.wtf import Form
from flask.ext.googlemaps import GoogleMaps, Map
from flask.ext.mongoalchemy import MongoAlchemy
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired
import googlemaps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shh! It\'s a secret!'
app.config['MONGOALCHEMY_DATABASE'] = 'locations'
GoogleMaps(app)
GoogleMapsAPI = googlemaps.Client(key='AIzaSyC_tuWoozjFgmRbSvwj6raddk_UFA4Fx_c')
db = MongoAlchemy(app)


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=['GET', 'POST'])
def map():
    form = FilterMapForm()
    blue_icon_url = 'https://lh4.ggpht.com/FRLzoxHDpRHxP6aFWxxQ1OUPlWnc55ZqnO7EpLtD8FBn6EK1zBerpF9P3BE3jJ6SFLNF7P0=w9-h9'
    green_icon_url = 'https://lh6.ggpht.com/GO-A_KjZDF9yJeeER2fajzO4MgqML-q2rccm27ynBlD6R-xOR3pJOb42WKfE0MNFtRsKwK4=w9-h9'
    red_icon_url = 'https://lh3.ggpht.com/hx6IeSRualApBd7KZB9s2N7bcHZIjtgr9VEuOxHzpd05_CZ6RxZwehpXCRN-1ps3HuL0g8Wi=w9-h9'
    yellow_icon_url = 'https://lh3.ggpht.com/XAjhu-6znztoLTr9AxuwM5v0wilaKiUJJMLKEiiFMn6lGOmBmY1Km7Kt1ohildzlIdWgkwy_5g=w9-h9'
    map_points = {}
    map_data = {}
    if form.validate_on_submit():
        print 'VALIDATED'
        for field in form:
            map_points[field.id] = []
            map_data[field.id] = []
            if field.data == True and field.type not in ['CSRFTokenField', 'HiddenField']:
                response = Location.query.filter(getattr(Location, field.id) == 'True').all()
                map_points[field.id] = [(document.latitude, document.longitude) for document in response]
                map_data[field.id] = [
                    '<b>' + document.location_name + '</b><br>' + document.address + '<br>' + document.resources for
                    document in response]
    else:
        for field in form:
            map_points[field.id] = []
            map_data[field.id] = []
            if field.type not in ['CSRFTokenField', 'HiddenField']:
                response = Location.query.filter(getattr(Location, field.id) == 'True').all()
                map_points[field.id] = [(document.latitude, document.longitude) for document in response]
                map_data[field.id] = [
                    '<b>' + document.location_name + '</b><br>' + document.address + '<br>' + document.resources for
                    document in response]
    generated_map = Map(
        'map',
        '34.0386',
        '-80.9675',
        zoom='13',
        style='height:100%;width:100%;',
        infobox=list(
            OrderedDict.fromkeys(map_data['water'] + map_data['food'] + map_data['supplies'] + map_data['shelter'])),
        markers={
            red_icon_url: list(OrderedDict.fromkeys(
                map_points['water'] + map_points['food'] + map_points['supplies'] + map_points['shelter']))
        }
    )
    return render_template('map.html', form=form, map=generated_map)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddDataForm()
    if form.validate_on_submit():
        response = GoogleMapsAPI.geocode(form.address.data)
        latitude = response[0]['geometry']['location']['lat']
        longitude = response[0]['geometry']['location']['lng']
        resource_list = []
        for field in [form.water, form.food, form.supplies, form.shelter]:
            if field.data == True:
                resource_list.append(field.id.title())
        print resource_list
        loc = Location(location_name=form.location_name.data,
                       address=form.address.data,
                       latitude=latitude,
                       longitude=longitude,
                       water=str(form.water.data),
                       food=str(form.food.data),
                       supplies=str(form.supplies.data),
                       shelter=str(form.shelter.data),
                       resources=', '.join(resource_list)
                       )
        loc.save()
        flash("Thank You. Your location has been added.")
        return redirect(url_for('map'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
