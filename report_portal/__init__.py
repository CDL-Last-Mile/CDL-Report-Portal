from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from report_portal.config import config
from werkzeug.middleware.dispatcher import DispatcherMiddleware

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/reportportalserver": app
    })


    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    CORS(app, resources={r"/*": {"origins": "*"}})

    from report_portal.errors.handlers import errors
    from report_portal.main.routes import main
    from report_portal.summary_report.routes import summary
    from report_portal.detailed_report.routes import detailed
    from report_portal.report.routes import report
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(summary)
    app.register_blueprint(detailed)
    app.register_blueprint(report)

    return app