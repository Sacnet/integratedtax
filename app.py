#from src.models.user import User
import os
from flask import Flask, render_template, flash, request, session, redirect, url_for, send_from_directory
from dbconnect import connection
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, validators, PasswordField, BooleanField, SelectField, DateField, IntegerField, StringField
from wtforms.validators import InputRequired, length, Email
from flask_wtf import FlaskForm, form
from passlib.hash import sha256_crypt
import datetime
from MySQLdb import escape_string as thwart
import gc
from functools import wraps
app = Flask(__name__)
app.secret_key = "sacnet"
#app.config['MYSQL_CURSOR'] = 'DictCursor'

Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def log():
    return render_template("login.html")

#@app.before_first_request
#def initialize_database():
    #Database.initialize()
@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")

#class LoginForm(Form):
    #name = StringField('Individual/Organisation Name', validators=[InputRequired()])
    #username = StringField('Username', validators=[InputRequired()])
    #password = PasswordField('Password', validators=[InputRequired()])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/login/', methods=['GET', 'POST'])
def login_user():
    error=''
    try:
          
        if request.method== "POST" and request.form['username']=='Sole Proprietorship':
            name1 = request.form['surname']
            username = request.form['username']
            passwordcand = request.form['password']
            c, conn=connection()
            result = c.execute("SELECT * FROM individ WHERE surname = (%s) and username = (%s)", (thwart(name1), thwart(username),))
            if result > 0:
                data =c.fetchone()[12]
                
                if passwordcand == data:
                    session['logged_in'] = True
                    session['name1'] = name1
                    session['passwordcand'] = passwordcand
                    flash(f'Welcome {name1}: ')
                    return redirect(url_for('dashboard'))
                else:
                    error='Wrong Password'
                    return render_template('login.html', error=error)
            else:
                error="Invalid credentials. Try Again"
                return render_template('login.html', error=error)
            gc.collect()
        elif  request.method== "POST" and request.form['username']=='Staff':
            name1 = request.form['surname']
            username = request.form['username']
            passwordcand = request.form['password']
            c, conn=connection()
            result = c.execute("SELECT * FROM users WHERE surname = (%s) and username = (%s)", (thwart(name1), thwart(username),))
            if result > 0:
                data =c.fetchone()[20]
                
                if passwordcand == data:
                    session['logged_in'] = True
                    session['name1'] = name1
                    session['passwordcand'] = passwordcand
                    flash(f'Welcome {name1}: ')
                    return redirect(url_for('dash'))
                else:
                    error='Wrong Password'
                    return render_template('login.html', error=error)
            else:
                error="Invalid credentials. Try Again"
                return render_template('login.html', error=error)
            gc.collect()
        elif  request.method== "POST" and request.form['username']=='Medium Scale':
            name1 = request.form['surname']
            username = request.form['username']
            passwordcand = request.form['password']
            c, conn=connection()
            result = c.execute("SELECT * FROM smallmed WHERE instiname = (%s) and username = (%s)", (thwart(name1), thwart(username),))
            if result > 0:
                data =c.fetchone()[13]
                
                if passwordcand == data:
                    session['logged_in'] = True
                    session['name1'] = name1
                    session['passwordcand'] = passwordcand
                    flash(f'Welcome {name1}: ')
                    return redirect(url_for('dashed'))
                else:
                    error='Wrong Password'
                    return render_template('login.html', error=error)
            else:
                error="Invalid credentials. Try Again"
                return render_template('login.html', error=error)
            gc.collect()
        elif  request.method== "POST" and request.form['username']=='Corporate':
            name1 = request.form['surname']
            username = request.form['username']
            passwordcand = request.form['password']
            c, conn=connection()
            result = c.execute("SELECT * FROM corport WHERE instituname = (%s) and username = (%s)", (thwart(name1), thwart(username),))
            if result > 0:
                data =c.fetchone()[13]
                
                if passwordcand == data:
                    session['logged_in'] = True
                    session['name1'] = name1
                    session['passwordcand'] = passwordcand
                    flash(f'Welcome {name1}: ')
                    return redirect(url_for('dashedboard'))
                else:
                    error='Wrong Password'
                    return render_template('login.html', error=error)
            else:
                error="Invalid credentials. Try Again"
                return render_template('login.html', error=error)
            gc.collect()
        else:
            error="Username not found"
            return render_template("login.html", error=error)
        return render_template("login.html")

    except Exception as e:
         return (str(e))
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return render_template('login.html')
    return wrap

@app.route('/upload/', methods=['GET', 'POST'])
@is_logged_in
def upload():
    if request.method=='POST':
        target = os.path.join(APP_ROOT, 'static/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the filename:".format(upload.filename))
            filename = upload.filename
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save to:", destination)
            upload.save(destination)
        #return send_from_directory("images", filename, as_attachment=True)
        return render_template('upload.html')
    
    return render_template('upload.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)



@app.route('/taxent/', methods=['GET', 'POST'])
@is_logged_in
def taxent():
    if request.method=='POST' and request.form['typeid']=='Sole Proprietorship':
        moneyval=request.form['movalue']
        surname=session['name1']
        typeid=request.form['typeid']
        now=datetime.datetime.now()
        expires=datetime.datetime.now() + datetime.timedelta(days=365)
        moneyval=float(moneyval)
        tax=(moneyval*5)/100
        c,conn=connection()
        result=c.execute("INSERT INTO debttab (surname, typeid, amount, amountent, dateent, datenext) VALUES (%s, %s, %s, %s, %s, %s)", (thwart(surname), thwart(typeid), [tax], [moneyval], [now], [expires]))
        if result>0:
            flash('Tax Calculated successfully', 'success')
            conn.commit()
            c.close()
            conn.close()
            return render_template("taxent.html")
        else:
            flash('Tax Not calculated', 'danger')
            return render_template("taxent.html")
    elif request.method=='POST' and request.form['typeid']=='corporate':
        moneyval=request.form['movalue']
        surname=session['name1']
        typeid=request.form['typeid']
        now=datetime.datetime.now()
        expires=datetime.datetime.now() + datetime.timedelta(days=365)
        moneyval=float(moneyval)
        tax=(moneyval*12)/100
        c,conn=connection()
        result=c.execute("INSERT INTO debttab (surname, typeid, amount, amountent, dateent, datenext) VALUES (%s, %s, %s, %s, %s, %s)", (thwart(surname), thwart(typeid), [tax], [moneyval], [now], [expires]))
        if result>0:
            flash('Tax Calculated successfully', 'success')
            message='Tax Owned is {tax}'
            conn.commit()
            c.close()
            conn.close()
            return render_template("taxent.html", message=message)
        else:
            flash('Tax Not calculated', 'danger')
            return render_template("taxent.html")
        return render_template("taxent.html")
    elif request.method=='POST' and request.form['typeid']=='smallmed':
        moneyval=request.form['movalue']
        surname=session['name1']
        typeid=request.form['typeid']
        now=datetime.datetime.now()
        expires=datetime.datetime.now() + datetime.timedelta(days=365)
        moneyval=float(moneyval)
        tax=(moneyval*8)/100
        c,conn=connection()
        result=c.execute("INSERT INTO debttab (surname, typeid, amount, amountent, dateent, datenext) VALUES (%s, %s, %s, %s, %s, %s)", (thwart(surname), thwart(typeid), [tax], [moneyval], [now], [expires]))
        if result>0:
            flash('Tax Calculated successfully', 'success')
            message='Tax Owned is {tax}'
            conn.commit()
            c.close()
            conn.close()
            return render_template("taxent.html", message=message)
        else:
            flash('Tax Not calculated', 'danger')
            return render_template("taxent.html")
        return render_template("taxent.html")
    elif request.method=='POST' and request.form['typeid']=='property':
        moneyval=request.form['movalue']
        surname=session['name1']
        typeid=request.form['typeid']
        now=datetime.datetime.now()
        expires=datetime.datetime.now() + datetime.timedelta(days=365)
        moneyval=float(moneyval)
        tax=(moneyval*25)/100
        c,conn=connection()
        result=c.execute("INSERT INTO debttab (surname, typeid, amount, amountent, dateent, datenext) VALUES (%s, %s, %s, %s, %s, %s)", (thwart(surname), thwart(typeid), [tax], [moneyval], [now], [expires]))
        if result>0:
            flash('Tax Calculated successfully', 'success')
            message='Tax Owned is {tax}'
            conn.commit()
            c.close()
            conn.close()
            return render_template("taxent.html", message=message)
        else:
            flash('Tax Not calculated', 'danger')
            return render_template("taxent.html")
        return render_template("taxent.html")
    elif request.method=='POST' and request.form['typeid']=='organstaff':
        moneyval=request.form['movalue']
        surname=session['name1']
        typeid=request.form['typeid']
        now=datetime.datetime.now()
        expires=datetime.datetime.now() + datetime.timedelta(days=30)
        moneyval=float(moneyval)
        tax=(moneyval*8)/100
        c,conn=connection()
        result=c.execute("INSERT INTO debttab (surname, typeid, amount, amountent, dateent, datenext) VALUES (%s, %s, %s, %s, %s, %s)", (thwart(surname), thwart(typeid), [tax], [moneyval], [now], [expires]))
        if result>0:
            flash('Tax Calculated successfully', 'success')
            message='Tax Owned is {tax}'
            conn.commit()
            c.close()
            conn.close()
            return render_template("taxent.html", message=message)
        else:
            flash('Tax Not calculated', 'danger')
            return render_template("taxent.html")
        return render_template("taxent.html")
    return render_template("taxent.html")

@app.route('/logout/')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return render_template('login.html')



@app.route('/accountcre/')
def account():
    return render_template('accountcre.html')

@app.route('/licenprint/')
def ecopy():
    return render_template('licenprint.html')

@app.route('/licenecopy/', methods=['GET', 'POST'])
def licen():
    if request.method=='POST':
        compname=request.form['username']
        ceosurname=request.form['password']
        c, conn=connection()
        results=c.execute("SELECT * FROM licensered WHERE busname=(%s) and ceosurname=(%s)", (thwart(compname), thwart(ceosurname),))
        if results>0:
            c.execute("SELECT * FROM licensered WHERE busname=(%s)", (thwart(compname),))
            licenseinfo=c.fetchall()
            conn.close()
            return render_template('licenprint.html', licenseinfo=licenseinfo)
        else:
            flash('License approval record not found', 'danger')
            return render_template('licenecopy.html')
    return render_template('licenecopy.html')

@app.route('/pinpayment/', methods=['GET', 'POST'])
@is_logged_in 
def paymentpin_user():
    if request.method=='POST' and (request.form['cardpin']>='4000000000' and request.form['cardpin']<='4999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        surname=session['name1']
        c, conn=connection()
        d=c
        e=c
        f=c
        b=c
        a=c
        results=d.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=d.execute("SELECT * FROM paypin1 WHERE noseRial=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            if result>0:
                amount=1000
                flash('Payment Successful', 'success')
                d.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                result=e.execute("SELECT * FROM accountcal WHERE namefirst=(%s)", ([session['name1']]))
                if result>0:
                    b.execute("SELECT * FROM accountcal WHERE namefirst=(%s)", ([session['name1']],))
                    amountt=b.fetchone()[2]
                    
                    amount=(1000)
                    amountt=amountt+amount 
                    a.execute("UPDATE accountcal SET amount=%s WHERE namefirst=%s", (session['name1'], [amountt]))
                    conn.commit()
                    a.close() 
                else:
                    f.execute("INSERT INTO accountcal (namefirst, amount) VALUES (%s, %s)", ([session['name1']], amount))
                    conn.commit() 
                    f.close()  
                conn.commit()               
                    
                return render_template('pinpayment.html')
                d.close()  
                e.close()
                conn.close()
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='8000000000' and request.form['cardpin']<='8999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin12 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=2000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='2000000000' and request.form['cardpin']<='2999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin13 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=5000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='9000000000' and request.form['cardpin']<='9999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin14 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=10000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='7000000000' and request.form['cardpin']<='7999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin15 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=20000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='1000000000' and request.form['cardpin']<='1999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin16 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=50000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='6000000000' and request.form['cardpin']<='6999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin17 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=100000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='3000000000' and request.form['cardpin']<='3999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin18 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=200000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='5000000000' and request.form['cardpin']<='5999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin19 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=500000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    elif request.method=='POST' and (request.form['cardpin']>='2000000000' and request.form['cardpin']<='2999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        surname=session['name1']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM credittab WHERE noSerial=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used Pin, dont defraud your country', 'danger')
            return render_template('pinpayment.html')
        else:
            result=c.execute("SELECT * FROM paypin20 WHERE seRialNo=(%s) and pin=(%s)",(thwart(serialNo), thwart(pincard),))
            if result>0:
                flash('Payment Successful', 'success')
                amount=1000000.00
                c.execute("INSERT INTO credittab (noSerial, surname, amount, datepaid) VALUES (%s, %s, %s, %s)", (thwart(serialNo), thwart(surname), [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                render_template('pinpayment.html')
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('pinpayment.html')
    else:
        return render_template('pinpayment.html')
    return render_template("pinpayment.html")

@app.route('/report')
@is_logged_in
def delete_report():
    return render_template('report.html')

@app.route('/delete_staff/<string:id>', methods=['POST'])
@is_logged_in
def delete_staff(id):
    c, conn=connection()
    c.execute('DELETE FROM USERS WHERE serialNO=(%s)',[id])
    conn.commit()
    c.close
    flash('Staff deleted successfully','success')
    return render_template('dash.html')

@app.route('/delete_staf/<string:id>', methods=['POST'])
@is_logged_in
def delete_staf(id):
    c, conn=connection()
    c.execute('DELETE FROM organstaffrec WHERE noSerial=(%s)',[id])
    conn.commit()
    c.close
    flash('Staff deleted successfully','success')
    return render_template('report.html')

@app.route('/dashedboard/')
@is_logged_in 
def dashedboard():
    c,conn=connection()
    d=c
    e=c 
    f=c
    d.execute("SELECT * FROM corport WHERE instituname=(%s)", [session['name1']])
    individ =d.fetchall()
    e.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
    debttab=e.fetchall()
    f.execute("SELECT * FROM credittab WHERE surname=(%s)", [session['name1']])
    credittab=f.fetchall()
    conn.commit()
    d.close()
    e.close()
    f.close()
    conn.close()
    return render_template('dashedboard.html', individ=individ, debttab=debttab, credittab=credittab)


@app.route('/dash/')
@is_logged_in 
def dash():
    c,conn=connection()
    d=c
    e=c 
    f=c
    d.execute("SELECT * FROM users WHERE surname=(%s)", [session['name1']])
    users =d.fetchall()
    e.execute("SELECT * FROM debttab")
    debttab=e.fetchall()
    f.execute("SELECT amount FROM credittab")
    credittab=f.fetchall()
    conn.commit()
    d.close()
    e.close()
    f.close()
    conn.close()
    print(users)
    return render_template('dash.html', users=users, debttab=debttab, credittab=credittab)

@app.route('/dashboard/')
@is_logged_in 
def dashboard():
    c,conn=connection()
    d=c
    e=c 
    f=c
    d.execute("SELECT * FROM individ WHERE surname=(%s)", [session['name1']])
    individ =d.fetchall()
    e.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
    debttab=e.fetchall()
    f.execute("SELECT amount, datepaid FROM credittab WHERE surname=(%s)", [session['name1']])
    credittab=f.fetchall()
    conn.commit()
    d.close()
    e.close()
    f.close()
    conn.close()
    print(debttab)
    return render_template('dashboard.html', individ=individ, debttab=debttab, credittab=credittab)

@app.route('/dashed/')
@is_logged_in 
def dashed():
    c,conn=connection()
    d=c
    e=c 
    f=c
    d.execute("SELECT * FROM smallmed WHERE instiname=(%s)", [session['name1']])
    individ =d.fetchall()
    e.execute("SELECT noSerial, typeid, amount, datenext FROM debttab WHERE surname=(%s)", [session['name1']])
    debttab=e.fetchall()
    f.execute("SELECT amount, datepaid FROM credittab WHERE surname=(%s)", [session['name1']])
    credittab=f.fetchall()
    conn.commit()
    d.close()
    e.close()
    f.close()
    conn.close()
    print(debttab)
    return render_template('dashed.html', individ=individ, debttab=debttab, credittab=credittab)

@app.route('/viewstaff/')
@is_logged_in
def view():
    c,conn=connection()
    c.execute("SELECT * FROM users")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('viewstaff.html', users=users)
@app.route('/viewstaf/')
@is_logged_in
def viewst():
    c,conn=connection()
    c.execute("SELECT * FROM organstaffrec WHERE organame=(%s)", [session['name1']])
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('viewstaf.html', users=users)
@app.route('/linpinrec/')
@is_logged_in
def viewlin():
    c,conn=connection()
    c.execute("SELECT * FROM licensepinrec")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('linpinrec.html', users=users)

@app.route('/licomrecord/')
@is_logged_in
def recordlin():
    c,conn=connection()
    c.execute("SELECT * FROM licensered")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('licomrecord.html', users=users)

@app.route('/smallmed/')
@is_logged_in
def recordlist():
    c,conn=connection()
    c.execute("SELECT * FROM smallmed")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('smallmed.html', users=users)

@app.route('/recordprop/')
@is_logged_in
def recordprop():
    c,conn=connection()
    c.execute("SELECT * FROM propertydec")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('recordprop.html', users=users)

@app.route('/allpinpay/')
@is_logged_in
def paymentpinrecord():
    c,conn=connection()
    c.execute("SELECT * FROM credittab")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('allpinpay.html', users=users)

@app.route('/pinrecord/')
@is_logged_in
def pinrecord():
    c,conn=connection()
    c.execute("SELECT * FROM credittab WHERE surname=(%s)", [session['name1']])
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('pinrecord.html', users=users)
@app.route('/paymentrec/')
@is_logged_in
def payrecord():
    c,conn=connection()
    c.execute("SELECT * FROM paytab WHERE surname=(%s)", [session['name1']])
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('paymentrec.html', users=users)

@app.route('/allpay/')
@is_logged_in
def allpayrecord():
    c,conn=connection()
    c.execute("SELECT * FROM paytab")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('allpay.html', users=users)

@app.route('/registcom/')
@is_logged_in
def registcom():
    c,conn=connection()
    c.execute("SELECT * FROM corport")
    users=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('registcom.html', users=users)

@app.route('/payment/', methods=['GET', 'POST'])
@is_logged_in
def payment():
    c,conn=connection()
    c.execute("SELECT typeid, amount FROM debttab WHERE surname=(%s)", [session['name1']])
    debttab=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('payment.html', debttab=debttab)

@app.route('/paytax/', methods=['GET', 'POST'])
@is_logged_in
def paytax():
    c,conn=connection()
    b=c
    a=c
    d=c
    e=c
    f=c
    g=c
    h=c
    i=c
    if request.method=="POST":
        result=a.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
        surname=a.fetchone()[1]
        if result<=0:
            flash('You own no Tax for now', 'success')
            return render_template('payment.html')
        d.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
        typeid=d.fetchone()[2]
        b.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
        tax=b.fetchone()[4]
        i.execute("SELECT * FROM debttab WHERE surname=(%s)", [session['name1']])
        datenext=d.fetchone()[6]
        e.execute("SELECT * FROM credittab WHERE surname=(%s)", [session['name1']])
        credittab=e.fetchone()[3]
        if tax>credittab:
            flash('Insufficient Credit in your Account', 'danger')
            return render_template('payment.html')       
        else:
            balance=credittab-tax
            f.execute("UPDATE credittab SET amount=%s WHERE surname=%s", (session['name1'], balance))
            conn.commit()
            g.execute("DELETE FROM debttab WHERE surname=%s", [session['name1']])
            conn.commit()
           
            h.execute("INSERT INTO paytab (surname, typeid, amount, datepaid) VALUES (%s, %s, %s, %s)", ([surname], [typeid], [tax], [datenext]))
            conn.commit()
            g.close()
            h.close()
            conn.close()
            flash('Tax successfully paid', 'success')
            return render_template('payment.html')
            
    
    
    return render_template('payment.html')

'''
    items = []
    c, conn=connection()
    c.execute("SELECT * FROM individ")
    individ =c.fetchall()
    for i in individ:
        for j in i:
            items.append(j)
    conn.commit()
    c.close()
    conn.close()
    gc.collect()
    return render_template("dashboard.html", items = items)    


    now = datetime.datetime.now()
requests = DB.get_requests(current_user.get_id())
for req in requests:
deltaseconds = (now - req['time']).seconds
req['wait_minutes'] = "{}.{}".format((deltaseconds/60),
str(deltaseconds % 60).zfill(2))
return render_template("dashboard.html", requests=requests)
'''

class organStaffReg(Form):
    
    title = SelectField('Title', choices=[('', 'Select TITLE'), ('Mr.', 'Mr.'), ('Miss.', 'Miss.'), ('Mrs.', 'Mrs'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], validators=[InputRequired()])
    surname = StringField('Surname', validators=[length(min=2, max=50), InputRequired()])
    firstname = StringField('First Name', validators=[length(min=2, max=50), InputRequired()])
    lastname = StringField('Last Name', validators=[length(min=2, max=50), InputRequired()])
    phoneno = TextField('Phone Number', validators=[length(max=11), InputRequired()])
    email = TextField('Email Address', validators=[length(max=50), Email()])
    tin = TextField('TIN', validators=[length(max=11), InputRequired()])
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and that I will contually perform my civic duty so as to contribute to the development of my country', [validators.Required()])


@app.route('/orgsta/', methods=['GET', 'POST'])
@is_logged_in
def organ_user():
    try:
        form = organStaffReg(request.form)
        if request.method == "POST" and form.validate():
            title = form.title.data
            surname = form.surname.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            phoneno = form.phoneno.data
            email = form.email.data
            taxin = form.tin.data
            now=datetime.datetime.now()
            nextdate=datetime.datetime.now()+datetime.timedelta(days=30)
            c, conn=connection()
            x =c.execute("SELECT * FROM organstaffrec WHERE surname = (%s) and firstname = (%s)", (thwart(surname), thwart(firstname),))

            if int(x) > 0:
                flash(f'Account for {form.surname.data} not created, Staff already registered', 'danger')
                return render_template('orgsta.html', form=form)
            else:
                c.execute("INSERT INTO organstaffrec (title, surname, firstname, lastname, phoneno, email, tin, organame, datereg, datenext) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(title), thwart(surname), thwart(firstname), thwart(lastname), thwart(phoneno), thwart(email), thwart(taxin), session['name1'], [now], [nextdate]))
                conn.commit()
                flash(f'Account for {form.surname.data} created successfully','success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['surname'] = surname
                return render_template("orgsta.html", form=form)
        return render_template("orgsta.html", form=form)

    except Exception as e: 
        return(str(e))
def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are not authorised to view this page until payment is made, purchase a valid pin', 'danger')
            return render_template('licensepay.html')
    return wrap


@app.route('/licensepag/')
def licensepag():
    return render_template('licensepag.html')

@app.route('/licensepay/', methods=['GET', 'POST'])
def licensee():
    if request.method=='POST' and (request.form['cardpin']>='100000000' and request.form['cardpin']<='199999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin3 WHERE noseRial=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=50
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard),[refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='200000000' and request.form['cardpin']<='299999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin4 WHERE noseRial=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=100.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='900000000' and request.form['cardpin']<='999999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin5 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=200.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='500000000' and request.form['cardpin']<='599999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin6 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=250.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='800000000' and request.form['cardpin']<='899999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin7 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fectchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=500.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='400000000' and request.form['cardpin']<='499999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin8 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=1000.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [refrr], [amount], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='700000000' and request.form['cardpin']<='799999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin9 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=1500.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [amount], [refrr], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    elif request.method=='POST' and (request.form['cardpin']>='300000000' and request.form['cardpin']<='399999999'):
        serialNo = request.form['serialNo'] 
        pincard = request.form['cardpin']
        now=datetime.datetime.now()
        c, conn=connection()
        results=c.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(serialNo),))
        if results>0:
            flash('Already used License Pin, dont defraud your country', 'danger')
            return render_template('licensepay.html')
        else:
            result=c.execute("SELECT noseRial, pin, reference FROM paypin10 WHERE seRialNo=(%s) and pin=(%s)", (thwart(serialNo), thwart(pincard),))
            refrr=c.fetchone()[2]
            if result>0:
                flash('License Payment Successful, Fill the form below to complete your operating license', 'success')
                amount=2000.00
                c.execute("INSERT INTO licensepinrec (serialno, pin, ref, amount, date) VALUES (%s, %s, %s, %s, %s)", (thwart(serialNo), thwart(pincard), [amount], [refrr], [now]))
                conn.commit()
                c.close()
                conn.close()
                return redirect(url_for('license', form=form))
            else:
                flash('Wrong Serial Number or Pin entered, Check again and re-enter', 'danger')
                return render_template('licensepay.html', form=form)
            return render_template('licensepay.html', form=form)
    return render_template('licensepay.html', form=form)


@app.route('/certilice/')
def certilice():
    c, conn=connection()
    c.execute("SELECT * FROM licensered WHERE reference=(%s)", [session['name1']])
    licenseinfo=c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return render_template('certilice.html', licenseinfo=licenseinfo)

class licenseform(Form):
    
    cardnose = TextField('Card Serial Number', validators=[length(min=6, max=6), InputRequired()])
    busname = StringField('Business Name', validators=[length(min=6, max=50), InputRequired()])
    tin = TextField('TIN', validators=[length(min=11, max=11), InputRequired()])
    taxpayersurname = StringField('Tax Payer Surname', validators=[length(min=2, max=50), InputRequired()])
    taxpayerfirstname = StringField('Tax Payer First Name', validators=[length(min=2, max=50), InputRequired()])
    address = StringField('Business Premises Address', validators=[length(min=6, max=50), InputRequired()])
    email = TextField('Email Address', validators=[length(max=50), Email()])
    busphoneno = TextField('Business Phone Number', validators=[length(min=11, max=11), InputRequired()])
    phoneno = TextField('Personal Phone Number', validators=[length(min=11, max=11), InputRequired()])
    cfosurname = StringField('CFO Surname', validators=[length(min=2, max=50), InputRequired()])
    cfofirstname = StringField('CFO First Name', validators=[length(min=2, max=50), InputRequired()])
    ceosurname = StringField('CEO Surname', validators=[length(min=2, max=50), InputRequired()])
    ceofirstname = StringField('CEO First Name', validators=[length(min=2, max=50), InputRequired()])
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and that I will contually perform my civic duty so as to contribute to the development of my country', [validators.Required()])


@app.route('/license/', methods=['GET', 'POST'])
def license():
        form = licenseform(request.form)
        if request.method == "POST" and form.validate():
            cardnose = form.cardnose.data
            busname = form.busname.data
            tin = form.tin.data
            payersurname = form.taxpayersurname.data
            payerfirstname = form.taxpayerfirstname.data
            address = form.address.data
            email = form.email.data
            busphoneno = form.busphoneno.data
            phoneno = form.phoneno.data
            cfosurname = form.cfosurname.data
            cfofirstname = form.cfofirstname.data
            ceosurname = form.ceosurname.data
            ceofirstname = form.ceofirstname.data
            now=datetime.datetime.now()
            c, conn=connection()
            e=c
            f=c
            x =f.execute("SELECT * FROM licensered WHERE busname = (%s) and ceosurname = (%s)", (thwart(busname), thwart(ceosurname),))
            if int(x) > 0:
                flash(f'This {form.busname.data} has been licensed already, this can not be license twice', 'danger')
                return render_template('license.html', form=form)
            else:
                d=e.execute("SELECT * FROM licensepinrec WHERE serialno=(%s)", (thwart(cardnose),))
                if int(d)>0:
                    d=e.execute("SELECT serialno, pin, ref FROM licensepinrec WHERE serialno=(%s)", (thwart(cardnose),))
                    refno=e.fetchone()[2]
                    f.execute("INSERT INTO licensered (busname, tin, payersurname, payerfirstname, address, email, busphoneno, phoneno, cfosurname, cfofirstname, ceosurname, ceofirstname, reference, datelicense) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(busname), thwart(tin), thwart(payersurname), thwart(payerfirstname), thwart(address),thwart(email), thwart(busphoneno), thwart(phoneno), thwart(cfosurname), thwart(cfofirstname), thwart(ceofirstname), thwart(ceofirstname), [refno], [now]))
                    conn.commit()    
                    session['logged_in'] = True
                    session['name1'] = refno
                    f.close()
                    conn.close()
                    gc.collect()
                    return redirect(url_for("certilice"))
                else:
                    flash(f'The License for {form.busname.data} cannot be approved, Go and purchase a valid license card','danger')
                    return render_template("licensepag.html", form=form)
        return render_template("license.html", form=form)
    

class RegistrationForm(Form):
    
    title = SelectField('Title', choices=[('', 'Select TITLE'), ('Mr.', 'Mr.'), ('Miss.', 'Miss.'), ('Mrs.', 'Mrs'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], validators=[InputRequired()])
    surname = StringField('Surname', validators=[length(min=2, max=50), InputRequired(message='Enter your Surname')])
    firstname = StringField('Firstname',  validators=[length(min=2, max=50), InputRequired()])
    gender = SelectField('Gender', choices=[('female', 'Female'), ('male', 'Male')], validators=[InputRequired()])
    status = SelectField('Status', choices=[('divorced', 'Divorsed'), ('married', 'Married'), ('single', 'Single')], validators=[InputRequired()])
    dobirth = DateField('Date of Birth', validators=[InputRequired()])
    countyofb = SelectField('County of Birth',  choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  County")])
    phoneno = TextField('Phone Number', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    stradd = TextField('Street Address', validators=[length(min=6, max=50), InputRequired(message='Address Required')])
    town = TextField('Village/Town/City', validators=[length(min=3, max=50), InputRequired(message='Village/Town/City Required')])
    countyres = SelectField('County of Residence', choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  County")])
    qualif = SelectField('Title', choices=[('', 'Select Qualification'), ('SSCE', 'SSCE'), ('NCE', 'NCE'), ('OND', 'Ordinary National Diploma'), ('HND', 'Higher National Diploma'), ('BSC', 'Bachelor of Science (B. Sc.)'), ('BArt', 'Bachelor of Art (B. Art)'), ('BEng', 'Bachelor of Engineering (B. Eng.)'), ('BEd', 'Bachelor of Education (B. Ed.)'), ('BLaw', 'Bachelor of Law (B. Law)'), ('BTech', 'Bachelor of Technology (B. Tech.)'), ('MArt', 'Master of Art (M. Art)'), ('MEng', 'Master of Engineering (M. Eng.)'), ('MEd', 'Master of Education (M. Ed.)'), ('MLaw', 'Master of Law (M. Law.)'), ('MSC', 'Master of Science (M. Sc.)'), ('MTech', 'Master of Technology (M. Tech.)'), ('PhD', 'Doctor of Philosophy (Ph. D)')], validators=[InputRequired(message="Select your  Qualification")])
    instattend = StringField('Institution Attended', [validators.length(min=6, max=50)])
    gradyear = SelectField('Year of Graduation', choices=[('', 'Select graduation year'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], validators=[InputRequired(message="Select graduation year")])
    nextkin = StringField('Next of Kin', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    nextkinadd = TextField('Next of Kin Address', validators=[length(min=6, max=50), InputRequired(message='Data Required')])
    nextkinphone = TextField('Next of Kin Phone Number', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    username = TextField('Username', [validators.length(min=5, max=50)])
    email = TextField('Email Address', validators=[length(max=50), Email()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and the <a href="/privacy/">Privacy Required</a>   in the Liberia Revenue Authority', [validators.Required()])

    
@app.route('/register/', methods=['GET', 'POST'])
def register_user():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            title = form.title.data
            surname = form.surname.data
            firstname = form.firstname.data
            gender = form.gender.data
            statue = form.status.data
            dobirth = str(form.dobirth.data)
            county = form.countyofb.data
            phoneno = form.phoneno.data
            stradd = form.stradd.data
            town = form.town.data
            countyres = form.countyres.data
            qualif = form.qualif.data
            instattend = form.instattend.data
            gradyear = form.gradyear.data
            nextkin = form.nextkin.data
            nextkinadd = form.nextkinadd.data
            nextkinphone= form.nextkinphone.data
            username = form.username.data
            email = form.email.data
            password1 = form.password.data
            now=datetime.datetime.now()
            c, conn=connection()
            x =c.execute("SELECT * FROM users WHERE surname = (%s) and firstname = (%s) and username = (%s)", (thwart(surname), thwart(firstname), thwart(username),))

            if int(x) > 0:
                flash(f'Account for {form.username.data} not created, username already taken', 'success')
                return render_template('register.html', form=form)
            else:
                c.execute("INSERT INTO users (title, surname, firstname, gender, statue, dobirth, county, phoneno, stradd, town, countyres, qualif, instattend, yeargrad, nextkin, nextkinadd, nextkinphone,  username, email, password1, dateent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(title), thwart(surname), thwart(firstname), thwart(gender), thwart(statue), thwart(dobirth), thwart(county), thwart(phoneno),  thwart(stradd), thwart(town), thwart(countyres), thwart(qualif), thwart(instattend), thwart(gradyear), thwart(nextkin), thwart(nextkinadd), thwart(nextkinphone),  thwart(username), thwart(email), thwart(password1), [now],))
                conn.commit()
                flash(f'Account for {form.username.data} created successfully','success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return render_template('register.html', form=form)
        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))

class IndividReg(Form):
    
    title = SelectField('Title', choices=[('', 'Select TITLE'), ('Mr.', 'Mr.'), ('Miss.', 'Miss.'), ('Mrs.', 'Mrs'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], validators=[InputRequired()])
    surname = StringField('Surname', validators=[length(min=2, max=50), InputRequired()])
    firstname = StringField('FirstName', validators=[length(min=2, max=50), InputRequired()])
    gender = SelectField('Gender', choices=[('female', 'Female'), ('male', 'Male')])
    phoneno = TextField('Phone Number', validators=[length(min=11, max=11), InputRequired()])
    email = TextField('Email Address', validators=[length(max=50), Email()])
    streadd = TextField('Street Address', validators=[length(min=6, max=50), InputRequired()])
    town = TextField('Village/Town/City', validators=[length(min=3, max=50), InputRequired()])
    county = SelectField('County of Residence', choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired()])
    countryres = TextField('Country of Residence', validators=[length(min=4, max=50), InputRequired()])
    username = TextField('Username', [validators.length(min=5, max=50)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and the <a href="/privacy/">Privacy Required</a>   in the Liberia Revenue Authority', [validators.Required()])

@app.route('/form1/', methods=['GET', 'POST'])
def form1_user():
    try:
        form = IndividReg(request.form)

        if request.method == "POST" and form.validate():
            title = form.title.data
            surname = form.surname.data
            firstname = form.firstname.data
            gender = form.gender.data
            phoneno = form.phoneno.data
            email = form.email.data
            streadd = form.streadd.data
            town = form.town.data
            county = form.county.data
            countryres = form.countryres.data
            username = form.username.data
            password1 = form.password.data
            now=datetime.datetime.now()
            c, conn=connection()
            x =c.execute("SELECT * FROM individ WHERE surname = (%s) and firstname = (%s) and username = (%s)", (thwart(surname), thwart(firstname), thwart(username),))

            if int(x) > 0:
                flash(f'Account for {form.username.data} not created, username already taken', 'danger')
                return render_template('form1.html', form=form)
            else:
                c.execute("INSERT INTO individ (title, surname, firstname, gender, phoneno, email, streadd, town, county, countryres, username, password1, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(title), thwart(surname), thwart(firstname), thwart(gender), thwart(phoneno), thwart(email),  thwart(streadd), thwart(town), thwart(county), thwart(countryres), thwart(username), thwart(password1), [now]))
                conn.commit()
                flash(f'Account for {form.username.data} created successfully','success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return render_template("form1.html", form=form)
        return render_template("form1.html", form=form)

    except Exception as e: 
        return(str(e))


class CorporReg(Form):
    
    instname = StringField('Company/Institution Name', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    taxnum = StringField('Tax Identification Number', validators=[length(min=11, max=11), InputRequired(message='Data Required')])
    regnum = StringField('Company/Institution Registration Number', validators=[length(min=11, max=11), InputRequired(message='Data Required')])
    datereg = DateField('Date of Registration ', validators=[InputRequired(message='Data Required')])
    officeemail = TextField('Official Email', validators=[length(max=50), Email(message='Invalid email'), InputRequired(message='Data Required')])
    officephone = TextField('Official Phone Number', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    officeadd = TextField('Company/Institution Address', validators=[length(min=5, max=50), InputRequired(message='Address Required')])
    town = TextField('Village/Town/City', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    county = SelectField('County of Residence', choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  COunty")])
    surname = StringField('Surname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    firstname = StringField('Firstname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    lastname = StringField('Lastname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    username = TextField('Username', [validators.length(min=5, max=50)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and the <a href="/privacy/">Privacy Required</a> of the Liberia Revenue Agency', [validators.Required()])

@app.route('/form2/', methods=['GET', 'POST'])
def form2_user():
    try:
        form = CorporReg(request.form)

        if request.method == "POST" and form.validate():
            
            instname = form.instname.data
            taxnum = form.taxnum.data
            regnum = form.regnum.data
            datereg = str(form.datereg.data)
            officeemail = form.officeemail.data
            officephone = form.officephone.data
            officeadd = form.officeadd.data
            town = form.town.data
            county = form.county.data
            surname = form.surname.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            username = form.username.data
            password1 = form.password.data
            now=datetime.datetime.now()
            c, conn=connection()
            x =c.execute("SELECT * FROM corport WHERE instituname = (%s) and username = (%s)", (thwart(instname), thwart(username),))

            if int(x) > 0:
                flash(f'Account for {form.instname.data} has already registered, please check the name properly and try again', 'danger')
                return render_template('form2.html', form=form)
            else:
                c.execute("INSERT INTO corport (instituname, taxnumb, regnumb, datereg, offemail, offphone, offadd, town, county, consurname, confirstname, conlastname, username, password1, datereg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(instname), thwart(taxnum), thwart(regnum), thwart(datereg), thwart(officeemail), thwart(officephone), thwart(officeadd), thwart(town),  thwart(county), thwart(surname), thwart(firstname), thwart(lastname), thwart(username), thwart(password1), [now]))
                conn.commit()
                flash(f'Account for {form.instname.data} created successfully Thanks for Registering your company', 'success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return render_template("form2.html", form=form)
        return render_template("form2.html", form=form)

    except Exception as e: 
        return(str(e))


class SmallReg(Form):
    instname = StringField('Company/Institution Name', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    taxnum = StringField('Tax Identification Number', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    regnum = StringField('Company/Institution Registration Number', validators=[length(min=12, max=12), InputRequired(message='Data Required')])
    officeemail = TextField('Official Email', validators=[length(max=50), Email(message='Invalid email'), InputRequired(message='Data Required')])
    officephone = TextField('Official Phone Number', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    officeadd = TextField('Company/Institution Address', validators=[length(min=4, max=50), InputRequired(message='Address Required')])
    town = TextField('Village/Town/City', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    county = SelectField('County of Residence', choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  COunty")])
    surname = StringField('Surname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    firstname = StringField('Firstname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    lastname = StringField('Lastname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    username = TextField('Username', [validators.length(min=4, max=50)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField ('I accept the  <a href="/tos/">Condition of Service</a> and the <a href="/privacy/">Privacy Required</a> of the Liberia Revenue Authority', [validators.Required()])

@app.route('/form3/', methods=['GET', 'POST'])
def form3_user():
    try:
        form = SmallReg(request.form)
        instname = form.instname.data
        taxnum = form.taxnum.data
        regnum = form.regnum.data
        officeemail = form.officeemail.data
        officephone = form.officephone.data
        officeadd = form.officeadd.data
        town = form.town.data
        county = form.county.data
        surname = form.surname.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        now=datetime.datetime.now()
        if request.method == "POST" and form.validate():
            c, conn=connection()
            x =c.execute("SELECT * FROM smallmed WHERE instiname = (%s) and username = (%s)", (thwart(instname), thwart(username),))

            if int(x) > 0:
                flash("This Institution has been registered already, please check and try again", 'danger')
                return render_template('form3.html', form=form)
            else:
                c.execute("INSERT INTO smallmed (instiname, taxnumb, regnum, offemail, offphone, offaddress, town, county, surname, firstname, lastname, username, password1, datereg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (thwart(instname), thwart(taxnum), thwart(regnum), thwart(officeemail), thwart(officephone), thwart(officeadd), thwart(town),  thwart(county), thwart(surname), thwart(firstname), thwart(lastname), thwart(username), thwart(password), [now]))
                conn.commit()
                flash("Thanks for Registering!", 'success')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return render_template("form3.html", form=form)
        return render_template("form3.html", form=form)

    except Exception as e: 
        return(str(e))


class PropertyDeclaration(Form):
    tin = StringField('Tax Identification Number (TIN)', validators=[length(min=10, max=10), InputRequired(message='Data Required')])
    title = SelectField('Title', choices=[('', 'Select TITLE'), ('Mr.', 'Mr.'), ('Miss.', 'Miss.'), ('Mrs.', 'Mrs'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], validators=[InputRequired(message="Select your  Title")])
    owsurname = StringField('Owner Surname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    owfirstname = StringField('Owner Firstname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    owlastname = StringField('Owner Lastname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    owemail = TextField('Owner Email', validators=[length(max=50), Email(message='Invalid email'), InputRequired(message='Data Required')])
    owphoneno = TextField('Owner Phone Number 1', validators=[length(min=11,max=11), InputRequired(message='Phone Number Required')])
    owphoneno1 = TextField('Owner Phone Number 2', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    owstreetadd = TextField('Owner Current Address', validators=[length(min=4, max=50), InputRequired(message='Address Required')])
    owcommunity = TextField('Community', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    owtown = TextField('Village/Town/City', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    county = SelectField('Owner County of Residence', choices=[('', 'Select County'), ('bomi', 'bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  COunty")])
    occupantsur = StringField('Occupant Surname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    occupantfirst = StringField('Occupant Firstname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    occupantphone = TextField('Occupant Phone Number ', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    occupantemail = TextField('Occupant Email', validators=[length(max=50), Email(message='Invalid email'), InputRequired(message='Data Required')])
    adminsur = StringField('Administrator Surname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    adminfirst = StringField('Administrator Firstname', validators=[length(min=2, max=50), InputRequired(message='Data Required')])
    adminphone = TextField('Administrator Phone Number ', validators=[length(min=11, max=11), InputRequired(message='Phone Number Required')])
    adminemail = TextField('Administrator Email', validators=[length(max=50), Email(message='Invalid email'), InputRequired(message='Data Required')])
    streetaddr = TextField('Property Location Address', validators=[length(min=4, max=50), InputRequired(message='Address Required')])
    loccommunity = TextField('Property Location Community', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    townloc = TextField('Property Location (Village/Town/City)', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    arealandmark = TextField('Area Land Mark', validators=[length(min=4, max=50), InputRequired(message='Village/Town/City Required')])
    loccounty = SelectField('Property Location (County)', choices=[('', 'Select County'), ('bomi', 'Bomi'), ('bong', 'Bong'), ('GrandBassa', 'Grand Bassa'), ('grandcapemount', 'Grand Cape Mount'), ('grandgedeh', 'Grand Gedeh'), ('grandkru', 'Grand Kru'), ('lofa', 'Lofa'), ('margibi', 'Margibi'), ('maryland', 'Maryland'), ('montserrado', 'Montserrado'),  ('nimba', 'Nimba'),  ('rivercess', 'River Cess'),  ('sinoe', 'Sinoe')], validators=[InputRequired(message="Select your  County")])
    taxzone = StringField('Tax Zone', validators=[length(min=4, max=50), InputRequired(message='Data Required')])
    usetype = SelectField('Use Type', choices=[('', 'Select Use Type'), ('commercial', 'Commercial'), ('residential', 'Residential'), ('other', 'Others')], validators=[InputRequired(message="Select your  Title")])
    landsize = SelectField('Land Size', choices=[('', 'Select Size'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30')], validators=[InputRequired(message="Select Land Size")])
    plotacre = SelectField('Land Size Type', choices=[('', 'Select Type'), ('plot', 'Plot'), ('acre', 'Acre')], validators=[InputRequired(message="")])
    estvalue = TextField('Estimated Value of Property ', validators=[length(min=4, max=11), InputRequired(message='Phone Number Required')])
    floortype = SelectField('Floor Type', choices=[('', 'Select Floor Type'), ('ceramic', 'Ceramic'), ('terrazzo', 'Terrazzo'), ('tiles', 'Tiles'), ('other', 'Others')], validators=[InputRequired(message="")])
    foundtype = SelectField('Foundation type', choices=[('', 'Select Foundation Type'), ('cementblock', 'Cement Block'), ('mudbrick', 'Mud Brick'), ('other', 'Others')], validators=[InputRequired(message="")])
    accept_tos = BooleanField ('I certify that the information provided above is true, accurate and complete to the best of my knowledge. I acknowledge that any false declaration may lead to possible prosecution.', [validators.Required()])
@app.route('/form4/', methods=['GET', 'POST'])
def form4_user():
    try:
        form = PropertyDeclaration(request.form)
        if request.method == "POST" and form.validate():
            tinumb = form.tin.data
            title = form.title.data
            osurname = form.owsurname.data
            ofirstname = form.owfirstname.data
            olastname = form.owlastname.data
            oemail = form.owemail.data
            ophoneno = form.owphoneno.data
            ophoneno1 = form.owphoneno1.data
            ostreetadd = form.owstreetadd.data
            commun = form.owcommunity.data
            otown = form.owtown.data
            county = form.county.data
            occsurname = form.occupantsur.data
            occfirstname = form.occupantfirst.data
            occphone = form.occupantphone.data
            occemail = form.occupantemail.data
            admsurname = form.adminsur.data
            admfirstname = form.adminfirst.data
            admphone = form.adminphone.data
            admemail = form.adminemail.data
            streetaddr = form.streetaddr.data
            loccomunity = form.loccommunity.data
            town = form.townloc.data
            landmark = form.arealandmark.data
            loccounty = form.loccounty.data
            taxzone = form.taxzone.data
            usetype = form.usetype.data
            landsize = form.landsize.data
            plotacre = form.plotacre.data
            estvalue = form.estvalue.data
            floortype = form.floortype.data
            foundtype = form.foundtype.data


            c, conn=connection()
            x =c.execute("SELECT * FROM propertydec WHERE tinumber = (%s)", (thwart(tinumb),))

            if int(x) > 0:
                flash("This Property has been registered already", 'danger')
                return render_template('form4.html', form=form)
            else:
                c.execute("INSERT INTO propertydec (tinumber, title, osurname, ofirstname, olastname, owemail, owphoneno, owphoneno1, owstreetadd, owcommunity, owtown, county, occupsurname, occupfirstname, occuphone, occupemail, adminsurname, adminfirstname, adminphone, adminemail, adminstreet, loccommun, loctown, ladmark, loccounty, taxzone, usetype, landsize, lotacre, estvalue, flortype, foundtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ( thwart(tinumb), thwart(title), thwart(osurname), thwart(ofirstname), thwart(olastname), thwart(oemail), thwart(ophoneno), thwart(ophoneno1), thwart(ostreetadd), thwart(commun), thwart(otown), thwart(county), thwart(occsurname), thwart(occfirstname), thwart(occemail), thwart(occphone), thwart(admsurname), thwart(admfirstname),  thwart(admphone), thwart(admemail), thwart(streetaddr), thwart(loccomunity), thwart(town), thwart(landmark), thwart(loccounty), thwart(taxzone), thwart(usetype), thwart(landsize), thwart(plotacre), thwart(estvalue), thwart(floortype), thwart(foundtype),))
                conn.commit()
                flash("Thanks for Registering!", 'success')
                c.close()
                conn.close()
                gc.collect()
                return render_template("form4.html", form=form)

        return render_template("form4.html", form=form)

    except Exception as e: 
        return(str(e))

if __name__=='__main__':
    app.run(debug=True)