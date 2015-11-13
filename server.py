from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "secret"
import re
mysql = MySQLConnector('emaildb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
@app.route('/')
def index():
	emails = mysql.fetch("Select * from emails")
	print emails
	return render_template('index.html', emails = emails)

@app.route('/process', methods=['POST'])
def create():
	emails = mysql.fetch("Select * from emails")
	if not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid Email Address')
		return redirect('/')
	else:
		query = "INSERT INTO emails (email_address, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['email'])
		mysql.run_mysql_query(query)
		return render_template('/success.html', emails = emails)

app.run(debug=True)