from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
from db import create_table
from main import generate_detection_stream, stop_live_detection

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
app.config['DETECTED_FOLDER'] = 'static/detected_banners'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DETECTED_FOLDER'], exist_ok=True)

# Create the table in DB if it doesn't exist
create_table()

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
        return "No video filename provided", 400
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(generate_detection_stream(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    stop_live_detection()
    return jsonify({"stopped": True})

@app.route('/locations')
def locations():
    video_id = request.args.get('video', '')
    return render_template('locations.html', video_id=video_id)

@app.route('/videos', methods=['GET'])
def get_existing_videos():
    videos_folder = "videos"
    videos = [f for f in os.listdir(videos_folder)
              if os.path.isfile(os.path.join(videos_folder, f)) and f.endswith(('.mp4', '.avi', '.mov'))]
    return jsonify(videos)

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
