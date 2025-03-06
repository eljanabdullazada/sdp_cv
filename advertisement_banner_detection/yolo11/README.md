<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>YOLO11 Advertisement Banner Detection</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 2em; }
    pre { background: #f4f4f4; padding: 1em; border-radius: 5px; }
    code { font-family: Consolas, monospace; }
    h1, h2, h3, h4 { margin-top: 1.2em; }
    ul, ol { margin-left: 2em; }
  </style>
</head>
<body>

  <h1 align="center">YOLO11 Advertisement Banner Detection</h1>

  <p align="center">
    <img src="https://img.shields.io/badge/YOLO-Object%20Detection-blue" alt="YOLO Badge">
  </p>

  <h2>Overview</h2>
  <p>
    The <strong>YOLO11 Advertisement Banner Detection</strong> is a Python-based script that utilizes the YOLO model for detecting advertisement banners in videos. The script processes a video file, applies the YOLO object detection model, and identifies banners in the frames. This can be used to analyze videos for specific advertisements.
  </p>

  <h2>How to Run the Script</h2>

  <h3>1. Create and Activate Virtual Environment</h3>
  <h4>On macOS/Linux:</h4>
  <pre><code>python3 -m venv venv
source venv/bin/activate
  </code></pre>

  <h4>On Windows (Command Prompt):</h4>
  <pre><code>python -m venv venv
venv\Scripts\activate
  </code></pre>

  <h4>On Windows (PowerShell):</h4>
  <pre><code>python -m venv venv
.\venv\Scripts\Activate
  </code></pre>

  <h3>2. Install Dependencies</h3>
  <p>Navigate to the project directory and install the required dependencies using pip:</p>
  <pre><code>
pip install -r requirements.txt
  </code></pre>

  <h3>3. Run the Script</h3>
  <p>Once the environment is set up and dependencies are installed, run the following command to start the script:</p>
  <pre><code>python3 fullcode.py
  </code></pre>

  <h3>4. Change Video and Model for Testing</h3>
  <p>To test with a different video or YOLO model, you can modify the following in <code>fullcode.py</code>:</p>

  <h4>Change the Video File</h4>
  <p>Open <code>fullcode.py</code> and locate the following line:</p>
  <pre><code>cap = cv2.VideoCapture('test_video.MP4')
  </code></pre>
  <p>Replace <code>'test_video.MP4'</code> with the name of your desired video file:</p>
  <pre><code>cap = cv2.VideoCapture('new_video.mp4')
  </code></pre>

  <h4>Change the YOLO Model</h4>
  <p>Find this line in <code>fullcode.py</code>:</p>
  <pre><code>model = YOLO("best-242-1600x896.pt")
  </code></pre>
  <p>Replace <code>"best-242-1600x896.pt"</code> with the path to your new YOLO model:</p>
  <pre><code>model = YOLO("new_model.pt")
  </code></pre>

  <h3>5. Controls</h3>
  <ul>
    <li>Press <code>q</code> to quit the video display.</li>
  </ul>

  <h2> How the Script Works</h2>
  <ol>
    <li><strong>Load Video</strong>: The script loads the specified video file for processing.</li>
    <li><strong>YOLO Model Inference</strong>: The script applies the YOLO model to detect objects (banners) in the frames of the video.</li>
    <li><strong>Display Results</strong>: The detected banners are highlighted in each frame, and the video is displayed to the user.</li>
  </ol>



  <h2>Additional Information</h2>
  <ul>
    <li>This project uses a pre-trained YOLO model for banner detection.</li>
  </ul>

</body>
</html>
