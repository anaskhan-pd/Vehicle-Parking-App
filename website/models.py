from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    pin_code = db.Column(db.String, nullable = False)
    price_per_hour = db.Column(db.Integer, nullable = False)
    max_spots = db.Column(db.Integer, nullable = False)


class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    lot_id = db.Column(db.Integer,db.ForeignKey('parking_lot.id'),nullable = False)
    status = db.Column(db.String,nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable = False)
    in_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    out_time = db.Column(db.DateTime, nullable = True)
    cost = db.Column(db.Integer, nullable = True)
    spot = db.relationship('ParkingSpot')

    






