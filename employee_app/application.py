import os
import sqlite3

# Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# WTForms imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField
from wtforms.validators import Length, Email, InputRequired, EqualTo

# sha_256 encryption import
from passlib.hash import sha256_crypt


# Create app instance and load configurations (from this file)
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , employee_app.py

# Load default config and override config from an environment variable
app.config.update(
	DATABASE=os.path.join(app.root_path, 'employee_app.db'),
	SECRET_KEY=b'\xf4\x9a\xf3\xcfRR\x85\xf0\x1a\x15\xdb\xa6j|\xa3\xebIyG\x92\xb4\x1b\x07\xcb',# secret key I generated
)

# Optional config file environment variable setting
#app.config.from_envvar('PAYLOCITY_APP_SETTINGS', silent=True)


# VIEW FUNCTIONS:

#-------
# HOME |
#-------

# Default home page (index.html) shows employees if logged in or message otherwise
@app.route('/')
def index():
	db = get_db()
	cur = db.execute('SELECT employee_id, lname, fname, minit, email, salary, dependents, dependentsA \
		FROM employees WHERE company_id=? ORDER BY lname ASC', [session.get('company_id')]) 
	employees = cur.fetchall()
	return render_template('index.html', employees=employees)


#----------------
# REGISTER USER |
#----------------

# Form for new users to register
class RegisterForm(FlaskForm):
	fname = StringField('First Name', validators=[InputRequired()])

	lname = StringField('Last Name', validators=[InputRequired()])
	
	email = StringField('Email', validators=[\
		InputRequired(), \
		Email(message="Must provide a valid email address"), \
		EqualTo('confirm_email', message='Emails do not match')])
	
	confirm_email = StringField('Repeat Email', validators=[InputRequired()])

	password = PasswordField('Password', validators=[\
		InputRequired(), \
		EqualTo('confirm_password', message='Passwords must match')])

	confirm_password  = PasswordField('Repeat Password', validators=[InputRequired()])

	company_id  = IntegerField('Company ID', validators=[InputRequired()])

# Registers a user once the information is valid as long as a user with that email doesn't already exist. Redirects to home page and sets session variables
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	error = None

	if form.validate_on_submit():
		db = get_db()
		cur = db.execute('SELECT email FROM users WHERE email=?', [request.form['email']])
		rv = cur.fetchone()
		
		if rv != None:
			error = 'An account with this email already exists'
		else:
			session['logged_in'] = True
			session['company_id'] = request.form['company_id']
			session['name'] = request.form['fname'] + " " + request.form['lname']
			db.execute('INSERT INTO users (fname, lname, email, password, company_id) VALUES (?, ?, ?, ?, ?)', \
				[request.form['fname'], request.form['lname'], request.form['email'], sha256_crypt.encrypt(request.form['password']), \
				int(request.form['company_id'])])
			db.commit()
			flash('You have successfully registered!')
			return redirect(url_for('index'))

	return render_template('register.html', form=form, error=error)

# Temporary route so that I can see all of the regstered users in order to see that they're being added correctly
@app.route('/users')
def users():
	if not session.get('logged_in'):
		return redirect(url_for('index'))
	db = get_db()
	cur = db.execute('SELECT id, email, password, company_id FROM users')
	rv = cur.fetchall()
	return render_template('users.html', rv=rv)

	
#--------
# LOGIN |
#--------

# Form for existing users to login
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[\
		InputRequired(), \
		Email(message="Must provide a valid email address")])

	password = PasswordField('Password', validators=[InputRequired()])

# Login page. Redirects users to index.html if they login successfully and sets session variables
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm()

	if form.validate_on_submit():
		db = get_db()
		cur = db.execute('SELECT * FROM users WHERE email=?', [request.form['email']])
		rv = cur.fetchone()
		if rv == None:
			error = 'There is no user profile under this email'
		elif sha256_crypt.verify(request.form['password'], rv['password']) != True:
			error = 'Incorrect password'	
		else:
			session['logged_in'] = True
			session['company_id'] = rv['company_id']
			session['name'] = rv['fname'] + " " + rv['lname']
			flash('You were logged in')
			return redirect(url_for('index'))

	return render_template('login.html', form=form, error=error)


#---------
# LOGOUT |
#---------

# Logout function. returns the home page (index.html) but with a flash message telling you you logged out and destroys session variables
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('company_id', None)
	session.pop('name', None)
	flash('You were logged out')
	return redirect(url_for('index'))


#------------------
# EMPLOYEE OBJECT |
#------------------

class Employee():
	employee_id = ""
	fname = ""
	lname = ""
	minit = ""
	email = ""
	salary = 0.0
	dependents = 0
	dependentsA = 0
	
	def __init__(self, employee_id, fname, lname, minit, email, salary, dependents, dependentsA):
		self.employee_id = employee_id
		self.fname = fname
		self.lname = lname
		self.minit = minit
		self.email = email
		self.salary = salary
		self.dependents = dependents
		self.dependentsA = dependentsA
	
	# Getters
	def get_employee_id(self):
		return self.employee_id
	
	def get_fname(self):
		return self.fname
	
	def get_lname(self):
		return self.lname
	
	def get_minit(self):
		return self.minit
	
	def get_email(self):
		return self.email
	
	def get_salary(self):
		return self.salary
	
	def get_dependents(self):
		return self.dependents
	
	def get_dependentsA(self):
		return self.dependentsA
	
	# Setters
	def set_employee_id(self, employee_id):
		self.employee_id = employee_id
	
	def set_fname(self, fname):
		self.fname = fname
	
	def set_lname(self, lname):
		self.lname = lname
	
	def set_minit(self, minit):
		self.minit = minit
	
	def set_email(self, email):
		self.email = email
	
	def set_salary(self, salary):
		self.salary = salary
	
	def set_dependents(self, dependents):
		self.dependents = dependents
	
	def set_dependentsA(self, dependentsA):
		self.dependentsA = dependentsA


#----------------
# EMPLOYEE FORM |
#----------------

class EmployeeForm(FlaskForm):
	employee = None

	# "Constructor" with default arguments
	def __init__(self, employee=None):
		self.employee = employee
	
	employee_id = StringField('Employee ID', validators=[\
		InputRequired(), \
		Length(min=10, max=10)])

	fname = StringField('First Name', validators=[InputRequired()])

	lname = StringField('Last Name', validators=[InputRequired()])

	minit = StringField('Middle Initial', validators=[Length(min=0, max=1, message="Middle initial must be one letter")])

	email = StringField('Email', validators=[\
		InputRequired(), \
		Email(message="Must provide a valid email address")])

	salary = DecimalField('Salary', places=2, rounding=None, use_locale=False, number_format=None, validators=[InputRequired()])
	
	dependents = IntegerField('Total Number of Dependents', validators=[InputRequired()])
	
	dependentsA = IntegerField('Number of \'A\' Dependents', validators=[InputRequired()])
	

#---------------
# ADD EMPLOYEE |
#---------------

# If logged in, this is the page to add employees. Redirects to the home page (index.html) if the user is not logged in
@app.route('/add', methods=['GET', 'POST'])
def add():
	if not session.get('logged_in'):
		return redirect(url_for('index'))

	form = EmployeeForm()
	error = None

	if form.validate_on_submit():
		db = get_db()
		cur = db.execute('SELECT employee_id, company_id FROM employees WHERE employee_id=? AND company_id=?', \
			[request.form['employee_id'], session.get('company_id')])
		rv = cur.fetchone()

		if rv != None:
			error = 'An employee with that employee ID already exists'
		else:
			db.execute('insert into employees (employee_id, lname, fname, minit, email, salary, dependents, dependentsA, company_id) \
				values (?, ?, ?, ?, ?, ?, ?, ?, ?)', [int(request.form['employee_id']), request.form['lname'], \
				request.form['fname'], request.form['minit'], request.form['email'], float(request.form['salary']), \
				int(request.form['dependents']), int(request.form['dependentsA']), session.get('company_id')])
			db.commit()
			flash('New employee was successfully created')
			return redirect(url_for('index'))

	return render_template('add.html', form=form, error=error)


#----------------
# EDIT EMPLOYEE |
#----------------
'''
@app.route('/edit', methods=['GET', 'POST'])
def edit():
	if not session.get('logged_in'):
		return redirect(url_for('index'))
	
	form = EditForm()
'''


# If logged in, this is the page to edit employees. Redirects to the home page (index.html) if the user is not logged in
@app.route('/edit/<employee_id>', methods=['GET'])
def edit(employee_id):
	if not session.get('logged_in'):
		return redirect(url_for('index'))
	
	db = get_db()
	cur = db.execute('SELECT id, employee_id, lname, fname, minit, email, salary, dependents, dependentsA, company_id \
		FROM employees WHERE employee_id=? AND company_id=?', [employee_id, session.get('company_id')])
	
	rv = cur.fetchone()

	if rv == None:
		return redirect(url_for('index'))
	
	return render_template('edit.html', rv=rv)

# This is the redirect from the /edit page that performs the edit logic if logged in. Users cannot access this page
@app.route('/edit_employee/<id>', methods=['POST'])#given, works but just pops up a "you are not allowed" page
def edit_employee(id):
	if not session.get('logged_in'):
		abort(401)

	db = get_db()
	db.execute('UPDATE employees SET employee_id=?, lname=?, fname=?, minit=?, email=?, salary=?, dependents=?, dependentsA=? WHERE id=?', \
		[request.form['employee_id'], request.form['lname'], request.form['fname'], request.form['minit'], request.form['email'], \
		request.form['salary'], request.form['dependents'], request.form['dependentsA'], id])
	
	db.commit()
	name = request.form['fname'] + " " + request.form['minit'] + ". " + request.form['lname']
	flash('Employee %s was successfully updated' % name)
	return redirect(url_for('index'))


#----------------
# VIEW EMPLOYEE |
#----------------

# Route to view a particular employee
@app.route('/employee/<employee_id>')
def employee(employee_id):
	if not session.get('logged_in'):
		return redirect(url_for('index'))
	db = get_db()
	cur = db.execute('SELECT employee_id, lname, fname, minit, email, salary, dependents, dependentsA, company_id \
		FROM employees WHERE employee_id=? AND company_id=?', [employee_id, session.get('company_id')])
	rv = cur.fetchone()
	if rv == None:
		return redirect(url_for('index'))
	return render_template('employee.html', rv=rv)


#------------------
# DELETE EMPLOYEE |
#------------------

@app.route('/delete/<employee_id>', methods=['GET'])
def delete(employee_id):
	if not session.get('logged_in'):
		return redirect(url_for('index'))
	
	db = get_db()
	cur = db.execute('SELECT id, employee_id, lname, fname, minit, email, salary, dependents, dependentsA \
		FROM employees WHERE employee_id=? AND company_id=?', [employee_id, session.get('company_id')])
	rv = cur.fetchone()
	return render_template('delete.html', rv=rv)

@app.route('/delete_employee/<id>', methods=['GET'])
def delete_employee(id):
	if not session.get('logged_in'):
		abort(401)

	db = get_db()
	
	# Get the user's name information before deletion
	cur = db.execute('SELECT lname, fname, minit FROM employees WHERE id=?', [id])
	rv = cur.fetchone()

	# Delete the user
	db.execute('DELETE FROM employees WHERE id=?', [id])
	db.commit()
	
	# Print the success message to the screen
	fname = rv['fname']
	minit = rv['minit']
	lname = rv['lname']
	name = fname + " " + minit + ". " + lname
	flash('Employee %s was successfully deleted' % name)
	return redirect(url_for('index'))


#-----------
# DATABASE |
#-----------
# NOTE: database can be initialized now by running "flask initdb" from within the root directory of this project
def connect_db():
	"""Connects to the specific database."""

	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()

	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())

	db.commit()

# cli.command allows us to add command-line arguments to flask
@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database."""

	init_db()
	print('Initialized the database.')


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()



