import os
import requests
import time
import httpx
import asyncio
from app.main import bp
from app.extensions import db
from app.models.weather import Weather
from app.main.city_codes import city_codes
from flask import request, jsonify, make_response
from datetime import datetime

appID = os.environ.get('APPID')
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
        if not weather:
            return make_response(jsonify({'message': 'User not found'}), 404)
        else:
            weather = weather[0].json_data
            percentage = round(len(weather) / len(city_codes) * 100, 2)
        return make_response(jsonify({'user_id': user_id,'percentage': str(percentage)+'%'}), 200)
    if request.method == 'POST':
        try:
            limit = 60  # Number of requests allowed
            interval = 60  # Time interval in seconds

            user_id = request.form.get('user_id')
            datetime_now = datetime.now()
            for city in city_codes:
                rate_limit(limit, interval)
                asyncio.run(run_city(user_id, datetime_now, city))
            weather = Weather.query.filter_by(user_id=user_id).all()[0]
            return make_response({'user_id': weather.user_id, 'timestamp': weather.date_time, 'json_data': weather.json_data}, 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


async def run_city(user_id, timestamp, city_id):
    uri = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={appID}&units=metric'
    current_time = time.time()
    request_counts.append(current_time)
    async with httpx.AsyncClient() as client:
        response = await client.get(uri)
    result = {response.json()['id']: {'temperature': response.json()['main']['temp'], 'humidity': response.json()['main']['humidity']}}
    if response.status_code == requests.codes.ok:
        current_user = Weather.query.filter_by(user_id=user_id).all()
        if current_user:
            # get the json of the current user in the DB and update with a new key using the city id
            current_user_json = current_user[0].json_data
            current_user_json[city_id] = result[city_id]
            db.session.query(Weather).filter_by(user_id=user_id).update(dict(json_data=current_user_json))
            db.session.commit()
        else:
            # create a new user in the DB
            print(result)
            weather = Weather(user_id=user_id, date_time=timestamp, json_data=result)
            db.session.add(weather)
            db.session.commit()    
