from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, RadioField,DecimalField
from wtforms.validators import DataRequired,EqualTo,Length,Email,ValidationError, NumberRange
from app.models import *


# class ContactForm(Form):
#   name = StringField("Name",  [InputRequired("Please enter your name.")])
#   email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
#   subject = StringField("Subject",  [InputRequired("Please enter a subject.")])
#   message = TextAreaField("Message",  [InputRequired("Not including a message would be stupid")])
#   submit = SubmitField("Send")

class AddAttributeForm(FlaskForm):
	attr_type = StringField('Attribute type (user/resource/env)', validators=[ DataRequired() ])
	attribute = StringField('Attribute name', validators=[ DataRequired(), Length(max=64) ])
	submit = SubmitField('Add Attribute')

class AddAvalForm(FlaskForm):
	attr_type = StringField('Attribute type (user/resource/env)', validators=[ DataRequired() ])
	attribute = StringField('Attribute name', validators=[ DataRequired(), Length(max=64) ])
	val = StringField('Value', validators=[ DataRequired(), Length(max=64) ])
	submit = SubmitField('Add Attr-Val')

	
class AvalForm(FlaskForm):
	attribute_id = IntegerField('Attribute id')
	attribute = StringField('Attribute name', validators=[ DataRequired(), Length(max=64) ])
	val = StringField('Value', validators=[ DataRequired(), Length(max=64) ])
	new_val = StringField('New value',validators=[Length(max=64)],render_kw={"placeholder":"Type to enter new value"})

class LoginForm(FlaskForm):
	login_id = StringField('Login name/Email',validators=[DataRequired(), Length(max=64)])
	pwd = PasswordField('Password',validators=[DataRequired(), Length(max=64)])
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	email   = StringField('Email', validators=[ DataRequired(), Email() ])
	pwd     = PasswordField('Password', validators=[ DataRequired(), Length(max=64) ])
	confirm_pwd = PasswordField('Confirm password', validators=[ DataRequired(), EqualTo('pwd') ])

class User_Registration_Form(RegistrationForm,FlaskForm):
	user_name = StringField('Name', validators=[ DataRequired(), Length(max=64) ])
	login_name = StringField('Login name', validators=[ DataRequired(), Length(max=64) ])
	details = FieldList(FormField(AvalForm), label='User Details (Attr-Val)')#, min_entries=1
	add_aval = SubmitField(label='Add Attr-Val')
	submit_id  = SubmitField('Check for user')
	submit  = SubmitField('Sign Up')

	def validate_login_name(self,login_name):
		user = User.query.filter_by(login_name=login_name.data).first()
		if user is not None:
			raise ValidationError('User login id already exists')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('User email id is already registered')

	# def validate_phone_no(self, phone_no):
	#     if not phone_no.data.isnumeric():
	#         raise ValidationError('Invalid Phone Number')



class AddResourceForm(FlaskForm):
	resource_id = IntegerField('Resource id', validators=[ DataRequired() ])
	resource_name = StringField('Name',validators=[DataRequired(), Length(max=64)])
	details = FieldList(FormField(AvalForm), label='Resource Details (Attr-Val)')
	add_aval = SubmitField(label='Add Attr-Val')
	# policy = FieldList(FormField(AvalForm), label='Resource Details (Attr-Val)')
	# add_policy = SubmitField(label='Add Policy Attr-Val')
	submit_id = SubmitField('Check for resource')
	submit = SubmitField('Add Resource')


class AddPolicyForm(FlaskForm):
	operation_id = IntegerField('Enter operation', validators=[ DataRequired() ])
	user_aval = FieldList(FormField(AvalForm), label='Enter user avals (Attr-Val)')
	add_user_aval = SubmitField(label='Add User Attr-Val')
	resource_aval = FieldList(FormField(AvalForm), label='Enter resource avals (Attr-Val)')
	add_resource_aval = SubmitField(label='Add Resource Attr-Val')
	env_aval = FieldList(FormField(AvalForm), label='Enter env avals (Attr-Val)')
	add_env_aval = SubmitField(label='Add Env Attr-Val')
	submit = SubmitField('Add Policy')

# class AccessResource_UserForm(FlaskForm):
# 	resource_id = IntegerField('Resource name', validators=[ DataRequired() ])
# 	submit  = SubmitField('Check access')

# class AccessResource_NonUserForm(FlaskForm):
# 	resource_id = StringField('Resource name', validators=[ DataRequired() ])
# 	details = FieldList(FormField(AvalForm), label='Your Details (Attr-Val)')
# 	# add_aval = SubmitField(label='Add Attr-Val')
# 	ask_aval = SubmitField(label='Try to access')
# 	submit  = SubmitField('Check access')

# class Org_Registration_Form(RegistrationForm,FlaskForm):
# 	org_id = StringField('Organisation Id', validators=[ DataRequired(), Length(min=6, max=64) ])
# 	org_name = StringField('Organisation name', validators=[ DataRequired(), Length(min=1, max=64) ])
# 	submit = SubmitField('Sign Up', validators=[ DataRequired() ])


# class SearchForm(FlaskForm):
# 	category=RadioField('Search by',default='Product',choices=[('Brand','Brand'),('Product','Product'),('Category','Category')])
# 	search_text=StringField(None,validators=[DataRequired()])
# 	submit=SubmitField('Search') babu