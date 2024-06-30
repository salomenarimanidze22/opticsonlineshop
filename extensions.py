from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
UPLOAD_FOLDER = 'C:\\Users\\lol\\Desktop\\online glasses store\\static\\images'
app.config["SECRET_KEY"] = "dhsfhsycthewQQRWG@#$!Huauyo"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)