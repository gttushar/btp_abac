from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
import os
#from flask.ext.session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/btp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads/')
app.config['MAX_CONTENT_PATH'] = 100000000
#SESSION_TYPE='redis'
#Session(app)

db=SQLAlchemy(app)
login=LoginManager(app)
login.login_view='login'

from app import routes,models
from app.models import *
with app.test_request_context():
	db.create_all()
	db.session.commit()