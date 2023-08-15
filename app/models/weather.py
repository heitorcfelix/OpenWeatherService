from app.extensions import db

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)
    json_data = db.Column(db.JSON)
