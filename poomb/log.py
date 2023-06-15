from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from poomb.auth import login_required
from poomb.db import get_db
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
#Sfrom poomb.emails import send_email
import plotly.graph_objs as go
import nest_asyncio
import json
import asyncio
from flask import jsonify


nest_asyncio.apply()


bp = Blueprint('log', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    max_tday = db.execute('SELECT MAX(tday) FROM log').fetchone()[0]
    exercises = db.execute(
        'SELECT * FROM log WHERE tday = ?',
        (max_tday,)
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
                    'INSERT INTO log (tday, exercise, weight, sets, reps)'
                    'VALUES (?, ?, ?, ?, ?)',
                    (tday, exercise[i], weights[i], sets[i], reps[i])
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
            tperformance = db.execute('SELECT * FROM log WHERE tday = ?', (tdate_formatted,)).fetchall()
        except ValueError:
            flash("No valid date")
        else:
            if len(tperformance) == 0:
             flash("No data for selected date")
        
            return render_template('log/performance.html',tperformance=tperformance, tdate=tdate)
    db = get_db()
    tperformance = db.execute('SELECT * FROM log LIMIT 10').fetchall()
    return render_template('log/performance.html', tperformance=tperformance)

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST':
        db = get_db()

        email = request.form.get('email')
        check_email = db.execute('SELECT * FROM users WHERE email=?', email)
        if email in check_email:
            send_email(email)

        return redirect(url_for('log/login.html'))