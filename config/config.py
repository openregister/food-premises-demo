# -*- coding: utf-8 -*-
import os

class Config(object):
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PREMISES_REGISTER = os.environ.get('PREMISES_REGISTER')
    POAO_PREMISES_REGISTER = os.environ.get('POAO_PREMISES_REGISTER')
    ADDRESS_REGISTER = os.environ.get('ADDRESS_REGISTER')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-not-secret')

class TestConfig(Config):
    TESTING = True
