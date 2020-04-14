import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import timedelta

#CONFIG

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'harms khan benke'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CHOCSHOP_MAIL_SUBJECT_PREFIX = '[CHOCSHOP]'
    CHOCSHOP_MAIL_SENDER = 'chocshop admin <chocshop.fmb@gmail.com>'
    CHOCSHOP_ADMIN = os.environ.get('CHOCSHOP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHOCSHOP_PURCHASES_PER_PAGE = 20
    CHOCSHOP_USERS_PER_PAGE = 20
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}