from flask import Flask
from flask_migrate import Migrate

from library.config import Config
from database.base.db import db

app = Flask(__name__)
app.config.from_object(Config.DB)

migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)