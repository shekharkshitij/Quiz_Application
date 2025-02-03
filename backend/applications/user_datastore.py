from flask_security import SQLAlchemyUserDatastore
from applications.database import db
from applications.model import User, Role

# Initialize the user datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
