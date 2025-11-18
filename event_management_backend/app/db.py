from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# global db and migrate instances to be initialized by app factory
db = SQLAlchemy()
migrate = Migrate()
