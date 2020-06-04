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
    CHOCSHOP_PURCHASES_PER_PAGE = 30
    CHOCSHOP_USERS_PER_PAGE = 30
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    SSL_REDIRECT = False
    
    SQLALCHEMY_ECHO = True
    
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
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.CHOCSHOP_MAIL_SENDER,
            toaddrs=[cls.CHOCSHOP_ADMIN],
            subject=cls.CHOCSHOP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    
    'default': DevelopmentConfig
}