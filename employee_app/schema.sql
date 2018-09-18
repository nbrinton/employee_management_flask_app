DROP TABLE IF EXISTS  employees;
CREATE TABLE employees (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	employee_id INTEGER NOT NULL,
	lname TEXT NOT NULL,
	fname TEXT NOT NULL,
	minit TEXT NOT NULL,
	email TEXT NOT NULL,
	salary REAL NOT NULL,
	dependents INTEGER NOT NULL,
	dependentsA INTEGER NOT NULL,
	company_id INTEGER NOT NULL
/*	FOREIGN KEY(company_id) REFERENCES companies(company_id)*/
);
/*
DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	company_id INTEGER NOT NULL,
	company_name TEXT NOT NULL
);
*/
/*INSERT INTO companies (company_id, company_name) VALUES (1111111111, 'Paylocity');*/
		
/*
db.execute('insert into employees (employee_id, lname, fname, minit, email, salary, dependents, dependentsA) \
			values (?, ?, ?, ?, ?, ?, ?, ?)', [int(request.form['employee_id']), request.form['lname'], \
			request.form['fname'], request.form['minit'], request.form['email'], int(request.form['salary']), \
			int(request.form['dependents']), int(request.form['dependentsA'])])
*/


DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	fname TEXT NOT NULL,
	lname TEXT NOT NULL,
	email TEXT NOT NULL,
	password TEXT NOT NULL,
	company_id INTEGER NOT NULL
);
