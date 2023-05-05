from flask import Flask
from flask_restx import Api, Resource
from flaskr.db import get_db
from datetime import datetime

app = Flask(__name__)
api = Api(app)

from log import performance

@api.route('/trdata')
class LogData(Resource):
    def get(self):
        response = performance()
        db = get_db()
        tperformance = db.execute('SELECT * FROM log').fetchall()

        data = []
        for item in tperformance:
            
            tday_obj = datetime.strptime(item['tday'], '%d-%m-%Y')
            tday_formatted = tday_obj.strftime('%d-%m-%Y')
            
            data.append({
                'tday': item['tday'],
                'exercise': item['exercise'],
                'weight': item['weight'],
                'sets': item['sets'],
                'reps': item['reps']
            })
        print(data)
        
        return {'data': response}
