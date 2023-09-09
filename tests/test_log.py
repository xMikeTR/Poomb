import os
import pytest
from poomb.db import get_db
from poomb.log import performance
import requests
from unittest.mock import patch, Mock
from poomb.log import pwresetrq_post
import datetime
import pytz






def test_index(app):
    c = app.test_client()
    response = c.get('http://127.0.0.1:5000/')
    assert response.status_code == 302
    
    assert b'/auth/login' in response.data

def test_index_show_recent_training(client, app, auth, mocker):
    auth.login()
    c = app.test_client()
    server = c.get('http://127.0.0.1:5000/')
    with app.app_context():
        db = get_db()
        response1 = db.execute('SELECT MAX(tday) FROM log').fetchone()[0]
        response2 = db.execute(
        'SELECT * FROM log WHERE tday = ? AND lifter_id = ?',
        (response1, 1)
    ).fetchall()

        
    assert response1, response2 in server


@pytest.mark.parametrize('path', (
    '/performance',
    '/add',
    '/update/1',
    
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"





def test_create(client, auth, app):
    auth.login()
    assert client.get('/add').status_code == 200
    client.post('/add', data={
        'tday': '2023-01-01',
        'exercise': 'Squat',
        'weight': '100',
        'sets': '3',
        'reps': '8'
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(tid) FROM log').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/update/1').status_code == 200
    client.post('/update/1', data={
        'exercise': 'updated',
        'weight': '150',
        'sets': '4',
        'reps': '10'
    })

    with app.app_context():
        db = get_db()
        exercise = db.execute('SELECT * FROM log WHERE tid = 1').fetchone()
        assert exercise['exercise'] == 'updated'


@pytest.mark.parametrize('path', (
    
    '/update/1',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    client.post(path, data={
        'tday': '2018-01-01',
        'exercise': '',
        'weight': '',
        'sets': '',
        'reps': ''
    })
    with pytest.raises(ValueError, match=r'fill out this field'):
        raise ValueError('Please fill out this field.')


def test_delete(client, auth, app):
    auth.login()
    client.get('/delete/1')
    

    with app.app_context():
        db = get_db()
        exercise = db.execute('SELECT * FROM log WHERE tid = 1').fetchone()
        assert exercise is None



def test_performance_shows(client, auth, app, mocker):
    with app.app_context():
        
        
        auth.login()
        response = client.get('/performance')
        assert response.status_code == 200

@pytest.mark.parametrize('path', (
    
    '/performance',
))

def test_training_shows(client, auth, app, path):
    with app.app_context():
        auth.login()
        response = client.post(path, '2023-04-04')
        assert response.status_code == 302

#@pytest.mark.parametrize('path', (
   # 
    #'/',
#))

#def test_index_apis(client, auth, app, path):
    #with app.app_context():
     # url = 'https://www.openpowerlifting.org/mlist/all-argentina/2023'
     # data = {
      #    'Federation':'ARPL',
        #  'Date': '2023-06-15',
        #  'Location':'Argentina',
        #  'Competition':'Nacionals'
          
      #}
      #response = requests.post(url, data=data)
      #assert response.status_code == 201


    
#def test_chartjs(auth, app, client):
 #   with app.app_context():
  #      auth.login()
   #     data = {
    #        'Exercise':'Squat',
     #       'Weight':'100',
      #      'Sets':'5',
       #     'Reps':'5'
        #}
        #path = 'http://127.0.0.1:5000/performance'
        
       # response = requests.post(path, data)
        
    #assert response.status_code == 201

@pytest.mark.parametrize('path', (
    
    '/pwresetrq',
))


def test_pwreset(client, path, app):
    with app.app_context():
        response = client.get(path)
        assert response.status_code == 200

@pytest.mark.parametrize('path', (
    
    '/pwresetrq',
))


def test_pwresetrq_post(client,path, app):
    # Mock the database interaction
    
            
            # Simulate a POST request to the pwresetrq route with a valid email
            with app.app_context():
                response = client.post('/pwresetrq', data={'email': 'test@test.com'}, follow_redirects=True)

            # Check the response status code
                assert response.status_code == 200




def test_pwreset_get(client, app):
    with app.app_context():
        response = client.post('/pwreset/1', 'resetkey')
        assert response.status_code == 200