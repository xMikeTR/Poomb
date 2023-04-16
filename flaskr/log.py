from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import datetime

bp = Blueprint('log', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    exercise = db.execute(
        'SELECT * FROM log ORDER BY tday DESC'
    ).fetchall()
    return render_template('log/index.html', exercise=exercise)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        tday = request.form['tday']
        exercises = request.form.getlist('exercise')
        weights = request.form.getlist('weight')
        sets = request.form.getlist('sets')
        reps = request.form.getlist('reps')
        error = None
        
        for i in range(len(exercises)):
            if not exercises[i]:
                error = 'Exercise is required for all entries.'
                break
        
        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            for i in range(len(exercises)):
                db.execute(
                    'INSERT INTO log (tday, exercise, weight, sets, reps, creator_id)'
                    'VALUES (?, ?, ?, ?, ?, ?)',
                    (tday, exercises[i], weights[i], sets[i], reps[i], g.user['id'])
                )
            db.commit()
            flash('Training added')
        return redirect(url_for('log.index'))
        
    return render_template('log/add.html')

        
def get_log(tday, check_user=True):
    print("tday:", tday)
    log = get_db().execute(
        'SELECT id, tday, exercise, weight, sets, reps, creator_id'
        ' FROM log '
        ' WHERE tday = ?',
        (tday,)
    ).fetchone()
    print("log:",log)
    
    if log is None:
        abort(404,f"Log id {tday} doesn't exist.")
        
    if check_user and g.user['id'] == False:
        abort(403)
    print("g.user['id']:", g.user['id'])
    return log

@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update(tday):
    print(tday)
    log = get_log(tday, check_user=True)
    
    if request.method == 'POST':
        tday = request.form['tday']
        exercise = request.form['exercise']
        weight = request.form['weight']
        sets = request.form['sets']
        reps = request.form['reps']
        error = None
        
        if not tday:
            error = 'Training day is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE log SET exercise = ?, weight = ?, sets = ?, reps = ?'
                'WHERE tday = ? AND creator_id = ?',
                (exercise, weight, sets, reps, g.user['id'])
            )
            db.commit()
            return redirect(url_for('log.index'))
        
        return render_template('log/update.html', logs = log, tdays=tday)

@bp.route('/<int:tday>/delete', methods=('POST',))
@login_required
def delete(tday):
    get_log(tday)
    db = get_db()
    db.execute('DELETE FROM log WHERE tday = ?', (tday,))
    db.commit()
    return redirect(url_for('log.index'))

