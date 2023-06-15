from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import sqlalchemy


from flask import Flask

app = Flask(__name__)

# from twitterProject.database import Database

meta = sqlalchemy.MetaData()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['SECRET_KEY'] = '4YrzfpQ4kGXjuP6w'

db = MySQL(app)