from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from poomb.auth import login_required
from poomb.db import get_db
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from poomb import mail
from poomb.emails import send_email
from poomb import keygen
import plotly.graph_objs as go
import nest_asyncio
import json
import asyncio
import pytz
import yagmail
from flask import jsonify


nest_asyncio.apply()


bp = Blueprint('log', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    max_tday = db.execute('SELECT MAX(tday) FROM log').fetchone()[0]
    exercises = db.execute(
        'SELECT * FROM log WHERE tday = ? AND lifter_id = ?',
        (max_tday, g.user['id'])
    ).fetchall()
    return render_template('log/index.html', exercises=exercises, tday=max_tday)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        tday = datetime.strptime(request.form['tday'], '%Y-%m-%d').strftime('%d-%m-%Y')
        exercise = request.form.getlist('exercise')
        weights = request.form.getlist('weight')
        sets = request.form.getlist('sets')
        reps = request.form.getlist('reps')
        error = None
        
        for i in range(len(exercise)):
            if not exercise[i]:
                error = 'Exercise is required for all entries.'
                break
        
        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            for i in range(len(exercise)):
                db.execute(
                    'INSERT INTO log (tday, exercise, weight, sets, reps, lifter_id)'
                    'VALUES (?, ?, ?, ?, ?, ?)',
                    (tday, exercise[i], weights[i], sets[i], reps[i], g.user['id'])
                )
            db.commit()
            flash('Training')
        return redirect(url_for('log.index'))
        
    return render_template('log/add.html')

        

@bp.route('/update/<int:tid>', methods=('GET', 'POST'))
@login_required
def update(tid):
    print("tid:", tid)
    if request.method == 'POST':
        exercise = request.form['exercise']
        weight = request.form['weight']
        sets = request.form['sets']
        reps = request.form['reps']
        error = None
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE log SET exercise = ?, weight = ?, sets = ?, reps = ?'
                'WHERE tid =?',
                (exercise, weight, sets, reps, g.user['id'])
            )
            db.commit()
            return redirect(url_for('log.index'))
        db = get_db()
        exercise = db.execute("SELECT * FROM  log WHERE TID=?",(tid,)
                          ).fetchone
        
        
    return render_template('log/update.html', tid=tid)

@bp.route('/delete/<int:tid>', methods=('GET',))
@login_required
def delete(tid):
    db = get_db()
    db.execute('DELETE FROM log WHERE tid = ?', (tid,))
    db.commit()
    return redirect(url_for('log.index'))


@bp.route('/performance', methods=('GET', 'POST'))
@login_required
def performance():
    if request.method == 'POST':
        tdate = request.form['tdate']
        try:
            tdate_obj = datetime.strptime(tdate, '%Y-%m-%d')
            tdate_formatted = tdate_obj.strftime('%d-%m-%Y')
            db = get_db()
            tperformance = db.execute('SELECT * FROM log WHERE tday = ? AND lifter_id = ?', [(tdate_formatted, g.user['id'], )]).fetchall()
        except ValueError:
            flash("No valid date")
        else:
            if len(tperformance) == 0:
             flash("No data for selected date")
        
            return render_template('log/performance.html',tperformance=tperformance, tdate=tdate)
    db = get_db()
    tperformance = db.execute('SELECT * FROM log WHERE lifter_id = ? LIMIT 10', [g.user['id']]).fetchall()
    return render_template('log/performance.html', tperformance=tperformance)

def get_user(username):
    db = get_db()
    user_data = db.execute("SELECT id, username, password FROM user WHERE username=?", (username,)).fetchone()
    if user_data:
        user_id, username, password = user_data
        return {'id': user_id, 'username': username, 'password': password}

def authenticate(username, password):
    user = get_user(username)
    if user and user['password'] == password:
        return user

def generate_token(user_id):
    expires = datetime.timedelta(hours=24)
    access_token = create_access_token(identity=user_id, expires_delta=expires)
    return access_token

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('log/reset.html')

    if request.method == 'POST':
        db = get_db()

        email = request.form.get('email')
        check_email = db.execute('SELECT * FROM user WHERE email=?', (email,))
        if email in check_email:
            send_email(email)
        else:
            flash('Email not found')

        return redirect(url_for('auth.login'))
@bp.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    db = get_db()

    user = db.execute('SELECT id FROM users WHERE reset_token = ?', (token,)).fetchone()
    if not user:
        print('No user found')
        return redirect(url_for('log.login.html'))

    password = request.form.get('password')
    if password:
        db.execute('UPDATE user SET password= ? WHERE id = ?', (password, g.user['id']))

        return redirect(url_for('log.login.html'))

    return render_template('log/reset_verified.html')


@bp.route("/pwresetrq", methods=["GET"])
def pwresetrq_get():
    return render_template('reset.html')

@bp.route("/pwresetrq", methods=["POST"])
def pwresetrq_post():
    db = get_db()
    email = request.form["email"]
    user = db.execute("SELECT * FROM user WHERE email=?", (email,)).fetchone()
    
    
    if user:
        pwalready = db.execute("SELECT * FROM pwreset WHERE user_id=?", (user[0],)).fetchone()
       

        # Check if user already has reset their password
        if pwalready:
            if not pwalready[3]:  # has_activated is False
                db.execute("UPDATE PWReset SET datetime=?, reset_key=? WHERE user_id=?", (datetime.now(), pwalready[2], user[0]))
                key = pwalready[2]
            else:
                key = keygen.make_key()
                db.execute("UPDATE PWReset SET reset_key=?, datetime=?, has_activated=? WHERE user_id=?", (key, datetime.now(), False, user[0]))
        else:
            key = keygen.make_key()
            print (type(key))
            db.execute("INSERT INTO PWReset (reset_key, user_id) VALUES (?, ?)", (str(key,), user[0]))
        
        
        
        ## Add Yagmail code here
        

        yag = yagmail.SMTP()
        contents = ['Please go to this URL to reset your password:', "APP URL HERE" + url_for("pwreset_get",  id = (str(key)))]
        yag.send(email, 'Reset your password', contents)
        flash(user[1] + ", check your email for a link to reset your password. It expires in a <amount of time here>!", "success")
        
        return redirect(url_for("index.html"))
    else:
        flash("Your email was never registered.", "danger")
        return redirect(url_for("pwresetrq_get"))

@bp.route("/pwreset/<id>", methods=["GET"])
def pwreset_get(id):
    db = get_db()
    key = id
    pwresetkey = db.execute("SELECT * FROM PWReset WHERE reset_key=?", (id,)).fetchone()
    
    generated_by = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=24)
    
    if pwresetkey[3]:  # has_activated is True
        flash("You already reset your password with the URL you are using. If you need to reset your password again, please make a new request here.", "danger")
        return redirect(url_for("pwresetrq_get"))
    
    if pwresetkey[2].replace(tzinfo=pytz.utc) < generated_by:
        flash("Your password reset link expired. Please generate a new one here.", "danger")
        return redirect(url_for("pwresetrq_get"))
    
    return render_template('reset_pw.html', id=key)

@bp.route("/pwreset/<id>", methods=["POST"])
def pwreset_post(id):
    db = get_db()

    password = request.form["password"]
    password2 = request.form["password2"]
    
    if password != password2:
        flash("Your password and password verification didn't match.", "danger")
        return redirect(url_for("pwreset_get", id=id))
    
    if len(password) < 8:
        flash("Your password needs to be at least 8 characters", "danger")
        return redirect(url_for("pwreset_get", id=id))
    
    user_reset = db.execute("SELECT * FROM PWReset WHERE reset_key=?", (id,)).fetchone()
    
    
    try:
        db.execute("UPDATE User SET password=? WHERE id=?", (generate_password_hash(password), user_reset[1]))
        
    except Exception as e:
        flash("Something went wrong", "danger")
        db.rollback()
        return redirect(url_for("index.html"))
    
    db.execute("UPDATE PWReset SET has_activated=? WHERE reset_key=?", (True, id))
   
    flash("Your new password is saved.", "success")
    return redirect(url_for("index.html"))