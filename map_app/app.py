import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    """Initializes the database with a table and dummy data if it doesn't exist."""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # Create the locations table
        c.execute('''
            CREATE TABLE locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT,
                latitude REAL,
                longitude REAL,
                image_link TEXT
            )
        ''')
        # Dummy data with Azerbaijani coordinates and the provided image links.
        dummy_data = [
            # Video1: Example coordinates in Baku area
            ('video1', 40.4093, 49.8671, 'https://www.shutterstock.com/image-photo/blank-billboard-on-side-road-260nw-251619454.jpg'),
            ('video1', 40.6828, 49.1234, 'https://img.freepik.com/free-photo/billboard-blank-outdoor-advertising-poster-blank-billboard-night-time-advertisement-street-light_1127-3066.jpg'),
            # Video2: Example coordinates in other parts of Azerbaijan
            ('video2', 40.5897, 49.6686, 'https://mir-s3-cdn-cf.behance.net/projects/404/59c848124809679.Y3JvcCwxMjIwLDk1NCwxMjYsMTUyMA.jpg'),
            ('video2', 38.7550, 48.8486, 'https://mir-s3-cdn-cf.behance.net/projects/404/337a51215919781.Y3JvcCw2NDYsNTA1LDgwLDYy.jpg')
        ]
        c.executemany('INSERT INTO locations (video_id, latitude, longitude, image_link) VALUES (?, ?, ?, ?)', dummy_data)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    video_id = request.args.get('video_id')
    locations = []
    if video_id:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id, latitude, longitude, image_link FROM locations WHERE video_id = ?", (video_id,))
        rows = c.fetchall()
        for row in rows:
            locations.append({
                'id': row[0],
                'lat': row[1],
                'lng': row[2],
                'image_link': row[3]
            })
        conn.close()
    return render_template('index.html', locations=locations, video_id=video_id)

@app.route('/location/<int:location_id>')
def get_location(location_id):
    """API endpoint to fetch the image link for a given location id."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT image_link FROM locations WHERE id = ?", (location_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({'image_link': row[0]})
    else:
        return jsonify({'error': 'Location not found'}), 404

if __name__ == '__main__':
    init_db()  # Create the database and dummy data if needed.
    app.run(debug=True)
