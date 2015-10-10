from collections import OrderedDict

from flask import render_template, redirect, url_for, flash
from . import main
from .forms import FilterMapForm, AddDataForm
from ..models import Location
from flask.ext.googlemaps import Map
import googlemaps

GoogleMapsAPI = googlemaps.Client(key='AIzaSyC_tuWoozjFgmRbSvwj6raddk_UFA4Fx_c')

@main.route('/')
def index():
    return redirect(url_for('main.map'))


@main.route('/map', methods=['GET', 'POST'])
def map():
    form = FilterMapForm()
    blue_icon_url = 'https://lh4.ggpht.com/FRLzoxHDpRHxP6aFWxxQ1OUPlWnc55ZqnO7EpLtD8FBn6EK1zBerpF9P3BE3jJ6SFLNF7P0=w9-h9'
    green_icon_url = 'https://lh6.ggpht.com/GO-A_KjZDF9yJeeER2fajzO4MgqML-q2rccm27ynBlD6R-xOR3pJOb42WKfE0MNFtRsKwK4=w9-h9'
    red_icon_url = 'https://lh3.ggpht.com/hx6IeSRualApBd7KZB9s2N7bcHZIjtgr9VEuOxHzpd05_CZ6RxZwehpXCRN-1ps3HuL0g8Wi=w9-h9'
    yellow_icon_url = 'https://lh3.ggpht.com/XAjhu-6znztoLTr9AxuwM5v0wilaKiUJJMLKEiiFMn6lGOmBmY1Km7Kt1ohildzlIdWgkwy_5g=w9-h9'
    map_points = {}
    map_data = {}
    if form.validate_on_submit():
        response = Location.query.filter(str(form.water.data) == Location.water,
                                         str(form.food.data) == Location.food,
                                         str(form.supplies.data) == Location.supplies,
                                         str(form.shelter.data) == Location.shelter
                                        ).all()
        for field in form:
            map_points[field.id] = [(document.latitude, document.longitude) for document in response]
            map_data[field.id] = ['<b>' + document.location_name + '</b><br>' + document.address + '<br>' + document.resources for document in response]
    else:
        for field in form:
            map_points[field.id] = []
            map_data[field.id] = []
            if field.type not in ['CSRFTokenField', 'HiddenField']:
                response = Location.query.filter(getattr(Location, field.id) == 'True').all()
                map_points[field.id] = [(document.latitude, document.longitude) for document in response]
                map_data[field.id] = [
                    '<b>' + document.location_name + '</b><br>' + document.address + '<br>' + document.resources + ' - ' + document.hours for
                    document in response]
    generated_map = Map(
        'map',
        '34.0386',
        '-80.9675',
        zoom=13,
        style='height:100%;width:100%;',
        infobox=list(
            OrderedDict.fromkeys(map_data['water'] + map_data['food'] + map_data['supplies'] + map_data['shelter'])),
        markers={
            red_icon_url: list(OrderedDict.fromkeys(
                map_points['water'] + map_points['food'] + map_points['supplies'] + map_points['shelter']))
        }
    )
    return render_template('map.html', form=form, map=generated_map)


@main.route('/add', methods=['GET', 'POST'])
def add():
    form = AddDataForm()
    if form.validate_on_submit():
        response = GoogleMapsAPI.geocode(form.address.data)
        latitude = response[0]['geometry']['location']['lat']
        longitude = response[0]['geometry']['location']['lng']
        resource_list = []
        for field in [form.water, form.food, form.supplies, form.shelter]:
            if field.data:
                resource_list.append(field.id.title())
        loc = Location(location_name=form.location_name.data,
                       address=form.address.data,
                       latitude=latitude,
                       longitude=longitude,
                       water=str(form.water.data),
                       food=str(form.food.data),
                       supplies=str(form.supplies.data),
                       shelter=str(form.shelter.data),
                       resources=', '.join(resource_list),
                       hours=str(form.hours.data)
                       )
        loc.save()
        flash("Thank You. The location has been added. You may have to refresh the page.")
        return redirect(url_for('main.map'))
    return render_template('add.html', form=form)


@main.route('/feedback')
def feedback():
    return redirect('mailto:feedback@columbiafloodrelief.com?subject=Feedback')

@main.route('/water')
def water():
    return render_template('water.html')

@main.route('/donate')
def donate():
    return render_template('donate.html')