from flask import Blueprint, g
from flask_restx import Api, Resource
from poomb.db import get_db
from datetime import datetime

bp = Blueprint('api', __name__)
api = Api(bp)

@api.route('/trdata')
class LogData(Resource):
    def get(self):
        db = get_db()
        tperformance = db.execute('SELECT * FROM log WHERE lifter_id = ?', [g.user['id']]).fetchall()

        data = {
            'labels': [],
            'datasets': []
        }

        for item in tperformance:
            tday_obj = datetime.strptime(item['tday'], '%d-%m-%Y')
            tday_formatted = tday_obj.strftime('%d-%m-%Y')

            # Check if training day label exists in data
            if tday_formatted not in data['labels']:
                data['labels'].append(tday_formatted)

            # Check if exercise dataset exists in data
            exercise_dataset = next(
                (dataset for dataset in data['datasets'] if dataset['label'] == item['exercise']),
                None
            )

            # If exercise dataset doesn't exist, create a new one
            if exercise_dataset is None:
                exercise_dataset = {
                    'label': item['exercise'],
                    'data': []
                }
                data['datasets'].append(exercise_dataset)

            # Add weight value to exercise dataset
            exercise_dataset['data'].append(item['weight'])

        return data
