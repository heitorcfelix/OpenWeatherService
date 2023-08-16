from app.extensions import db

class Weather(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    json_data = db.Column(db.JSON)
