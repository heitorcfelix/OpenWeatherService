# OpenWeatherService
### Service that collects data from an Open Weather API and stores it as JSON data in a PostgreSQL DB

### Requirements
- Docker >= 24.0.5

### How to Build

- Create an [OpenWeather Account](https://openweathermap.org/) and Generate a API Key
- Put the key and all sensitive values in secrets folder
    - [AppID](./secrets/appid.env)
    - [DB URI](./secrets/database_url.env)
    - [DB USER](./secrets/database_user.env)
    - [DB PASSWORD](./secrets/database_password.env)

- Run
```sh
docker compose up -d
```

### How to Run
Receives a user defined ID, collect weather data from OpenWeather API and store:
- The user defined ID (needs to be unique for each request)
- Datetime of request
- JSON data with:
    - City ID
    - Temperature in Celsius
    - Humidity
```sh
curl -XPOST -H 'Content-Type: application/x-www-form-urlencoded' -d 'user_id=1' 'http://localhost:8000'
```

Receives the user defined ID, returns with the percentage of the POST progress ID (collected cities completed) until the current moment.
```sh
curl -XGET 'http://localhost:8000?user_id=1'
```

### How to Test
```sh
python test/test_app.py
```
The test will try all 161 Appendix A cities, it should take considerable time. To change the list of cities, change in [city_codes](./app/main/city_codes.py).