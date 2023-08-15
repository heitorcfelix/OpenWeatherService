import requests
import time
from . import bp
from app.extensions import db
from app.models.weather import Weather
from app.main.city_codes import city_codes
from flask import request, jsonify, make_response
from datetime import datetime
import httpx
import asyncio

appID = ''
request_counts = []

def rate_limit(limit, interval):
    current_time = time.time()
    while request_counts and request_counts[0] < current_time - interval:
        request_counts.pop(0)
    if len(request_counts) > limit:
        time_to_wait = request_counts[0] + interval - current_time
        time.sleep(time_to_wait)

@bp.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        weather = Weather.query.filter_by(user_id=user_id).all()
        percentage = round(len(weather) / len(city_codes) * 100, 2)
        return make_response(jsonify({'percentage': percentage}), 200)
    if request.method == 'POST':
        try:
            limit = 60  # Number of requests allowed
            interval = 60  # Time interval in seconds

            user_id = request.form.get('user_id')
            datetime_now = datetime.now()
            for city in city_codes:
                rate_limit(limit, interval)
                asyncio.run(run_city(user_id, datetime_now, city))
            return make_response(jsonify({'message': 'OK'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


async def run_city(user_id, timestamp, city_id):
    uri = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={appID}&units=metric'
    current_time = time.time()
    request_counts.append(current_time)
    async with httpx.AsyncClient() as client:
        response = await client.get(uri)
    if response.status_code == requests.codes.ok:
        result = {}
        result['cytyID'] = response.json()['id']
        result['temperature'] = response.json()['main']['temp']
        result['humidity'] = response.json()['main']['humidity']

        weather = Weather(user_id=user_id, date_time=datetime.now(), json_data=result)
        db.session.add(weather)
        db.session.commit()
