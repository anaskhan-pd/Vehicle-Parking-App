from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'heythereanaskhan'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    from .views import views
    from .auth import auth
    from .models import db

    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app