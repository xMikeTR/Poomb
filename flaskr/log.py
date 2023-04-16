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
    return render_template('log/index.html', exercises=exercise)

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
                    'INSERT INTO log (tday, exercise, weight, sets, reps)'
                    'VALUES (?, ?, ?, ?, ?)',
                    (tday, exercises[i], weights[i], sets[i], reps[i])
                )
            db.commit()
            flash('Training')
        return redirect(url_for('log.index'))
        
    return render_template('log/add.html')

        


@bp.route('/update/<string:tid>', methods=('GET', 'POST'))
@login_required
def update(tid):
    
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
                'UPDATE log SET tday = ? exercise = ?, weight = ?, sets = ?, reps = ?'
                'WHERE tid =?,',
                (exercise, weight, sets, reps, g.user['id'])
            )
            db.commit()
            return redirect(url_for('log.index'))
        db = get_db()
        exercise = db.execute("SELECT * FROM  log WHERE TID=?",(tid,)
                          ).fetchone
        
        
        return render_template('log/update.html', exercises=exercise)

@bp.route('/delete/<string:tid>', methods=('GET',))
@login_required
def delete(tid):
    db = get_db()
    db.execute('DELETE FROM log WHERE tid = ?', (tid,))
    db.commit()
    return redirect(url_for('log.index'))

