from flask import Flask, render_template, flash, request, session, redirect, url_for
from dbconnect import connection
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, validators, PasswordField, BooleanField, SelectField, DateField, IntegerField, StringField
from wtforms.validators import InputRequired, length, Email
from flask_wtf import FlaskForm, form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from functools import wraps

c,conn=connection()

app = Flask(__name__)
person = None

@app.route('/')
def index():
    c.execute("SELECT title, surname, firstname FROM individ")
    individ =c.fetchall()
    
    return render_template('h1.html', person=individ)

app.run(debug=True)