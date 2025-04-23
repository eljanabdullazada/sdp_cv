from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from db import create_table, insert_banner_data, get_all_banner_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
app.config['DETECTED_FOLDER'] = 'static/detected_banners'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DETECTED_FOLDER'], exist_ok=True)
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

@app.route('/detect', methods=['POST'])
def detect():
    from main import detect_banners
    video_filename = request.json['filename']
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    detect_banners(video_path)
    return 'Detection complete'

@app.route('/locations')
def locations():
    video_id = request.args.get('video', '')
    return render_template('locations.html', video_id=video_id)


if __name__ == '__main__':
    app.run(debug=True)
