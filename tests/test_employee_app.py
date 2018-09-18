import os
import tempfile

import pytest

from employee_app import employee_app


@pytest.fixture
def client():
	db_fd, employee_app.app.config['DATABASE'] = tempfile.mkstemp()
	employee_app.app.config['TESTING'] = True
	client = employee_app.app.test_client()

	with employee_app.app.app_context():
		employee_app.init_db()

	yield client

	os.close(db_fd)
	os.unlink(employee_app.app.config['DATABASE'])



# '/' Homepage Tests (not logged in)

# Test that the home page returns with no error codes
def test_home_logged_out_status_code(client):
	rv = client.get('/')
	assert rv.status_code == 200

# Test that the welcome message appears on the home page
def test_home_logged_out_welcome_message(client):
	rv = client.get('/')
	assert b'Welcome to the Employee Manager! To get started, login and add or edit some employees or register with us today!' in rv.data

# Test that the register button appears on the home page
def test_home_logged_out_register_button(client):
	rv = client.get('/')
	assert b'Register Today' in rv.data

# Test that the login button appears on the home page
def test_home_logged_out_login_button(client):
	rv = client.get('/')
	assert b'Login' in rv.data

# Test that the Employee Manager logo text appears on the home page in the navbar
def test_home_logged_out_navbar_logo(client):
	rv = client.get('/')
	assert b'Employee Manager' in rv.data

# Test that the Home page button appears on the home page in the navbar
def test_home_logged_out_navbar_home(client):
	rv = client.get('/')
	assert b'Home' in rv.data

# Test that the Login page button appears on the home page in the navbar
def test_home_logged_out_navbar_login(client):
	rv = client.get('/')
	assert b'Login' in rv.data

# Test that the Register page button appears on the home page in the navbar
def test_home_logged_out_navbar_register(client):
	rv = client.get('/')
	assert b'Login' in rv.data



# Homepage tests (logged in)

# Test that the home page returns with no error codes
#def test_home_logged_in_status_code(client):
	



# Test Login and Logout Functionality

# define login and logout functions that use the client fixture
def login(client, username, password):
	return client.post('/login', data=dict(
		username=username,
		password=password
	), follow_redirects=True)

def logout(client):
	return client.get('/logout', follow_redirects=True)



# run tests using the above functions
"""
def test_login_logout(client):
	rv = login(client, 'testuser@gmail.com', 'default')
	assert b'You were logged in' in rv.data

	rv = logout(client)
	assert b"You were logged out" in rv.data
"""

"""
	rv = login(client, 'notauser@gmail.com', )
	assert b'Invalid username' in rv.data

	rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
	assert b'Invalid password' in rv.data
"""



