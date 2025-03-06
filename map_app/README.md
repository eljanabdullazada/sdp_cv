# Banner Location Viewer

## Overview

The **Banner Location Viewer** is a Flask-based web application that allows users to search for banner locations associated with a specific video ID on a map. The application will display the locations as markers on the map, and users can click on each marker to view the banner image associated with that location.

## How to Run the Application

### 1. Clone the Repository

Clone this repository to your local machine using the following command:
git clone <repository_url>

### 2. Install Dependencies

Navigate to the project directory and install the required dependencies using pip:
cd <project_directory>
pip install -r requirements.txt

### 3. Run the Flask Application

Start the Flask web application by running the following command:
python app.py

### 4. Access the Application

Open your web browser and go to the following URL to access the application:
http://127.0.0.1:5000/

This will display the main page where you can enter a video ID to search for its associated banner locations on the map.

## How the Application Works

1. **Search Video**: Enter the video ID in the search bar to find locations associated with that video.
2. **Map Display**: Once the video ID is found, the application will display markers on the map representing each associated location.
3. **Click to View Image**: You can click on any marker to view the banner image linked to that specific location.

## Database

The SQLite database, `database.db`, is automatically created when you run the application for the first time. It contains dummy location data with coordinates in Azerbaijan, which can be used for testing the functionality of the application.

## Project Structure

- **app.py**: The main Flask application file.
- **templates/**: Contains HTML templates for rendering the pages.
- **static/**: Stores static files such as JavaScript, CSS, and images.
- **database.db**: SQLite database containing location data (coordinates and associated banner images).

## Additional Information

- The application assumes that the video ID you search for has pre-existing location data in the database.
- The location data is provided in the database as dummy values, primarily representing locations in Azerbaijan.
