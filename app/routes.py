from flask import render_template, redirect, url_for, flash, request, session, abort, get_flashed_messages
from sqlalchemy import func, text, and_, or_
from flask_login import current_user,login_user, logout_user, login_required
from flask_mail import Mail, Message
from wtforms import StringField
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import datetime, sys, os, time, random

from app.forms import *
from app.models import *
from app import app
from app import db

@app.route('/')
def base():
	return redirect(url_for('login'))

		# if session['user_type'] == 'user':
		# 	return redirect(url_for('user_home'))
		# elif session['user_type'] == 'org':
		# 	return redirect(url_for('org_home'))
	# session['user_type'] = 'user'
@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('user_home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(login_name=form.login_id.data).first()
		if user is None:
			user = User.query.filter_by(email=form.login_id.data).first()
		if user is None or not user.check_password(form.pwd.data):
			flash('Invalid login id or email or password','danger')
			return redirect(url_for('login'))
		user_type_detail = User_details.query \
					.join(User_attributes, User_attributes.user_attribute_id == User_details.user_attribute_id) \
					.add_columns(User_details.user_id, User_details.user_attribute_id,  \
								 User_attributes.user_attribute, User_details.user_val) \
					.filter(User_details.user_id == user.user_id) \
					.filter(User_attributes.user_attribute == 'user_type').first()

		# print(user_type_detail.keys())

		session['user_id'] = user.user_id
		session['user_name'] = user.user_name
		session['user_type'] = 'user'
		print ("details = ", user_type_detail)
		if user_type_detail is not None and user_type_detail[4].lower() == 'admin':  # 4 = index of user_val string
			print('Hello admin !!! ')
			session['admin'] = True
		else:
			session['admin'] = False
		login_user(user)

		session['logged_in'] = True
		flash('Successfully logged in','success')
		# print(form.user_type.data + " successfully logged in", file=sys.stderr)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for(session['user_type'] + '_home')
		return redirect(next_page)
	return render_template('login.html',title='Sign In',form=form)


@app.route('/user_home',methods = ['GET','POST'])
@login_required
def user_home():
	#print(session['user_type'], " Home : ", session['user_id'], file=sys.stderr)
	if session['user_type'] != 'user':
		abort(403)
	return render_template('user_home.html', title='User Home', user_name=session['user_name'])


@app.route('/add_attribute',methods = ['GET','POST'])
@login_required
def add_attribute():
	if not session['admin']:
		abort(403)
	form = AddAttributeForm()
	if form.validate_on_submit():
		attr_type = form.attr_type.data.lower()
		attribute = form.attribute.data.lower()
		if attr_type == 'user':
			exists = User_attributes.query.filter_by(user_attribute=attribute).first()
			if exists is None:
				attr_id = db.session.query(func.max(User_attributes.user_attribute_id)).scalar()
				attr_id = (int(attr_id) + 1) if attr_id is not None else 1
				db.session.add(User_attributes(user_attribute_id=attr_id, user_attribute=attribute))
				flash(attribute + ' added successfully to User attributes!!', 'success')
			else:
				flash(attribute + ' attribute already exists!!', 'danger')
		elif attr_type == 'resource':
			exists = Resource_attributes.query.filter_by(resource_attribute=attribute).first()
			if exists is None:
				attr_id = db.session.query(func.max(Resource_attributes.resource_attribute_id)).scalar()
				attr_id = (int(attr_id) + 1) if attr_id is not None else 1
				db.session.add(Resource_attributes(resource_attribute_id=attr_id, resource_attribute=attribute))
				flash(attribute + ' added successfully to Resource attributes!!', 'success')
			else:
				flash(attribute + ' attribute already exists!!', 'danger')
		else:
			exists = Env_attributes.query.filter_by(env_attribute=attribute).first()
			if exists is None:
				attr_id = db.session.query(func.max(Env_attributes.env_attribute_id)).scalar()
				attr_id = (int(attr_id) + 1) if attr_id is not None else 1
				db.session.add(Env_attributes(env_attribute_id=attr_id, env_attribute=attribute))
				flash(attribute + ' added successfully to Env attributes!!', 'success')
			else:
				flash(attribute + ' attribute already exists!!', 'danger')

		db.session.commit()

	return render_template('add_attribute.html', title='Add attribute', form=form)


@app.route('/add_aval',methods = ['GET','POST'])
@login_required
def add_aval():
	if not session['admin']:
		abort(403)
	form = AddAvalForm()
	if form.validate_on_submit():
		attr_type = form.attr_type.data.lower()
		attribute = form.attribute.data.lower()
		val = form.val.data
		if attr_type == 'user':
			attr_row = User_attributes.query.filter_by(user_attribute=attribute).first()
			if attr_row is not None:
				attr_id = int(attr_row.user_attribute_id)
				aval_row = User_aval.query.filter_by(user_attribute_id=attr_id, user_val=val).first()
				if aval_row is None:
					db.session.add(User_aval(user_attribute_id=attr_id, user_val=val))
					flash('(' + attribute + ', ' + val + ') pair added successfully to User attr-vals!!', 'success')
				else:
					flash('(' + attribute + ', ' + val + ') pair already exists!!', 'danger')
			else:
				flash(attribute + ' attribute does not exist!!', 'danger')
		elif attr_type == 'resource':
			attr_row = Resource_attributes.query.filter_by(resource_attribute=attribute).first()
			if attr_row is not None:
				attr_id = int(attr_row.resource_attribute_id)
				aval_row = Resource_aval.query.filter_by(resource_attribute_id=attr_id, resource_val=val).first()
				if aval_row is None:
					db.session.add(Resource_aval(resource_attribute_id=attr_id, resource_val=val))
					flash('(' + attribute + ', ' + val + ') pair added successfully to Resource attr-vals!!', 'success')
				else:
					flash('(' + attribute + ', ' + val + ') pair already exists!!', 'danger')
			else:
				flash(attribute + ' attribute does not exist!!', 'danger')
		else:
			attr_row = Env_attributes.query.filter_by(env_attribute=attribute).first()
			if attr_row is not None:
				attr_id = int(attr_row.env_attribute_id)
				aval_row = Env_aval.query.filter_by(env_attribute_id=attr_id, env_val=val).first()
				if aval_row is None:
					db.session.add(Env_aval(env_attribute_id=attr_id, env_val=val))
					flash('(' + attribute + ', ' + val + ') pair added successfully to Env attr-vals!!', 'success')
				else:
					flash('(' + attribute + ', ' + val + ') pair already exists!!', 'danger')
			else:
				flash(attribute + ' attribute does not exist!!', 'danger')

		db.session.commit()
	return render_template('add_aval.html', title='Add attr-value', form=form)


@app.route('/register_user', methods=['GET', 'POST'])
@login_required
def register_user():
	if not session['admin']:
		return redirect(url_for('logout'))

	form = User_Registration_Form()

	if form.validate_on_submit():
		user_id = db.session.query(func.max(User.user_id)).scalar()
		user_id = (int(user_id) + 1) if user_id is not None else 1
		user = User(user_id=user_id, user_name=form.user_name.data, login_name=form.login_name.data, email=form.email.data)
		user.set_password(form.pwd.data)
		db.session.add(user)
		db.session.commit()
		flash('User added successfully!', 'success')
		return redirect(url_for('update_user'))
	return render_template('register_user.html', title='Register new User', form=form)

@app.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
	if not session['admin']:
		return redirect(url_for('logout'))

	form = User_Registration_Form()

	if not form.login_name.data:
		return render_template('update_user.html', title='Update User', form=form)

	if form.submit_id.data:
		user = User.query.filter_by(login_name=form.login_name.data).first()
		if user is None:
			user = User.query.filter_by(email=form.login_name.data).first()
		if user is None:
			flash('Invalid login name or email','danger')
			return redirect(url_for('update_user'))
		user_details = User_details.query.filter_by(user_id=user.user_id) \
						.join(User_attributes, User_attributes.user_attribute_id == User_details.user_attribute_id) \
						.add_columns(User_details.user_id, User_details.user_attribute_id,  \
									 User_attributes.user_attribute, User_details.user_val) \
						.all()
		form.user_name.data = user.user_name
		form.login_name.data = user.login_name
		form.email.data = user.email
		for aval in user_details:
			aval_form = AvalForm()
			aval_form.attribute_id = aval['user_attribute_id']
			aval_form.attribute = aval['user_attribute']
			aval_form.val = aval['user_val']
			aval_form.new_val = ''
			form.details.append_entry(aval_form)


	if form.add_aval.data:
		form.details.append_entry()
		return render_template('update_user.html', title='Update User', form=form)

	if form.submit.data:
		user = User.query.filter_by(login_name=form.login_name.data).first()
		if user is None:
			user = User.query.filter_by(email=form.login_name.data).first()
		details_to_add = []
		for aval in form.details.data:
			if aval['attribute_id']:
				# print('aval with id = '); print(aval);
				if aval['new_val']:
					valid_aval = User_aval.query.filter_by(user_attribute_id=aval['attribute_id'], \
																   user_val=aval['new_val']).first()
					if valid_aval is not None:
						row = User_details.query.filter_by(user_id=user.user_id, \
							user_attribute_id=aval['attribute_id'], user_val=aval['val']).first()
						row.user_val = aval['new_val']
						db.session.merge(row)
					else:
						flash(aval['new_val'] + ' is invalid value for attribute ' + aval['attribute'], 'danger')
						return redirect(url_for('update_user'))
			else:
				# print('aval without = '); print(aval);
				valid_attribute = User_attributes.query.filter_by(user_attribute=aval['attribute'].lower()).first()
				if valid_attribute is not None:
					aval['attribute_id'] = valid_attribute.user_attribute_id
					valid_aval = User_aval.query.filter_by(user_attribute_id=aval['attribute_id'], user_val=aval['val']).first()
					if valid_aval is not None:
						user_detail = User_details(user_id=user.user_id,user_attribute_id=aval['attribute_id'],user_val=aval['val'])
						db.session.add(user_detail)
					else:
						flash(aval['val'] + ' is invalid value for attribute ' + aval['attribute'], 'danger')
						return render_template('update_user.html', title='Update User', form=form)
						# return redirect(url_for('update_user'))
				else:
					flash(aval['attribute'] + ' is not a valid user attribute!!', 'danger')
					return render_template('update_user.html', title='Update User', form=form)
					# return redirect(url_for('update_user'))
		while form.details.data:
			form.details.pop_entry()
		db.session.commit()
		flash('User details updated successfully!', 'success')
		return redirect(url_for('update_user'))
	return render_template('update_user.html', title='Update User', form=form)


@app.route('/add_resource',methods = ['GET','POST'])
@login_required
def add_resource():
	if not session['admin']:
		abort(403)

	form = AddResourceForm()

	if form.validate_on_submit() or form.submit.data:
		resource_id = db.session.query(func.max(Resource.resource_id)).scalar()
		resource_id = (resource_id + 1) if resource_id is not None else 1
		resource = Resource(resource_id=resource_id, resource_name=form.resource_name.data.lower())
		db.session.add(resource)

		# for aval in form.details.data:
		# 	resource_detail= Resource_details(resource_id=max_id,attribute=aval['attribute'].lower(),val=aval['val'].lower())
		# 	db.session.add(resource_detail)
		# for aval in form.policy.data:
		# 	policy = Policy(resource_id=max_id, attribute=aval['attribute'].lower(), val=aval['val'].lower())
		# 	db.session.add(policy)

		db.session.commit()
		flash('Resource added successfully!', 'success')
		return redirect(url_for('update_resource'))
	return render_template('add_resource.html', form=form)

@app.route('/update_resource', methods=['GET', 'POST'])
@login_required
def update_resource():
	if not session['admin']:
		return redirect(url_for('logout'))

	form = AddResourceForm()
	resources = Resource.query.all()

	if not form.resource_id.data:
		return render_template('update_resource.html', title='Update Resource', form=form, resources=resources)

	if form.add_aval.data:
		resource_id = form.resource_id.data
		form.details.append_entry()
		return render_template('update_resource.html', title='Update Resource', form=form, resources=resources, resource_id=resource_id)

	if form.submit_id.data:
		resource_id = form.resource_id.data
		resource = Resource.query.filter_by(resource_id=resource_id).first()
		# valid resource check not required uue to drop down selection
		print('resource = '); print(resource)
		resource_details = Resource_details.query.filter_by(resource_id=resource.resource_id) \
						.join(Resource_attributes, Resource_attributes.resource_attribute_id == Resource_details.resource_attribute_id) \
						.add_columns(Resource_details.resource_id, Resource_details.resource_attribute_id,  \
									 Resource_attributes.resource_attribute, Resource_details.resource_val) \
						.all()
		form.resource_id.data = resource.resource_id
		form.resource_name.data = resource.resource_name
		for aval in resource_details:
			aval_form = AvalForm()
			aval_form.attribute_id = aval['resource_attribute_id']
			aval_form.attribute = aval['resource_attribute']
			aval_form.val = aval['resource_val']
			aval_form.new_val = ''
			form.details.append_entry(aval_form)
		return render_template('update_resource.html', title='Update Resource', form=form, resources=resources, resource_id=resource_id)

	if form.submit.data:
		resource = Resource.query.filter_by(resource_id=form.resource_id.data).first()
		for aval in form.details.data:
			if aval['attribute_id']:
				# print('aval with id = '); print(aval);
				if aval['new_val']:
					valid_aval = Resource_aval.query.filter_by(resource_attribute_id=aval['attribute_id'], \
															   resource_val=aval['new_val']).first()
					if valid_aval is not None:
						row = Resource_details.query.filter_by(resource_id=resource.resource_id, \
							resource_attribute_id=aval['attribute_id'], resource_val=aval['val']).first()
						row.resource_val = aval['new_val']
						db.session.merge(row)
					else:
						flash(aval['new_val'] + ' is invalid value for attribute ' + aval['attribute'], 'danger')
						return redirect(url_for('update_resource'))
			else:
				# print('aval without = '); print(aval);
				valid_attribute = Resource_attributes.query.filter_by(resource_attribute=aval['attribute'].lower()).first()
				if valid_attribute is not None:
					aval['attribute_id'] = valid_attribute.resource_attribute_id
					valid_aval = Resource_aval.query.filter_by(resource_attribute_id=aval['attribute_id'], \
															   resource_val=aval['val']).first()
					if valid_aval is not None:
						resource_detail = Resource_details(resource_id=resource.resource_id, \
										resource_attribute_id=aval['attribute_id'],resource_val=aval['val'])
						db.session.add(resource_detail)
					else:
						flash(aval['val'] + ' is invalid value for attribute ' + aval['attribute'], 'danger')
						return render_template('update_resource.html', title='Update Resource', form=form, resources=resources)
						# return redirect(url_for('update_resource'))
				else:
					flash(aval['attribute'] + ' is not a valid resource attribute!!', 'danger')
					return render_template('update_resource.html', title='Update Resource', form=form, resources=resources)
					# return redirect(url_for('update_resource'))
		while form.details.data:
			form.details.pop_entry()
		db.session.commit()
		flash('Resource details updated successfully!', 'success')
		return redirect(url_for('update_resource'))
	return render_template('update_resource.html', title='Update Resource', form=form)


@app.route('/add_policy', methods=['GET', 'POST'])
@login_required
def add_policy():
	if not session['admin']:
		return redirect(url_for('logout'))
	form = AddPolicyForm()

	operations = Operations.query.all()

	if form.add_user_aval.data:
		form.user_aval.append_entry()
		return render_template('add_policy.html', title='Add Policy', form=form, operations=operations)
	if form.add_resource_aval.data:
		form.resource_aval.append_entry()
		return render_template('add_policy.html', title='Add Policy', form=form, operations=operations)
	if form.add_env_aval.data:
		form.env_aval.append_entry()
		return render_template('add_policy.html', title='Add Policy', form=form, operations=operations)

	if form.submit.data:
		policy_id = db.session.query(func.max(Policy.policy_id)).scalar()
		policy_id = (1 + int(policy_id)) if policy_id is not None else 1
		policy = Policy(policy_id=policy_id, operation_id=form.operation_id.data)
		db.session.add(policy)
		db.session.commit()
		for aval in form.user_aval.data:
			row = User_attributes.query.filter_by(user_attribute=aval['attribute']).first()
			attribute_id = row.user_attribute_id
			db.session.add(Policy_user_aval(policy_id=policy_id, user_attribute_id=attribute_id, user_val=aval['val']))
		for aval in form.resource_aval.data:
			row = Resource_attributes.query.filter_by(resource_attribute=aval['attribute']).first()
			attribute_id = row.resource_attribute_id
			db.session.add(Policy_resource_aval(policy_id=policy_id, resource_attribute_id=attribute_id, resource_val=aval['val']))
		for aval in form.env_aval.data:
			row = Env_attributes.query.filter_by(env_attribute=aval['attribute']).first()
			attribute_id = row.env_attribute_id
			db.session.add(Policy_env_aval(policy_id=policy_id, env_attribute_id=attribute_id, env_val=aval['val']))
		db.session.commit()

		flash('Policy added successfully!', 'success')
		return redirect(url_for('add_policy'))
	return render_template('add_policy.html', title='Add Policy', form=form, operations=operations)


def check_env(env_id, env_val):
	if not env_id:
		return 1
	now = datetime.datetime.now()
	# weekday  (1(true) or 0(false))
	if env_id == 1:	# return 1 if env_val is satisfied else 0
		return (1 if bool(env_val) == (now.weekday() < 5) else 0)
	# office_hours (8am to 5pm) (1(true) or 0(false))
	if env_id == 2:	# return 1 if env_val is satisfied else 0
		return (1 if bool(env_val) == (now.weekday() < 5 and now.hour >= 8 and now.hour < 17) else 0)

	return 0

def get_env():
	now = datetime.datetime.now()
	env = {}
	env['weekday'] = '1' if now.weekday() < 5 else '0'
	env['office_hours'] = '1' if (now.hour >= 8 and now.hour < 17) else '0'
	return env


@app.route('/access_resource_user', methods=['GET', 'POST'])
@login_required
def access_resource_user():
	if not current_user.is_authenticated:
		abort(403)
	# print('On page access_resource_user', file=sys.stderr, flush=True)

	resources = Resource.query.all()

	if request.method == "POST" and 'send_otp' in request.form:
		app.config["MAIL_SERVER"]   = 'iitkgpmail.iitkgp.ac.in'
		app.config["MAIL_PORT"]     = 465
		app.config["MAIL_USERNAME"] = 'gupta.tushar@iitkgp.ac.in'
		app.config['MAIL_PASSWORD'] = 'Abcd@1234'
		app.config['MAIL_USE_TLS']  = False
		app.config['MAIL_USE_SSL']  = True
		mail = Mail(app)  
		otp = random.randint(100000,999999)
		session['otp'] = otp
		# user_email = User.query.filter_by(user_id=session['user_id']).first().email
		# currently using same email for all users
		user_email = 'thetushar.g14@gmail.com'
		msg = Message('OTP',sender = app.config["MAIL_USERNAME"], recipients = [user_email])
		msg.body = 'OTP for verification : ' +  str(otp)
		mail.send(msg)
		print("request.form['resource_id'] =", request.form['resource_id'])
		print('OTP sending success !')
		# message = 'Operations allowed on \'mechanics.pdf\' = \'read\', \'write\''
		return render_template('access_resource_user.html', resources=resources, sent_otp=True, selected_resource=request.form['resource_id'])

	
	elif request.method == "POST":
		# print('Access request', file=sys.stderr, flush=True)
		user_id = session['user_id']
		user_name = User.query.filter_by(user_id=user_id).first().user_name
		user_details = User_details.query.filter_by(user_id=user_id).all()
		user_aval_list = []
		user_data = 'Name: ' + user_name + '\n'
		for row in user_details:
			user_data += User_attributes.query.filter_by(user_attribute_id=row.user_attribute_id).first().user_attribute \
						+ ': ' + row.user_val + '\n'
		user_data = user_data[:-1]

		start_time = datetime.datetime.now()

		runQuery = SparqlQueries()
		for row in user_details:
			val = row.user_val
			val_list = list(set(runQuery.ancestor_search(val) +	runQuery.descendant_search(val)))
			user_aval_list.append({ 'user_attribute_id': row.user_attribute_id, 'user_val': val_list })
		# user_aval_dict = {}
		# for aval in user_aval_list:
		# 	user_aval_dict[aval['attribute']] = aval['val']
		# if user_id == 3:
			# return render_template('access_resource_user.html', resources=resources, message='Sorry, you are not allowed to access \'galvin.pdf\'', user_name=user_name)

		otp_matched = False
		if 'otp' in request.form:
			if int(session['otp']) == int(request.form['otp']):
				print('Otp matched !!')
				otp_matched = True
			session.pop('otp',None)

		resource_id = request.form['resource_id']
		resource = Resource.query.filter_by(resource_id=resource_id).first()
		resource_details = Resource_details.query.filter_by(resource_id=resource_id).all()

		allowed_operations = dict()		# operation_id : operation_name

		policies = Policy.query.join(Operations, Operations.operation_id==Policy.operation_id) \
					.with_entities(Policy.policy_id, Operations.operation_id, Operations.operation_name).all()
		# for policy in policies:
		# 	print('policy = ', end=' ');	print(policy);
		for policy in policies:
			policy_user_aval_list = Policy_user_aval.query.filter_by(policy_id=policy.policy_id).all()
			policy_resource_aval_list = Policy_resource_aval.query.filter_by(policy_id=policy.policy_id).all()
			policy_env_aval_list = Policy_env_aval.query.filter_by(policy_id=policy.policy_id).all()
			user_aval_valid = 0
			resource_aval_valid = 0
			env_aval_valid = 0
			for policy_aval in policy_user_aval_list:
				match = 0
				for aval in user_aval_list:
					# print('policy_aval.user_val = ' + policy_aval.user_val + 'aval[\'user_val\'] = ',end=' ')
					# print(aval['user_val'])
					if policy_aval.user_val in aval['user_val']:
						match += 1
				if match > 0:
					user_aval_valid += 1
				# print('policy_aval = ',end=''); print(policy_aval); print('match = ' + str(match));
			for policy_aval in policy_resource_aval_list:
				match = 0
				for aval in resource_details:
					if aval.resource_attribute_id==policy_aval.resource_attribute_id and aval.resource_val==policy_aval.resource_val:
						match += 1
				if match > 0:
					resource_aval_valid += 1
			for policy_aval in policy_env_aval_list:
				required = bool(int(policy_aval.env_val))
				match policy_aval.env_attribute_id:
					case 1:
						env_aval_valid += (1 if not required or now.weekday() < 5 else 0)
					case 2:
						env_aval_valid += (1 if not required or (now.weekday() < 5 and now.hour >= 8 and now.hour < 17) else 0)
					case 3:
						env_aval_valid += (1 if not required or otp_matched else 0)
				# env_aval_valid += check(policy_aval.env_attribute_id, policy_aval.env_val)


			if 	user_aval_valid == len(policy_user_aval_list) and \
					resource_aval_valid == len(policy_resource_aval_list) and \
						env_aval_valid == len(policy_env_aval_list):
				allowed_operations[policy.operation_id] = policy.operation_name
		''' old policy check code
		for policy in policy_list:
			valid = 0
			for aval in user_details:
				if aval.user_attribute_id==policy.user_attribute_id and aval.user_val.lower()==policy.user_val.lower():
					valid += 1
			for aval in resource_details:
				if aval.resource_attribute_id==policy.resource_attribute_id and aval.resource_val.lower()==policy.resource_val.lower():
					valid += 1
			valid += check_env(policy.env_attribute_id, policy.env_val)		#Env avals

			if valid == 3:
				allowed_operations[policy.operation_id] = policy.operation_name
		'''

		# entry in Logs table
		# orgs = Org.query.all()
		# for org in orgs:
		# 	print('org_name = ' + org.org_name, file=sys.stderr)
		org_id = int(Org.query.filter(or_(func.lower(Org.org_name) == func.lower("IIT-KGP"), \
										  func.lower(Org.org_name) == func.lower("IIT Kharagpur"), \
										  func.lower(Org.org_name) == func.lower("IIT_KGP"))).first().org_id)
		log_no = db.session.query(func.max(Logs.log_no)).scalar()
		log_no = (log_no + 1) if log_no is not None else 1
		log = Logs(log_no=log_no, user_id=user_id, org_id=org_id, resource_id=resource_id, decision='n')
		
		message = ''
		if len(allowed_operations) > 0:		# i.e. is not empty
			message += 'Operations allowed on \'' + resource.resource_name + '\' = '
			for key in sorted(allowed_operations):
				message += '\'' + allowed_operations[key] + '\' , '
			while message[-1] != '\'':
				message = message[:-1]
			log.decision = 'y'	# update decision in current log object
			log.operation_id = sorted(allowed_operations.keys())[0]
		else:
			message = 'Sorry, you are not allowed to access \'' + resource.resource_name + '\''

		''' logging code
		db.session.add(log)
		db.session.commit()
		# entries in Logs_user_aval table
		for aval in user_details:
			log_user_aval = Logs_user_aval(log_no=log.log_no, user_attribute_id=aval.user_attribute_id, user_val=aval.user_val)
			db.session.add(log_user_aval)
		db.session.commit()

		# entries in Logs_env table
		env = get_env()
		day_env_id = int(Env_attributes.query.filter_by(env_attribute='day').first().env_attribute_id)
		time_env_id = int(Env_attributes.query.filter_by(env_attribute='time').first().env_attribute_id)
		db.session.add(Logs_env(log_no=log_no, env_attribute_id=day_env_id, env_val=env['day']))
		db.session.add(Logs_env(log_no=log_no, env_attribute_id=time_env_id, env_val=env['time']))

		db.session.commit()
		'''

		end_time = datetime.datetime.now() #time.time()
		execution_time = (end_time - start_time).microseconds / 1000000.0
		return render_template('access_resource_user.html', resources=resources, message=message, user_name=user_name, execution_time=execution_time, user_aval=user_data)

	return render_template('access_resource_user.html', resources=resources)


def get_private_key(org_name):
    file = open(os.path.join(os.path.dirname(__file__), '../private_keys.txt'), 'r+t')
    for line in file.readlines():
        words = line.split(':')
        if words[1] == org_name:
            return words[3]
    return None
def get_public_key(org_name):
    file = open(os.path.join(os.path.dirname(__file__), '../private_keys.txt'), 'r+t')
    for line in file.readlines():
        words = line.split(':')
        if words[1] == org_name:
            return words[2]
    return None

# digital signature libs and funcs
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
import base64

def base64_to_bytes(key:str) -> bytes: 
    return base64.b64decode(key.encode('utf-8'))

def encrypt_for_user(sender_private:str, receiver_public:str, message:str) -> str: 
    sender_private = PrivateKey(base64_to_bytes(sender_private))
    receiver_public = PublicKey(base64_to_bytes(receiver_public))
    sender_box = Box(sender_private, receiver_public)
    return base64.b64encode(sender_box.encrypt(bytes(message, "utf-8"))).decode('utf-8')

def decrypt_for_user(receiver_private:str, sender_public:str, message:str) -> str: 
    receiver_private = PrivateKey(base64_to_bytes(receiver_private))
    sender_public = PublicKey(base64_to_bytes(sender_public))
    receiver_box = Box(receiver_private, sender_public)
    return receiver_box.decrypt(base64.b64decode(message.encode('utf-8'))).decode('utf-8')

# importing ontology query python functions
from .owlquery import *

# getting execution time
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

@app.route('/access_resource_non_user', methods=['GET', 'POST'])
def access_resource_non_user():
	# print('On page access_resource_non_user', file=sys.stderr, flush=True)
	resources = Resource.query.all()
	orgs = Org.query.all()

	if request.method == "POST":
		print('Access request non user', file=sys.stderr, flush=True)
		start_time = datetime.datetime.now()

		org_name = ''
		digital_signature = request.files['digital_signature']
		filename = secure_filename(digital_signature.filename)
		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		# with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
		encrypted_data = digital_signature.read().decode()	# read() returns bytes
		# decoding
		org_id = request.form['org_id']
		sender_public = Org.query.filter_by(org_id=org_id).first().public_key
		receiver_private = get_private_key('IIT Kharagpur')
		# print('sender_public = ' + sender_public)
		# print('receiver_private = ' + receiver_private)
		decrypted_data = None
		try:
			decrypted_data = decrypt_for_user(receiver_private, sender_public, encrypted_data)
		except:
			message = 'Access denied: Digital signature could not be verified'
			return render_template('access_resource_non_user.html', resources=resources, orgs=orgs, message=message)


		# for each max_distance, cartesian product : list of aval dicts
		user_details = [[]]
		# distance = 0
		# for line in decrypted_data.split('\n'):
		# 	name, val = line.split(':')
		# 	id = User_attributes.query.filter_by(user_attribute=name).first().user_attribute_id
		# 	user_details[0].append({ 'user_attribute_id': tuple([ id ]), 'user_val': [val] })
		# 	print('distance = 0, aval = ');print({ 'user_attributes': name, 'user_attribute_id': tuple([ id ]), 'user_val': [val] });
		max_distance = 3
		runQuery = SparqlQueries()
		detail_list = []
		user_aval_list = []
		for line in decrypted_data.split('\n'):
			attr_name, val = line.split(':')
			attr_name_list = runQuery.distance_search(attr_name, 0)	# list cant be key of dict
			attr_id_list = []
			for elem in attr_name_list:
				id = User_attributes.query.filter_by(user_attribute=elem).first()
				if id is not None:
					attr_id_list.append(id.user_attribute_id)
			attr_id_list = tuple(attr_id_list)
			# val_list = runQuery.ancestor_search(val)
			val_list = list(set(runQuery.ancestor_search(val) + \
								runQuery.descendant_search(val) + \
								runQuery.distance_search(val, max_distance)))
			user_aval_list.append({ 'user_attribute_id': attr_id_list, 'user_val': val_list })
			# print('user aval = ');print({ 'user_attributes': attr_name_list, 'user_attribute_id': attr_id_list, 'user_val': val_list });

		resource_id = request.form['resource_id']
		resource = Resource.query.filter_by(resource_id=resource_id).first()
		resource_details = Resource_details.query.filter_by(resource_id=resource_id).all()

		message = ''
		message = 'Max mapping distance = ' + str(max_distance) + '\n\n'

		allowed_operations = dict()		# operation_id : operation_name

		policies = Policy.query.join(Operations, Operations.operation_id==Policy.operation_id) \
					.with_entities(Policy.policy_id, Operations.operation_id, Operations.operation_name).all()
		# for policy in policies:
		# 	print('policy = ', end=' ');	print(policy);
		for policy in policies:
			policy_user_aval_list = Policy_user_aval.query.filter_by(policy_id=policy.policy_id).all()
			policy_resource_aval_list = Policy_resource_aval.query.filter_by(policy_id=policy.policy_id).all()
			policy_env_aval_list = Policy_env_aval.query.filter_by(policy_id=policy.policy_id).all()
			user_aval_valid = 0
			resource_aval_valid = 0
			env_aval_valid = 0
			for policy_aval in policy_user_aval_list:
				match = 0
				for aval in user_aval_list:
					# print('policy_aval.user_val = ' + policy_aval.user_val + 'aval[\'user_val\'] = ',end=' ')
					# print(aval['user_val'])
					if policy_aval.user_val in aval['user_val']: #and policy_aval.user_attribute_id in aval['user_attribute_id'] 
						match += 1
				if match > 0:
					user_aval_valid += 1
				# print('policy_aval = ',end=''); print(policy_aval); print('match = ' + str(match));
			for policy_aval in policy_resource_aval_list:
				match = 0
				for aval in resource_details:
					if aval.resource_attribute_id==policy_aval.resource_attribute_id and aval.resource_val==policy_aval.resource_val:
						match += 1
				if match > 0:
					resource_aval_valid += 1
			for policy_aval in policy_env_aval_list:
				required = bool(int(policy_aval.env_val))
				match policy_aval.env_attribute_id:
					case 1:
						env_aval_valid += (1 if not required or now.weekday() < 5 else 0)
					case 2:
						env_aval_valid += (1 if not required or (now.weekday() < 5 and now.hour >= 8 and now.hour < 17) else 0)
					case 3:
						env_aval_valid += (1 if not required else 0)



			if 	user_aval_valid == len(policy_user_aval_list) and \
					resource_aval_valid == len(policy_resource_aval_list) and \
						env_aval_valid == len(policy_env_aval_list):
				allowed_operations[policy.operation_id] = policy.operation_name

		# message += '\n\n(ancestral heirarchy)\n\t'
		# if distance == 0:
			# message = 'Sorry, you are not allowed to access \'galvin.pdf\''
		if len(allowed_operations) > 0:		# i.e. is not empty
			message += 'Operations possible on \'' + resource.resource_name + '\' = '
			for key in sorted(allowed_operations):
				message += '\'' + allowed_operations[key] + '\' , '
			while message[-1] != '\'':
				message = message[:-1]
			# message += ', \'append\''
		else:
			message += 'Sorry, you are not allowed to access \'' + resource.resource_name + '\''

		end_time = datetime.datetime.now()
		execution_time = (end_time - start_time).microseconds / 1000000.0
		print('message = \n' + message)

		# ONTOLOGY kabaad end

		# allowed_operations = dict()		# operation_id : operation_name
		# for policy in policy_list:
		# 	valid = 0
		# 	# print('policy = '); print(policy);
		# 	for aval in user_details:
		# 		if aval['user_attribute_id']==policy.user_attribute_id and aval['user_val']==policy.user_val:
		# 			valid += 1
		# 	for aval in resource_details:
		# 		if aval.resource_attribute_id==policy.resource_attribute_id and aval.resource_val==policy.resource_val:
		# 			valid += 1
		# 	valid += check_env(policy.env_attribute_id, policy.env_val)		#Env avals

		# 	if valid == 3:
		# 		allowed_operations[policy.operation_id] = policy.operation_name

		# IMP: ENTRIES IN LOG TABLE

		# # entry in Logs table
		# log_no = db.session.query(func.max(Logs.log_no)).scalar()
		# log_no = (log_no + 1) if log_no is not None else 1
		# log = Logs(log_no=log_no, org_id=org_id, resource_id=resource_id, decision='n')
		
		# message = ''
		# if len(allowed_operations) > 0:		# i.e. is not empty
		# 	message = 'Operations allowed on \'' + resource.resource_name + '\' = '
		# 	for key in sorted(allowed_operations):
		# 		message += '\'' + allowed_operations[key] + '\''
		# 	log.decision = 'y'	# update decision in current log object
		# 	log.operation_id = sorted(allowed_operations.keys())[0]
		# else:
		# 	message = 'Sorry, you are not allowed to access \'' + resource.resource_name + '\''

		# db.session.add(log)
		# db.session.commit()
		# # entries in Logs_user_aval table
		# for aval in user_details:
		# 	log_user_aval = Logs_user_aval(log_no=log.log_no, user_attribute_id=aval['user_attribute_id'], user_val=aval['user_val'])
		# 	db.session.add(log_user_aval)
		# db.session.commit()

		# # entries in Logs_env table
		# env = get_env()
		# day_env_id = int(Env_attributes.query.filter_by(env_attribute='day').first().env_attribute_id)
		# time_env_id = int(Env_attributes.query.filter_by(env_attribute='time').first().env_attribute_id)
		# db.session.add(Logs_env(log_no=log_no, env_attribute_id=day_env_id, env_val=env['day']))
		# db.session.add(Logs_env(log_no=log_no, env_attribute_id=time_env_id, env_val=env['time']))
		
		# db.session.commit()

		return render_template('access_resource_non_user.html', resources=resources, orgs=orgs, message=message, user_aval=decrypted_data, execution_time=execution_time)

	return render_template('access_resource_non_user.html', resources=resources, orgs=orgs)

from flask import g

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(str(diff))
    if (response.response and 200 <= response.status_code < 300):
        response.set_data(response.get_data().replace(b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
    return response

def insert_users(num_users, num_user_aval):
	offset = 100 # ids start from offset
	for i in range(num_users):
		user_id = offset + i
		user = User(user_id=user_id, user_name='user_name'+str(user_id), login_name='login_name'+str(user_id), email=str(user_id)+'@gmail.com')
		user.set_password('password' + str(user_id))
		db.session.add(user)
		for j in range(num_user_aval):
			user_detail = User_details(user_id=user_id,user_attribute_id=offset + j,user_val='userval'+str(j))
			db.session.add(user_detail)
	db.session.commit()
	print('users insertion done')
def insert_resources(num_resources, num_resource_aval):
	offset = 100 # ids start from offset
	for i in range(num_resources):
		resource_id = offset + i
		resource = Resource(resource_id=resource_id, resource_name='resource_name'+str(resource_id))
		db.session.add(resource)
		for j in range(num_resource_aval):
			resource_detail = Resource_details(resource_id=resource_id, \
								resource_attribute_id=offset + j,resource_val='resource_val'+str(j))
			db.session.add(resource_detail)
	db.session.commit()
	print('resources insertion done')
def insert_rules(num_rules, num_rule_aval):
	offset = 100 # ids start from offset
	for i in range(num_rules):
		policy_id = offset + i
		policy = Policy(policy_id=policy_id, operation_id=5)
		db.session.add(policy)
		for j in range(num_rule_aval):
			policy_user_aval = Policy_user_aval(policy_id=policy_id, user_attribute_id=offset+j, user_val='user_val'+str(j))
			db.session.add(policy_user_aval)
			policy_resource_aval = Policy_resource_aval(policy_id=policy_id, resource_attribute_id=offset+j, resource_val='resource_val'+str(j))
			db.session.add(policy_resource_aval)
			policy_env_aval = Policy_env_aval(policy_id=policy_id, env_attribute_id=offset+j, env_val='env_val'+str(j))
			db.session.add(policy_env_aval)
	db.session.commit()
	print('rules insertion done')

def delete_users(num_users, num_user_aval):
	offset = 100 # ids start from offset
	for i in range(num_users):
		user_id = offset + i
		User.query.filter_by(user_id=user_id).delete()
		for j in range(num_user_aval):
			User_details.query.filter_by(user_id=user_id,user_attribute_id=offset + j,user_val='userval'+str(j)).delete()
	db.session.commit()
	print('users deletion done')
def delete_resources(num_resources, num_resource_aval):
	offset = 100 # ids start from offset
	for i in range(num_resources):
		resource_id = offset + i
		Resource.query.filter_by(resource_id=resource_id, resource_name='resource_name'+str(resource_id)).delete()
		for j in range(num_resource_aval):
			Resource_details.query.filter_by(resource_id=resource_id, resource_attribute_id=offset + j,resource_val='resource_val'+str(j)).delete()
	db.session.commit()
	print('resources deletion done')
def delete_rules(num_rules, num_rule_aval):
	offset = 100 # ids start from offset
	for i in range(num_rules):
		policy_id = offset + i
		Policy.query.filter_by(policy_id=policy_id, operation_id=5).delete()
		for j in range(num_rule_aval):
			Policy_user_aval.query.filter_by(policy_id=policy_id, user_attribute_id=offset+j, user_val='user_val'+str(j)).delete()
			Policy_resource_aval.query.filter_by(policy_id=policy_id, resource_attribute_id=offset+j, resource_val='resource_val'+str(j)).delete()
			Policy_env_aval.query.filter_by(policy_id=policy_id, env_attribute_id=offset+j, env_val='env_val'+str(j)).delete()
	db.session.commit()
	print('rules deletion done')

def run_graph_example(max_distance):
	user_details = [[]]
	runQuery = SparqlQueries()
	detail_list = []
	user_aval_list = []
	for line in ['Department:School', 'Designation:Dean'] : # decrypted_data.split('\n'):
		attr_name, val = line.split(':')
		attr_name_list = runQuery.distance_search2(attr_name, 0)	# list cant be key of dict
		attr_id_list = []
		for elem in attr_name_list:
			id = User_attributes.query.filter_by(user_attribute=elem).first()
			if id is not None:
				attr_id_list.append(id.user_attribute_id)
		attr_id_list = tuple(attr_id_list)
		# val_list = runQuery.ancestor_search(val)
		val_list = list(set(runQuery.ancestor_search(val) + \
							runQuery.descendant_search(val) + \
							runQuery.distance_search2(val, max_distance)))
		user_aval_list.append({ 'user_attribute_id': attr_id_list, 'user_val': val_list })
		# print('user aval = ');print({ 'user_attributes': attr_name_list, 'user_attribute_id': attr_id_list, 'user_val': val_list });

	resource_id = 5 #Mechanics.pdf
	resource = Resource.query.filter_by(resource_id=resource_id).first()
	resource_details = Resource_details.query.filter_by(resource_id=resource_id).all()

	allowed_operations = dict()		# operation_id : operation_name

	policies = Policy.query.join(Operations, Operations.operation_id==Policy.operation_id) \
				.with_entities(Policy.policy_id, Operations.operation_id, Operations.operation_name).all()
	# for policy in policies:
	# 	print('policy = ', end=' ');	print(policy);
	for policy in policies:
		policy_user_aval_list = Policy_user_aval.query.filter_by(policy_id=policy.policy_id).all()
		policy_resource_aval_list = Policy_resource_aval.query.filter_by(policy_id=policy.policy_id).all()
		policy_env_aval_list = Policy_env_aval.query.filter_by(policy_id=policy.policy_id).all()
		user_aval_valid = 0
		resource_aval_valid = 0
		env_aval_valid = 0
		for policy_aval in policy_user_aval_list:
			match = 0
			for aval in user_aval_list:
				# print('policy_aval.user_val = ' + policy_aval.user_val + 'aval[\'user_val\'] = ',end=' ')
				# print(aval['user_val'])
				if policy_aval.user_val in aval['user_val']: #and policy_aval.user_attribute_id in aval['user_attribute_id'] 
					match += 1
			if match > 0:
				user_aval_valid += 1
			# print('policy_aval = ',end=''); print(policy_aval); print('match = ' + str(match));
		for policy_aval in policy_resource_aval_list:
			match = 0
			for aval in resource_details:
				if aval.resource_attribute_id==policy_aval.resource_attribute_id and aval.resource_val==policy_aval.resource_val:
					match += 1
			if match > 0:
				resource_aval_valid += 1
		for policy_aval in policy_env_aval_list:
			required = bool(int(policy_aval.env_val))
			match policy_aval.env_attribute_id:
				case 1:
					env_aval_valid += (1 if not required or now.weekday() < 5 else 0)
				case 2:
					env_aval_valid += (1 if not required or (now.weekday() < 5 and now.hour >= 8 and now.hour < 17) else 0)
				case 3:
					env_aval_valid += (1 if not required else 0)

		if 	user_aval_valid == len(policy_user_aval_list) and \
				resource_aval_valid == len(policy_resource_aval_list) and \
					env_aval_valid == len(policy_env_aval_list):
			allowed_operations[policy.operation_id] = policy.operation_name

@app.route('/graph/<int:max_distance>/<int:num_users>/<int:num_user_aval>/<int:num_resources>/<int:num_resource_aval>/<int:num_rules>/<int:num_rule_aval>', methods=['GET', 'POST'])
def graph(max_distance, num_users, num_user_aval, num_resources, num_resource_aval, num_rules, num_rule_aval):
	# offset = 100 # ids start from offset
	# adding dummy data in database
	# insert_users(num_users, num_user_aval)
	# insert_resources(num_resources, num_resource_aval)
	# insert_rules(num_rules, num_rule_aval)

	start_time = datetime.datetime.now()

	# evaluating non_user based access request
	run_graph_example(max_distance)

	end_time = datetime.datetime.now()
	execution_time = (end_time - start_time)#.microseconds / 1000000.0

	# # removing dummy data from database
	delete_users(num_users, num_user_aval)
	delete_resources(num_resources, num_resource_aval)
	delete_rules(num_rules, num_rule_aval)

	message = str(execution_time) + 's'
	return message


@app.route('/view_resources')
@login_required
def view_resources():
	# if not current_user.is_authenticated:
	# 	return redirect(url_for('login'))
	resources = Resource.query.all()
	return render_template('view_resources.html', resources=resources)

@app.route('/view_profile')
@login_required
def view_profile():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	user_id  = session['user_id']
	user = User.query.filter_by(user_id=user_id).first()
	user_details = User_details.query \
					.filter_by(user_id=user_id) \
					.join(User_attributes, User_attributes.user_attribute_id == User_details.user_attribute_id) \
					.add_columns(User_details.user_id, User_details.user_attribute_id,  \
								 User_attributes.user_attribute, User_details.user_val).all()
	# print(user_details.keys())
	print(user_details)
	return render_template('view_profile.html', user = user, user_details=user_details)

@app.route('/logout')
def logout():
	logout_user()
	session.pop('user_id',None)
	session.pop('org_id',None)
	session.pop('user_type',None)
	return redirect(url_for('login'))


	# page = request.args.get('page',1,type=int)
	# # User = Users.query.filter_by(user_id=session['user_id']).first()
	# item_list = None
	# form = SearchForm()
	# if request.method == 'POST':
	# 	if form.category.data == "Brand":
	# 		item_list = Item.query.join(Itemcity,Itemcity.item_id==Item.item_id)\
	# 		.add_columns(Item.item_id,Item.name,Item.category,Item.brand,Item.price,\
	# 			Itemcity.quantity,Itemcity.city_id,Item.totalsold)\
	# 		.filter(and_(func.lower(Item.brand)==func.lower(form.search_text.data),Itemcity.city_id==city))\
	# 			.order_by(Item.totalsold.desc())\
	# 			.paginate(page=page,per_page=200)
	# 		return render_template('User_home.html',title='home',form=form,item_list=item_list)


# @app.route('/manager_home',methods = ['GET','POST'])
# @login_required
# def manager_home():
# 	if(session['user_type']!='Manager'):
# 		abort(403)
# 	curr_manager= Manager.query.filter_by(manager_id = session['userid']).first()
# 	brand = curr_manager.brand
# 	page = request.args.get('page',1,type = int)
# 	item_list = Item.query.filter_by(brand = brand).paginate(page = page,per_page = 20)
# 	return render_template('manager_home.html',title = 'home',item_list = item_list,brand =brand)

# @app.route('/manager_add_item',methods = ['GET','POST'])
# @login_required
# def manager_add_item():
# 	if(session['user_type']!='Manager'):
# 		abort(403)
# 	form=ItemaddForm()
# 	if form.validate_on_submit():
# 		curr_manager= Manager.query.filter_by(manager_id = session['userid']).first()
# 		brand = curr_manager.brand
# 		item = Item(name=form.name.data, category=form.category.data, 
# 						description=form.description.data, price=form.price.data,brand = brand,totalsold=0,quantity=0)
# 		count=db.session.query(func.count('*')).select_from(Item).scalar()
# 		item.item_id=count+1
# 		db.session.add(item)
# 		Citylist = City.query.all()
# 		for city in Citylist:
# 			itemcity = Itemcity(item_id=item.item_id,city_id=city.city_id,quantity=0)
# 			db.session.add(itemcity)
# 		db.session.commit()
# 		return redirect(url_for('manager_home'))
# 	return render_template('manager_add_item.html', title='Add Item', form=form)

# @app.route('/manager/<int:item_id>')
# @login_required
# def manager_item(item_id):
# 	if(session['user_type']!='Manager'):
# 		abort(403)
# 	item = Item.query.filter_by(item_id = item_id).first_or_404();
# 	itemcity = Itemcity.query.join(City,City.city_id==Itemcity.city_id)\
# 					.add_columns(Itemcity.city_id,Itemcity.quantity,City.city_name)\
# 					.order_by(Itemcity.quantity.desc())\
# 					.filter(Itemcity.item_id == item_id)
# 	return render_template('manager_view_item.html',title ='View Item',item=item,itemcity = itemcity)

# @app.route('/manager/<int:item_id>/<string:city_id>',methods=['GET','POST'])
# @login_required
# def quantity_change(item_id,city_id):
# 	if(session['user_type']!='Manager'):
# 		abort(403)
# 	curr_manager=Manager.query.filter_by(manager_id = session['userid']).first()
# 	item = Item.query.filter_by(item_id = item_id).first()
# 	if(curr_manager.brand != item.brand):
# 		flash("Invalid Access",'danger')
# 		return redirect(url_for(manager_home))
# 	form = Changequantityform();
# 	if form.validate_on_submit():
# 		itemcity = Itemcity.query.filter_by(item_id=item_id,city_id=city_id).first()
# 		itemcity.quantity +=form.Quantity.data
# 		item.quantity +=form.Quantity.data
# 		db.session.commit()
# 		return redirect("/manager_home")
# 	return render_template("add_quantity.html",item=item,city_id=city_id,form=form)



# @app.route('/view_profile')
# @login_required
# def view_profile():
# 	if not current_user.is_authenticated:
# 		return redirect(url_for('login'))
# 	user_type = session['user_type']
# 	username  = session['username']
# 	if user_type == "User":
# 		user = User.query.filter_by(username=username).first()
# 	elif user_type == "Manager":
# 		user = Manager.query.filter_by(username=username).first()
# 	elif user_type == "Delivery_agent":
# 		user = Delivery_agent.query.filter_by(username=username).first() 
# 	return render_template('view_profile.html', user = user, user_type = user_type)

# @app.route('/register_User', methods=['GET', 'POST'])
# def register_User():
# 	city=City.query.all()
# 	if current_user.is_authenticated:
# 		if session['user_type'] == "User":
# 			return redirect(url_for('User_home'))
# 		elif session['user_type'] == "Manager":
# 			return redirect(url_for('manager_home'))
# 		else:
# 			return redirect(url_for('agent_home'))
# 	form=User_Registration_Form()
# 	if form.validate_on_submit():
# 		# cid, username, email, password_hash, address, city_id, phone_no
# 		user = User(username=form.username.data, email=form.email.data, 
# 						address=form.address.data, city_id=form.city_id.data, phone_no=form.phone_no.data)
# 		user.set_password(form.password.data)
# 		count=db.session.query(func.count('*')).select_from(User).scalar()
# 		user.cid=count+1
# 		db.session.add(user)
# 		db.session.commit()
# 		flash('Congratulations, you are now a registered User!','success')
# 		return redirect(url_for('login'))
# 	return render_template('register.html', title='Register', form=form,city_list=city)

# @app.route('/register_manager', methods=['GET', 'POST'])
# def register_manager():
# 	if current_user.is_authenticated:
# 		if session['user_type'] == "User":
# 			return redirect(url_for('User_home'))
# 		elif session['user_type'] == "Manager":
# 			return redirect(url_for('manager_home'))
# 		else:
# 			return redirect(url_for('agent_home'))
# 	form=Manager_Registration_Form()
# 	if form.validate_on_submit():
# 		# cid, username, email, password_hash, brand
# 		user = Manager(username=form.username.data, email=form.email.data, brand=form.brand.data)
# 		user.set_password(form.password.data)
# 		count=db.session.query(func.count('*')).select_from(Manager).scalar()
# 		user.manager_id=count+1
# 		db.session.add(user)
# 		db.session.commit()
# 		flash('Congratulations, you are now a registered manager!','success')
# 		return redirect(url_for('login'))
# 	return render_template('register.html', title='Register', form=form)

# @app.route('/register_agent', methods=['GET', 'POST'])
# def register_agent():
# 	city=City.query.all()
# 	if current_user.is_authenticated:
# 		if session['user_type'] == "User":
# 			return redirect(url_for('User_home'))
# 		elif session['user_type'] == "Manager":
# 			return redirect(url_for('manager_home'))
# 		else:
# 			return redirect(url_for('agent_home'))
# 	form=Agent_Registration_Form()
# 	if form.validate_on_submit():
# 		# cid, username, email, password_hash, city_id
# 		user = Delivery_agent(username=form.username.data, email=form.email.data, city_id=form.city_id.data)
# 		user.set_password(form.password.data)
# 		count=db.session.query(func.count('*')).select_from(Delivery_agent).scalar()
# 		user.agent_id=count+1
# 		user.pending_deliveries=0
# 		db.session.add(user)
# 		db.session.commit()
# 		flash('Congratulations, you are now a registered delivery agent!','success')
# 		return redirect(url_for('login'))
# 	return render_template('register.html', title='Register', form=form,city_list=city)

# @app.route('/view_cart')
# @login_required
# def view_cart():
#     if(session['user_type']!='User'):
#         abort(403)
#     cart_list=Cart.query.join(Item,Cart.item_id==Item.item_id)\
#         .add_columns(Item.item_id,Item.name,Item.brand,Cart.quantity,Item.price)\
#             .filter(Cart.cid==session['userid'])
#     x=0
#     for cart in cart_list:
#     	x=1
#     return render_template('view_cart.html',title='Cart',cart=cart_list,x=x)

# def place_order(cart_list):
#     x=User.query.filter(User.cid==session['userid']).first()
#     city = x.city_id
#     order_id=db.session.query(func.count('*')).select_from(Order).scalar()
#     order_id+=1
#     min_count=db.session.query(func.min(Delivery_agent.pending_deliveries))\
#     		.filter(Delivery_agent.city_id == city).scalar()
#     print(min_count)
#     agent=Delivery_agent.query.\
# 	    filter(and_(Delivery_agent.pending_deliveries==min_count,\
# 	    	Delivery_agent.city_id == city)).first()
#     amount=0

#     for y in cart_list: 
#         z=Itemcity.query.filter(and_(Itemcity.city_id==x.city_id,Itemcity.item_id==y.item_id)).first()
#         item=Item.query.filter_by(item_id=y.item_id).first()
#         z.quantity-=y.quantity
#         item.quantity-=y.quantity
#         item.totalsold+=y.quantity
#         amount+=y.price*y.quantity
#         db.session.commit()
#         order_item=Contains(order_id=order_id,item_id=y.item_id,quantity=y.quantity)
#         db.session.add(order_item)
#         db.session.commit()

	
#     order1=Order(order_id=order_id,cid=session['userid'],amount=amount,status='DELIVERING',\
#         time_of_delivery=None,agent_id=agent.agent_id)
#     db.session.add(order1)
#     db.session.commit()
#     agent.pending_deliveries+=1
#     db.session.commit()
	

# @app.route('/checkout', methods=['GET','POST'])
# @login_required
# def checkout():
# 	if(session['user_type']!='User'):
# 		abort(403)
# 	amount=0
# 	form=CheckoutForm()
# 	cart_list=Cart.query.join(Item,Cart.item_id==Item.item_id)\
# 		.filter(Cart.cid==session['userid'])\
# 		.add_columns(Item.item_id,Item.name,Item.brand,Cart.quantity,Item.price)
# 	for x in cart_list:
# 		amount+=x.quantity*x.price
# 	if form.validate_on_submit():
# 		place_order(cart_list)
# 		a=Cart.query.filter(Cart.cid==session['userid'])
# 		for ab in a:
# 			db.session.delete(ab)
# 		db.session.commit()
# 		flash('Your order has been placed successfully','success')
# 		return redirect(url_for('User_home'))
# 	return render_template('checkout.html',title='Checkout',cart=cart_list,amount=amount,form =form)


# @app.route("/view_item/<int:item_id>")
# @login_required
# def view_item(item_id):
# 	if(session['user_type']!='User'):
# 		abort(403)
# 	item=Item.query.get_or_404(item_id)
# 	x=Cart.query.filter(and_(Cart.cid==session['userid'],Cart.item_id==item.item_id)).first()
# 	count=0
# 	if x is not None:
# 		count=x.quantity
# 	return render_template('view_item.html',item=item,count=count)

# @app.route("/cart_add/<int:item_id>/<int:count>")
# @login_required
# def cart_add(item_id,count):
# 	if(session['user_type']!='User'):
# 		abort(403)
# 	item=Item.query.get_or_404(item_id)
# 	if count>0:
# 		cart_item=Cart.query.filter(and_(Cart.cid==session['userid'],Cart.item_id==item_id)).first()
# 		cart_item.quantity+=1
# 		db.session.commit()
# 	else:
# 		x=Cart(cid=session['userid'],item_id=item.item_id,quantity=1)
# 		db.session.add(x)
# 		db.session.commit()
# 	return redirect(url_for('view_item',item_id=item_id))

# @app.route("/cart_remove/<int:item_id>/<int:count>")
# @login_required
# def cart_remove(item_id,count):
# 	if(session['user_type']!='User'):
# 		abort(403)
# 	item=Item.query.get_or_404(item_id)
# 	cart_item=Cart.query.filter(and_(Cart.cid==session['userid'],Cart.item_id==item_id)).first()
# 	if count>1:
# 		cart_item.quantity-=1
# 		db.session.commit()
# 	else:
# 		db.session.delete(cart_item)
# 		db.session.commit()
# 	return redirect(url_for('view_item',item_id=item_id))

# @app.route('/agent_home',methods = ['GET','POST'])
# @login_required
# def agent_home():
# 	if(session['user_type']!='Delivery_agent'):
# 		abort(403)
# 	orders =  Order.query.filter_by(agent_id = session['userid']).all()
# 	pending_orders = []
# 	completed_orders = []
# 	for order_object in orders:
# 		if order_object.status == 'DELIVERING':
# 			pending_orders.append(order_object)
# 		else:
# 			completed_orders.append(order_object)
# 	return render_template('agent_home.html',title = 'home', \
# 							pending_orders = pending_orders, completed_orders = completed_orders)

# @app.route('/view_order/<int:order_id>')
# @login_required
# def view_order(order_id):
# 	if not (session['user_type']=='User' or session['user_type']=='Delivery_agent'):
# 		abort(403)
# 	order_object =  Order.query.filter_by(order_id=order_id).first()
# 	order = {}
# 	order['order_id'] = order_object.order_id
# 	order['User_name'] = User.query.filter_by(cid=order_object.cid).first().username
# 	order['amount'] = order_object.amount
# 	order['status'] = order_object.status
# 	order['time_of_order'] = order_object.time_of_order
# 	order['time_of_delivery'] = order_object.time_of_delivery
# 	order['agent_name'] = Delivery_agent.query.filter_by(agent_id=order_object.agent_id).first().username
# 	order['contains'] = Contains.query.join(Item,Item.item_id==Contains.item_id)\
# 		.filter(Contains.order_id==order_id)\
# 			.add_columns(Item.name,Contains.quantity,Item.brand,Item.price)
# 	print(type(order['contains']), file=sys.stderr)
# 	return render_template('view_order.html',order=order)

# @app.route('/User_orders')
# def User_orders():
# 	if not current_user.is_authenticated:
# 		return redirect(url_for('login'))
# 	if(session['user_type']!='User'):
# 		abort(403)
# 	username  = session['username']
# 	cid = session['userid']
# 	# print(Order.query.filter_by(cid=cid).all(), file=sys.stderr)
# 	orders =  Order.query.join(Delivery_agent,Order.agent_id==Delivery_agent.agent_id)\
# 				.filter(Order.cid==cid)\
# 				.add_columns(Order.order_id,Order.amount,Order.time_of_order,\
# 					Order.time_of_delivery,Delivery_agent.username,Order.status,Order.cid)
# 	pending_orders = []
# 	completed_orders = []
# 	for order_object in orders:
# 		if order_object.status == 'DELIVERING':
# 			pending_orders.append(order_object)
# 		else:
# 			completed_orders.append(order_object)
# 	return render_template('User_orders.html', pending_orders = pending_orders, completed_orders = completed_orders)

# @app.route('/mark_order_delivered/<int:order_id>')
# @login_required
# def mark_order_delivered(order_id):
# 	if(session['user_type']!='Delivery_agent'):
# 		abort(403)
# 	order = Order.query.filter_by(order_id = order_id).first()
# 	agent_id1=order.agent_id
# 	agent = Delivery_agent.query.filter_by(agent_id=agent_id1).first()
# 	if order.status == 'COMPLETE':
# 		flash('Order id = ' + str(order_id) + ' is already delivered !!', 'danger')
# 	elif order.status == 'DELIVERING':
# 		order.status = 'COMPLETE'
# 		order.time_of_delivery = datetime.utcnow()
# 		agent.pending_deliveries-=1
# 		db.session.commit()
# 		flash('Order id = ' + str(order_id) + ' marked as DELIVERED ', 'success')
# 	return redirect(url_for('agent_home'))
