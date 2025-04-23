from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
from db import create_table
from main import generate_stream, stop_live_detection, detect_banners
from models import db, Location

# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://elcan:yourpassword@localhost:5432/banner_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# File handling configurations
app.config['UPLOAD_FOLDER'] = 'videos'
app.config['DETECTED_FOLDER'] = 'static/detected_banners'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DETECTED_FOLDER'], exist_ok=True)

# Create the table in DB if it doesn't exist
with app.app_context():
    create_table()
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'filename': filename})
    return 'No file uploaded', 400


@app.route('/video/<filename>')
def get_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/video_feed')
def video_feed():
    filename = request.args.get("filename")
    if not filename:
        return "Missing filename", 400
    filename = secure_filename(filename)
    return Response(generate_stream(filename), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    stop_live_detection()
    return jsonify({"stopped": True})

@app.route('/locations')
def locations():
    video_id = request.args.get('video', '')
    return render_template('locations.html', video_id=video_id)



@app.route('/locations_data/<video_id>')
def get_locations_data(video_id):
    locations = Location.query.filter_by(video_name=video_id).all()
    result = [
        {
            "id": loc.id,
            "lat": loc.latitude,
            "lng": loc.longitude,
            "image_link": loc.image_path
        }
        for loc in locations
    ]
    return jsonify(result)


@app.route('/location/<int:location_id>')
def get_location_image(location_id):
    loc = Location.query.get(location_id)
    if not loc:
        return jsonify({"error": "Location not found"}), 404
    return jsonify({"image_link": loc.image_path})


@app.route('/videos', methods=['GET'])
def get_existing_videos():
    videos_folder = "videos"
    videos = [f for f in os.listdir(videos_folder)
              if os.path.isfile(os.path.join(videos_folder, f)) and f.endswith(('.mp4', '.avi', '.mov'))]
    return jsonify(videos)


@app.route('/detect', methods=['POST'])
def run_detection():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    detect_banners(video_path)  # This saves the crops and updates DB
    return jsonify({"status": "Detection complete"})


@app.route('/delete', methods=['POST'])
def delete_video():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(video_path):
        os.remove(video_path)
        return jsonify({'success': f'Video "{filename}" deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
