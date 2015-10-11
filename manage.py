#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Location
from flask.ext.script import Manager, Shell

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
app.jinja_env.cache = {}

def make_shell_context():
    return dict(app=app, db=db, Location=Location)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()