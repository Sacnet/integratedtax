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
app = Flask(__name__)
app.secret_key = "sacnet82"

  
@app.route('//')
def dashbard():
    c, conn=connection()
    d=c
    e=c
    f=c
    b=c
    a=c
    amount=1000
    flash('Payment Successful', 'success')
    result=b.execute("SELECT * FROM accountcal")
    if result>0:
        amountt=b.fetchone()[2]
        amountt+=amount
        print(amountt) 
        return render_template('', individ=amountt)

@app.route('/hhh/')
def dashboard():
    c, conn=connection()
    d=c
    e=c
    f=c
    b=c
    a=c
    amount=1000
    flash('Payment Successful', 'success')
    result=b.execute("SELECT * FROM accountcal")
    if result>0:
        amountt=b.fetchone()[2]
        amountt+=amount
        a.execute("UPDATE accountcal SET amount=%s WHERE namefirst='Abegunde'", (amountt))
        conn.commit()
        print(amountt) 
        return render_template('hhh.html', individ=amountt)
'''
def dashboard():
    items = []
    c, conn=connection()
    c.execute("SELECT * FROM users WHERE surname='Onibokun'")
    users =c.fetchall()
    conn.commit()
    c.close()
    print(users)
    return render_template('hhh.html', individ=users)

    
   
    c,conn=connection()
    d=c
    e=c 
    f=c
    d.execute("SELECT * FROM users")
    individ =d.fetchall()
    e.execute("SELECT * FROM debttab")
    debttab=e.fetchall()
    f.execute("SELECT amount FROM credittab")
    credittab=f.fetchall()
    conn.commit()
    d.close()
    e.close()
    f.close()
    conn.close()
    print(individ)
    return render_template('hhh.html', individ=individ, debttab=debttab, credittab=credittab)

@app.route('/hhh/')
def paytax():
    c,conn=connection()
    d=c
    e=c
    f=c
    g=c
    h=c
    d.execute("SELECT surname, typeid, amount FROM debttab")
    debttab=str(d.fetchone()[2])
    typeid=debttab[:2]
    tax=str(debttab[:4])
    print(debttab)
    return render_template('hhh.html', debttab=debttab)
'''
if __name__ == '__main__':
    app.run(debug=True)
