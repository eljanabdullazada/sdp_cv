import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='banner_db',
        user='elcan',
        password='yourpassword',
        host='localhost',
        port='5432'
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS banners (
            id SERIAL PRIMARY KEY,
            image_path TEXT,
            latitude FLOAT,
            longitude FLOAT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_banner_data(image_path, latitude, longitude):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO banners (image_path, latitude, longitude) VALUES (%s, %s, %s);',
                (image_path, latitude, longitude))
    conn.commit()
    cur.close()
    conn.close()

def get_all_banner_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT image_path, latitude, longitude FROM banners;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'image': row[0], 'lat': row[1], 'lon': row[2]} for row in rows]
