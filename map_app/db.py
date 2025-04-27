import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    result = urlparse(db_url)
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS banners (
            id SERIAL PRIMARY KEY,
            video_name TEXT,
            image_path TEXT,
            latitude FLOAT,
            longitude FLOAT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_banner_data(image_path, latitude, longitude, video_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO banners (image_path, latitude, longitude, video_name)
        VALUES (%s, %s, %s, %s)
    ''', (image_path, latitude, longitude, video_name))
    conn.commit()
    cur.close()
    conn.close()

def get_all_banner_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, video_name, image_path, latitude, longitude FROM banners;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'video_name': row[1], 'image_path': row[2], 'latitude': row[3], 'longitude': row[4]} for row in rows]
