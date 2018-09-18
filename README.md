# Employee Benefits Manager Solution

## Authors

* **Nathan Brinton**

This project is my solution to a simple employee management problem. My solution uses
the Flask web framework to create a web app that multiple companies can create users on
and whose users can then login and add, edit, or delete employees for that company. The
primary feature of the website is to calculate and display the cost of benefits for each 
employee, and thus, once you sign in, the index page is a list of all of the employees
in order. I created this website so that I could teach myself how to use a web framework
by solving a fairly simple problem. In my intro to web development class at BSU, I learned
some of the basics of full stack web development using HTML, CSS, PHP, and MariaDB, but they
didn't teach a lot of stuff including how to use frameworks and how to actually host your
website on a server client.

## Getting Started

Firstly you need to make sure that you have all of the dependencies for this project installed
properly on your system. Currently, this project contains information on how to install and run
this project in a Linux environment, specifically a Debian-based one (Ubuntu 14).

### Project Dependencies

#### Git
The very first dependency for this project is Git. If you do not have git installed, then you 
can, however, choose to simply download the raw source code from the project repository. For 
installing Git on Ubuntu 14, enter:
~~~
	sudo apt-get install git
~~~

After installing Git, clone the repository by entering:
~~~
git clone https://nbrinton@bitbucket.org/nbrinton/employee_management_app.git
~~~

After either cloning or downloading the repository, change into repo by entering:
~~~
cd employee_management_app
~~~

#### Pip (Not sure about this, as it might already be in the virtual environtment) REVISIT THIS!
To build the project, you need to make sure that pip is installed by entering:
~~~
	sudo apt-get install python3-pip
~~~

#### Virtual Environment: virtualenv
This project uses a Python 3.4 virtual environment to run, so you must have the proper version 
of virtualenv installed on your system. To install the proper version of virtualenv on Ubuntu 14,
enter:
~~~
	sudo apt-get install python3.4-venv
~~~

To run the program you must first activate the virtual environment with the command:
~~~
	source employee_venv/bin/activate
~~~

Alternatively, you may also use:
~~~
	. employee_venv/bin/activate
~~~

When you're done using the virtual environment, deactivate it using the command:
~~~
	deactivate
~~~

Do not deactivate the virtual environment until you are completely done running the
program!

Besides Git, virtualenv, and pip, all of the other dependencies should already be installed
within the employee_venv virtual environment. However, you can also optionally install sqlite3 
separately should you choose to perform extra sqlite3 commands outside of the ones built into 
the project in application.py.
~~~
apt-get install sqlite3 (Shouldn't need this due to function within application.py)
~~~

#### Dependencies Residing Within employee_venv
~~~
pip install Flask
pip install pytest
pip install Flask-WTF
pip install passlib
~~~

### Building and Running

To run the program now, all you should have to do is give the shell script "run.sh"
executable privileges and then run it using these two commands:
~~~
	chmod +x run.sh
	./run.sh
~~~

You only need to give run.sh executable privileges one time. After the first time, 
just enter the command:
~~~
	./run.sh
~~~

This should run an instance of the app on the localhost port 5000. Open up a web browser
of your choice and in the url bar enter:
~~~
	localhost:5000
~~~

This will take you to the index page of the website. From here you can use the website
to your liking.

#### Building Manually

If you would like to build everything manually, here is essentially all that the run.sh
shell script is doing:

Since the application is created as a package, you have to install it using pip 
by entering this from within the root directory employee_management_app:
~~~
	pip install --editable .
~~~

Then set the environment variables for the app by entering:
~~~
	export FLASK_APP=employee_app
	export FLASK_DEBUG=true
~~~

Run the app by entering:
~~~
	flask run
~~~

If you get an exception later on stating that a table cannot be found, check that you did 
execute the initdb command and that your table names are correct (singular vs. plural, for example).


### Running the tests

To run the unit tests for this project, run this command from within the root directory:
~~~
	pytest
~~~

Currently there is only one test that runs (and should pass...), but I am currently working
on creating more so that this website can be thoroughly unit-tested to make sure that it is
both stable and robust.

####NOTE: This functionality is currently not in use!!!
Also, by having added a few extra lines to the setup.py and creating setup.cfg, we can run the tests by entering:
~~~
	python setup.py test
~~~


### Using the Built-In Test User to Explore the Website's Fuctionality

This project comes with an already populated database which includes a test user account 
that you can use to login with and personally explore the website's functionality. Here is
the user information:

Username: testuser@gmail.com
Password: default

Simply browse to the login page and enter the above credentials.


### DATABASE USE

This project already has a populated database including a test user that you can use to
play around with the functionality of the website. The main executable file, application.py
includes several build-in commands, utilizing Flask's built-in support for Click that allows
for extension of the Flask CLI (command-line interface).

For documentation on the use of sqlite3, go here: [sqlite3 CLI Documentation](https://www.sqlite.org/cli.html)
Specifically for help quering the database from the command line, go here: [Quering the Database Schema](https://www.sqlite.org/cli.html#querying_the_database_schema)


To view or modify the database from within the terminal, you must make sure that you have 
sqlite3 installed on your computer. To do this on Ubuntu 14, enter:
~~~
	sudo apt-get install sqlite3 -y
~~~

Once you have installed sqlite3, change into the `employee_app` directory from within the
root directory; the database file `employee_app.db` resides here. To perform queries on the
database, run sqlite3 with the database file as an argument like this:
~~~
	sqlite3 employee_app.db
~~~

After doing this you can perform sqlite3 operations on the database and its various tables. Here
are some common commands when usiing sqlite3:

***Run sqlite3 On An Existing Database:***
~~~
	sqlite3 <database file>
~~~

***List the Existing Tables in Your Database:***
~~~
	.tables
~~~

***Basic Select Statement:***
~~~
	SELECT * FROM employees;
~~~

***Clear the Screen:***
Ctrl+L (UNIX-Based OS)

***Quit sqlite3:***
~~~
	.quit
~~~

***Manually Initialize the Database Based On a Given File:***
~~~
	sqlite3 /tmp/employee_app.db < schema.sql
~~~

To initialize the databse through the program, enter (order of commands in order to do this is outlined in: initdb_command_order.png
~~~
	flask initdb
~~~




## FUTURE DEVELOPMENT:

1. "Edit" Functionality
	* WTForms Functionality
		Currently I cannot figure out how to get the edit forms to fill with the old values using wtforms so I'm 
		not using them for this. However, this means that the validators aren't there and that's a security risk.
	* Vulnerability: Editing an employee's ID to one that already exists
		I currently have this check in the add employee as well as in the register code, but I don't have this in 
		the edit code yet. You should only be able to edit the employee whose name you clicked on and not another
		one indirectly.

2. Vulnerability: Company ID and registering a new user
	* Currently anyone can register with any company so long as they know that company's ID number. I would like to
	eventually create some sort of check (be it a password, email verification, what have you) so that you can 
	only create a user account for a company if you have permission to do so. This will likely involve implementing
	the full company table functionality that I currently have commented out and not fully implemented.

3. Create vagrant file for easy setup
	* I would like to create a nice vagrant file for my project so that other people can easily create my development
	environment for viewing or editing purposes.

4. Helper functions
	* I feel like there's quite a bit of duplicate code which is bad practice and just uneccessary. I'm not sure how
	much I'm going to worry about it for now because it fully works and I don't want to mess it up, but it would be
	nice to make my code more robust in this fashion.

5. User Edit page
	* Currently you can only edit employees and not the actual admin users. I would like to add the functionality for
	users to edit their information (albeit the very little amount of information that they can actually modify).

6. Add employees from a csv or other file format 
	* Currently a user has to enter every employee manually. This is a very unlikely scenario and so it would be a nice
	feature for users to be able to add a slew of employees from a selected file (probably csv).

7. Strip strings properly
	* I'm not exactly sure if I do any real string stripping on any of my forms or anything, and this is typically good
	practice to avoid very frustrating consequences to either developers or users. (Especially fix the period existing
	even when a person does not list a middle initial).

8. Password requirements
	* I have no idea at the moment how you would implement this, but it would be a nice feature to have minimum password
	requirements such as being a minimum length, containing a special character and number, etc.

9. Styling touch-up
	* The styling is fairly nice (and certainly much nicer than it was when I started), but it would be nice to finesse
	the styling and really make it perfect.

10. Company table functionality
	* Currently I am not actually using a separate company table combined with JOIN statements, and it isn't super
	necessary at the moment and it adds an extra layer of complexity which opens you to the possibility of more bugs.
	This would be a nice and realistic thing to add to the website, however, and opens the door for more functionality.

11. Better handling of salary
	* Currently the salary accepts a floating point number, but it doesn't work if the user enters in commas, and I would
	like it to be able to strip those out without any issue.

12. Bug: Edit form salary field doesn't have validators
	* Since I haven't been able to implement WTForms for the edit form, it isn't validating before submitting and a user
	can use commas in their salary field and when they try to edit the employee again or view them it will break from
	trying to do float stuff on a string type.


##PRIMARY SOURCES:

###FLASK:

* [Flask Installation](http://flask.readthedocs.io/en/latest/installation/)
* [Flask Quickstart](http://flask.readthedocs.io/en/latest/quickstart/)
* [Flask Tutorial: Flaskr](http://flask.readthedocs.io/en/latest/tutorial/)

###WTFORMS:

* [Flask Quickstart: Creating WTForms](https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms)
* [WTForms Fields](http://wtforms.simplecodes.com/docs/0.6.1/fields.html)
* [WTForms Validators](http://wtforms.readthedocs.io/en/latest/validators.html)
* [Form Validation with WTForms](http://flask.pocoo.org/docs/0.12/patterns/wtforms/)

###JINJA2:

* [Jinja2 Template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/)
* [Jinja2 Documentation](http://jinja.pocoo.org/docs/2.10/)

###SQLITE

* [SQL as Understood by SQLite](https://sqlite.org/lang.html)
* [SQLite3 CLI](https://www.sqlite.org/cli.html)
* [SQlite3 Quering the Database Schema](https://www.sqlite.org/cli.html#querying_the_database_schema)

###BOOTSTRAP

* [Bootstrap Home](https://getbootstrap.com/)
* [Bootstrap Getting Started](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
* [Bootstrap Badges](https://getbootstrap.com/docs/4.0/components/badge/)
* [Bootstrap Lists](https://getbootstrap.com/docs/4.0/components/list-group/)
* [Bootstrap Navbar](https://getbootstrap.com/docs/4.0/components/navbar/)
* [Bootstrap Jumbotron](https://getbootstrap.com/docs/4.0/components/jumbotron/)

###JAVASCRIPT
* [setTimeout method](https://www.w3schools.com/Jsref/met_win_settimeout.asp)

### USEFUL REFERENCE TUTORIAL VIDEOS

* [Traversy Media Video 1](https://www.youtube.com/watch?v=zRwy8gtgJ1A)
* [Traversy Media Video 2](https://www.youtube.com/watch?v=addnlzdSQs4&t=1209s)

## MISC SOURCES:

* [Install Venv for Python 3](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)
* [Python two decimal display for a floating point number](https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points)
* [Python for-loop iterator help](https://stackoverflow.com/questions/17691838/range-in-jinja2-inside-a-for-loop)
* [Python line continuation](https://stackoverflow.com/questions/4172448/is-it-possible-to-break-a-long-line-to-multiple-lines-in-python)
* [Insert a python variable into an SQLite query](https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python)
* [Flask Dynamic URL Building tutorial video](https://www.youtube.com/watch?v=WijSHvC18ro)
* [HTML Button Link](https://stackoverflow.com/questions/2906582/how-to-create-an-html-button-that-acts-like-a-link)
* [Database update clause with string replacement](https://stackoverflow.com/questions/16322031/python-variable-replacement-in-sqlite3-insert-statement)
* [Python string formatting](https://stackoverflow.com/questions/5082452/python-string-formatting-vs-format)
* [SQLite update clause](https://www.tutorialspoint.com/sqlite/sqlite_update_query.htm)
* [SQLite documentation](https://sqlite.org/lang.html)
* [Jinja2 Comments](https://stackoverflow.com/questions/13562222/jinja2-inline-comments)
* [SQL Order of "WHERE" and "ORDER BY" clauses](https://www.techonthenet.com/sql/order_by.php)
* [SQLite Foreign Keys](https://sqlite.org/foreignkeys.html)
* [Flask/Jinja2 Template request.path for identifying current page](https://stackoverflow.com/questions/8676455/flask-current-page-in-request-variable)
* [Centering buttons in a div in Boostrap](https://stackoverflow.com/questions/22578853/how-to-center-buttons-in-twitter-bootstrap-3)
* [Bootstrap button group](https://stackoverflow.com/questions/11832250/css-bootstrap-display-button-inline-with-text)
* [Removing irritating collapsing](https://stackoverflow.com/questions/20219796/bootstrap-collapse-menu-disappears-when-resizing-screen)
* [Install Passlib](http://passlib.readthedocs.io/en/stable/install.html)
* [Currency Format](https://stackoverflow.com/questions/320929/currency-formatting-in-python/3393776)
* [Nice README format](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md)
* [MarkDown cheat sheet](https://en.support.wordpress.com/markdown-quick-reference/)
* [SQLite3 Clear Screen](https://stackoverflow.com/questions/21616375/is-there-a-command-to-clear-screen-in-sqlite3)
