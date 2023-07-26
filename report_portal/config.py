import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# os.environ["WERKZEUG_RUN_MAIN"] = "true"
load_dotenv()

support = []
for r in  os.getenv('SUPPORT').split(','):
    support.append(str(r))

recipients = []
for r in  os.getenv('ADMINS').split(','):
    recipients.append(str(r))

dc_terminals = []
for r in  os.getenv('DC_TERMINALS').split(','):
    dc_terminals.append(int(r))

BASE_URL = 'http://localhost:5000'
if os.environ.get("DEBUG_ENV") == "dev":
    DEBUG = True
    BASE_URL = 'http://localhost/reportportalserver'
else:
    DEBUG = False
    BASE_URL = 'http://localhost/reportportalserver'

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = 'http://localhost/reportportalserver'
    MAIL_SERVER = 'cdldelivers-com.mail.protection.outlook.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASS")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    EMAIL = os.getenv("EMAIL")
    RECIPIENTS = recipients
    SUPPORT = support
    DC_TERMINALS = dc_terminals
    CORS_METHOD = ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
    CORS_HEADERS = ["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin"]
    CORS_SUPPORT_CREDENTIALS = True 
    CORS_ORIGINS = ["*"]
    SECRET_KEY = "xc8xa9xe3xccx84qxc5xddTWxe9xf4xa6Dxaexcfxed7xe1x9bx10xfb"
    
    
   

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    DEBUG = False
    


class ProductionConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
    DEBUG = False
   


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

config = config[os.getenv('FLASK_ENV')]