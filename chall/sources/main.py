#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_security import Security, RegisterForm
from flask_session import Session

from .settings import init_settings
from .models.app_models import create_models, init_user_datastore
from .models.profile_model import init_profile_base
from .logging import init_logger

def launch_app(loglevel=0):
    app = Flask(__name__)
    security = Security()
    sess = Session()
    init_logger(loglevel)
    init_settings(app.config)
    create_models(app)
    base = init_user_datastore()
    init_profile_base(app)
    sess.init_app(app)
    security.init_app(app, base,\
                         register_form=RegisterForm)
    register_blueprints(app)
    return app

from .views import index
from .api import endpoints

def register_blueprints(app):
    app.register_blueprint(index)
    app.register_blueprint(endpoints)
