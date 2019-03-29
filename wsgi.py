from flask import Flask
from admin import admin
from home import home
from common.extends import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('common/configs.py')
    app.jinja_env.trim_blocks = True
    register(app)
    return app

def register(app):
    db.init_app(app=app)
    app.register_blueprint(admin)
    app.register_blueprint(home)

blog = create_app()


if __name__ == '__main__':
    blog.run()