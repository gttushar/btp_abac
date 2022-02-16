from app import db, login
from app.routes import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Env_attributes(db.Model):
	__tablename__ = 'env_attributes'
	env_attribute_id = db.Column(db.Integer, primary_key=True)
	env_attribute = db.Column(db.String(64), nullable=False, unique=True)

class Resource_attributes(db.Model):
	__tablename__ = 'resource_attributes'
	resource_attribute_id = db.Column(db.Integer, primary_key=True)
	resource_attribute = db.Column(db.String(64), nullable=False, unique=True)

class User_attributes(db.Model):
	__tablename__ = 'user_attributes'
	user_attribute_id = db.Column(db.Integer, primary_key=True)
	user_attribute = db.Column(db.String(64), nullable=False, unique=True)


class Env_aval(db.Model):
	__tablename__ = 'env_aval'
	env_attribute_id = db.Column(db.Integer, db.ForeignKey('env_attributes.env_attribute_id'), primary_key=True)
	env_val = db.Column(db.String(64), primary_key=True)

class Resource_aval(db.Model):
	__tablename__ = 'resource_aval'
	resource_attribute_id = db.Column(db.Integer, db.ForeignKey('resource_attributes.resource_attribute_id'), primary_key=True)
	resource_val = db.Column(db.String(64), primary_key=True)

class User_aval(db.Model):
	__tablename__ = 'user_aval'
	user_attribute_id = db.Column(db.Integer, db.ForeignKey('user_attributes.user_attribute_id'), primary_key=True)
	user_val = db.Column(db.String(64), primary_key=True)
	# price = db.Column(db.Float(precision=5),nullable=False)
	# item_id = db.Column(db.Integer,primary_key=True)


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(64), nullable=False)
	login_name = db.Column(db.String(64), unique=True, nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	# city_id = db.Column(db.String(5),db.ForeignKey('city.city_id'),nullable = False)

	def __repr__(self):
		return f"User('{self.user_name}')"
	
	def set_password(self,password):
		self.password_hash = generate_password_hash(password)
	
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def get_id(self):
		return self.user_id


class User_details(db.Model):
	__tablename__ = 'user_details'
	user_id = db.Column(db.Integer, primary_key=True)
	user_attribute_id = db.Column(db.Integer, primary_key=True)
	user_val = db.Column(db.String(64), nullable=False)
	__table_args__ = (
		db.ForeignKeyConstraint(
			['user_attribute_id', 'user_val'],
			['user_aval.user_attribute_id', 'user_aval.user_val'],
		),
	)
	
	def __repr__(self):
		return f"User_Aval('{self.user_attribute_id}', '{self.user_val}')"


class Resource(db.Model):
	__tablename__ = 'resource'
	resource_id = db.Column(db.Integer, primary_key=True)
	resource_name = db.Column(db.String(128), nullable=False)
	# time_of_order = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

	def __repr__(self):
		return f"Resource('{self.resource_name}')"

	def get_id(self):
		return self.resource_id

class Resource_details(db.Model):
	__tablename__ = 'resource_details'
	resource_id = db.Column(db.Integer,primary_key=True)
	resource_attribute_id = db.Column(db.Integer, primary_key=True)
	resource_val = db.Column(db.String(64), nullable=False)
	
	__table_args__ = (
		db.ForeignKeyConstraint(
			['resource_attribute_id', 'resource_val'],
			['resource_aval.resource_attribute_id', 'resource_aval.resource_val'],
		),
	)    
	def __repr__(self):
		return f"Resource_Aval('{self.resource_attribute_id}', '{self.resource_val}')"


class Operations(db.Model):
	__tablename__ = 'operations'
	operation_id = db.Column(db.Integer, primary_key=True)
	operation_name = db.Column(db.String(16), default='read')

class Policy(db.Model):
	__tablename__ = 'policy'
	policy_id = db.Column(db.Integer, primary_key=True)
	operation_id = db.Column(db.Integer, db.ForeignKey('operations.operation_id'), nullable=False)
	# db.CheckConstraint('quantity>0','check1')

class Policy_user_aval(db.Model):
	__tablename__ = 'policy_user_aval'
	policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), primary_key=True)
	user_attribute_id = db.Column(db.Integer, primary_key=True)
	user_val = db.Column(db.String(64), primary_key=True)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['user_attribute_id', 'user_val'],
			['user_aval.user_attribute_id', 'user_aval.user_val'],
		),
	)

class Policy_resource_aval(db.Model):
	__tablename__ = 'policy_resource_aval'
	policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), primary_key=True)
	resource_attribute_id = db.Column(db.Integer, primary_key=True)
	resource_val = db.Column(db.String(64), primary_key=True)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['resource_attribute_id', 'resource_val'],
			['resource_aval.resource_attribute_id', 'resource_aval.resource_val'],
		),
	)    

class Policy_env_aval(db.Model):
	__tablename__ = 'policy_env_aval'
	policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), primary_key=True)
	env_attribute_id = db.Column(db.Integer, primary_key=True)
	env_val = db.Column(db.String(64), primary_key=True)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['env_attribute_id', 'env_val'],
			['env_aval.env_attribute_id', 'env_aval.env_val'],
		),
	)    

class Logs (db.Model):
	__tablename__ = 'logs'
	log_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# null for external user
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
	org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)
	resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'), nullable=False)
	operation_id = db.Column(db.Integer, db.ForeignKey('operations.operation_id'), nullable=True)
	decision = db.Column(db.String(1), nullable=False)
	__table_args__ = (
		db.CheckConstraint("decision IN ('y', 'n')"),
	)


# Access time (day/night), access day(weekend/weekday), ip/subnet
class Logs_env (db.Model):
	__tablename__ = 'Logs_env'
	log_no = db.Column(db.Integer, db.ForeignKey('logs.log_no'), primary_key=True)
	env_attribute_id = db.Column(db.Integer, primary_key=True)
	env_val = db.Column(db.String(64), nullable=False)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['env_attribute_id', 'env_val'],
			['env_aval.env_attribute_id', 'env_aval.env_val'],
		),
	)    


class Logs_user_aval(db.Model):
	__tablename__ = 'logs_user_aval'
	log_no = db.Column(db.Integer, db.ForeignKey('logs.log_no'), primary_key=True)
	user_attribute_id = db.Column(db.Integer, primary_key=True)
	user_val = db.Column(db.String(64), nullable=False)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['user_attribute_id', 'user_val'],
			['user_aval.user_attribute_id', 'user_aval.user_val'],
		),
	)    


class Org(UserMixin, db.Model):
	__tablename__ = 'org'
	org_id = db.Column(db.Integer, primary_key=True)
	org_name = db.Column(db.String(64), unique=True, nullable=False)
	public_key = db.Column(db.String(1024), nullable=False)

	def __repr__(self):
		return f"Org('{self.org_id}')"

	def get_id(self):
		return self.org_id


@login.user_loader
def load_user(user_id):
	if session['user_type'] == 'user':
		return User.query.filter_by(user_id=user_id).first()
	elif session['user_type'] == 'org':
		return Org.query.filter_by(org_id=user_id).first()
