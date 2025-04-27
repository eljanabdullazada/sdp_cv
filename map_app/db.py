import psycopg2

def get_connection():
    # Establish connection to PostgreSQL
    return psycopg2.connect(
        dbname='vagif',
        user='elcan',
        password='yourpassword',  # Change to your password
        host='localhost',
        port='5432'
    )

def create_table():
    # Create banners table with video_name column
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS banners (
            id SERIAL PRIMARY KEY,
            video_name TEXT,  -- Added the video_name column
            image_path TEXT,
            latitude FLOAT,
            longitude FLOAT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_banner_data(image_path, latitude, longitude, video_name):
    # Insert banner data including video_name into PostgreSQL database
    conn = get_connection()
    cur = conn.cursor()

    # Insert query with the new column 'video_name'
    cur.execute('''
        INSERT INTO banners (image_path, latitude, longitude, video_name)
        VALUES (%s, %s, %s, %s)
    ''', (image_path, latitude, longitude, video_name))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

def get_all_banner_data():
    # Fetch all banner data from the database, ensuring the correct column order
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, video_name, image_path, latitude, longitude FROM banners;')  # Correct order of columns
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'video_name': row[1], 'image_path': row[2], 'latitude': row[3], 'longitude': row[4]} for row in rows]
