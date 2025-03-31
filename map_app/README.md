**Video Locations Map - Setup Guide**

This guide will help you set up and run the **Video Locations Map** application, including creating a PostgreSQL database, connecting it to the Flask application, adding data, and verifying that everything works.

* * * * *

**Prerequisites**

Before you begin, ensure you have the following installed:

-   Python (≥ 3.8)
-   PostgreSQL
-   pip (Python package manager)
-   A code editor (e.g., VS Code, PyCharm)

* * * * *

**Step 1: Clone the Repository**

Open a terminal and run:

git clone <https://github.com/eljanabdullazada/sdp_cv>

cd map_app

* * * * *

**Step 2: Create and Activate a Virtual Environment**

python -m venv venv  # Create virtual environment 

source venv/bin/activate  # Activate on macOS/Linux 

venv\Scripts\activate  # Activate on Windows 

* * * * *

**Step 3: Install Dependencies**

pip install -r requirements.txt

This installs Flask, Flask-SQLAlchemy, dotenv, and other necessary packages.

* * * * *

**Step 4: Set Up PostgreSQL Database**

**Open PostgreSQL CLI (psql)**

psql -U postgres

It may ask for a password (default is the one set during PostgreSQL installation).

**Create a Database**

CREATE DATABASE banner_db;

Set the following information for the database:

DATABASE_URL=postgresql://username:password@localhost:5432/banner_db

Exit psql using:

\q

* * * * *

**Step 5: Configure Environment Variables**

Create a .env file in the project root and add:

DATABASE_URL=postgresql://username:password@localhost:5432/banner_db

Make sure to replace myuser and mypassword with your actual PostgreSQL credentials.

* * * * *

**Step 6: Initialize the Database and Add Data**

After creating database run the app using python3 app.py and that will create the relations in the database banner_db.

Once relations are created you can add the data in it using the following query:

INSERT INTO locations (video_id, latitude, longitude, image_link)

VALUES

('video123', 40.4093, 49.8671, 'https://img.freepik.com/premium-vector/billboard-marketing-company-that-says-creative-business-marketing_502601-626.jpg'),

('video456', 40.4100, 49.8700, 'https://static.vecteezy.com/system/resources/previews/002/314/222/non_2x/collection-web-banners-different-sizes-for-mobile-and-social-networks-poster-shopping-ads-and-marketing-material-vector.jpg'),

('video789', 40.4200, 49.8800, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsMaMZOde4hkrEn-6KVQH_p0DfKKdd81q4Zw&s');

* * * * *

**Step 8: Run the Application**

python3 app.py

The app will be available at: **<http://127.0.0.1:5000/>**

* * * * *

**Step 9: Test the App**

1.  Open the browser and go to http://127.0.0.1:5000/.
2.  Enter video123, video456, or video789 as the video ID and search.
3.  The map should load with the marker in Baku.
4.  Click on the marker and scroll down to see the image.