from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'banners'
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(255), nullable=False)  # Renamed from video_id
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
