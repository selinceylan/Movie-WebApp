from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlite3 import dbapi2 as sqlite
import flask_whooshalchemy as wa
import flask_sqlalchemy

app= Flask (__name__)

#Config files
app.config['SECRET_KEY']='191a99b4b07f4a52bfad894897406bde'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['WHOOSH_BASE']='whoosh'
db = SQLAlchemy(app)
def unlock_db(site):
    """Replace db_filename with the name of the SQLite database."""
    connection = sqlite.connect(site)
    connection.commit()
    connection.close() 
bcrypt= Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from imdb_webapp import routes    