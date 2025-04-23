from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os, subprocess
from db import create_table

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
    """Serve the original uploaded video"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/detect', methods=['POST'])
def detect():
    video_filename = request.json.get('filename')
    if not video_filename:
        return jsonify({'error': 'No filename provided'}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)

    try:
        # Run detection script as a subprocess to allow cv2.imshow
        subprocess.Popen(['python', 'live_detect.py', video_path])
        return jsonify({"message": "Detection started in a new window."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/processed/<filename>')
# def get_processed_video(filename):
#     """Serve the processed video with banners detected"""
#     return send_from_directory(app.config['DETECTED_FOLDER'], filename)


@app.route('/locations')
def locations():
    video_id = request.args.get('video', '')
    return render_template('locations.html', video_id=video_id)

@app.route('/videos', methods=['GET'])
def get_existing_videos():
    """Return a list of all videos already uploaded to the server"""
    videos_folder = "videos"
    videos = [f for f in os.listdir(videos_folder) if os.path.isfile(os.path.join(videos_folder, f)) and f.endswith(('.mp4', '.avi', '.mov'))]
    return jsonify(videos)


@app.route('/delete', methods=['POST'])
def delete_video():
    """Delete the video from the server"""
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists
    if os.path.exists(video_path):
        os.remove(video_path)  # Remove the file from the server
        return jsonify({'success': f'Video "{filename}" deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
