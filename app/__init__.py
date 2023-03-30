from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
import os, pickle
#from flask.ext.session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/btp'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/duplicatebtp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads/')
app.config['MAX_CONTENT_PATH'] = 100000000
#SESSION_TYPE='redis'
#Session(app)

db=SQLAlchemy(app)
login=LoginManager(app)
login.login_view='login'

# poltree loading and store on server
from n_ary_poltree import poltree_generator
from n_ary_poltree.poltree_generator import node
# loading poltree from pickle file
poltree_generator.generator(True)
infile = open("n_ary_poltree/poltree.pkl","rb")
node_list = pickle.load(infile)



from app import routes,models
from app.models import *
with app.test_request_context():
	db.create_all()
	db.session.commit()
