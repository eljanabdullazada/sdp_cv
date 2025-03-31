from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from db import db, Location

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    video_id = request.args.get('video_id')
    return render_template('index.html', video_id=video_id)

@app.route('/locations_data/<video_id>')
def locations_data(video_id):
    locations = Location.query.filter_by(video_id=video_id).all()
    locations_list = [{
        'id': loc.id,
        'lat': loc.latitude,
        'lng': loc.longitude,
        'image_link': loc.image_link
    } for loc in locations]
    return jsonify(locations_list)

@app.route('/location/<int:location_id>')
def get_location(location_id):
    location = Location.query.get(location_id)
    if location:
        return jsonify({'image_link': location.image_link})
    return jsonify({'error': 'Location not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
