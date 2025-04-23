let uploadedVideos = JSON.parse(localStorage.getItem("uploadedVideos")) || [];
let selectedVideo = "";

// Update file name when a file is chosen for upload
function updateFileName() {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");

    // If there's a file selected for upload, show the file name
    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
    } else {
        // If no file is selected, reset label to "Choose a video"
        fileLabel.textContent = "Choose a video";
    }
}


function updateVideoList() {
    const dropdown = document.getElementById("videoList");
    dropdown.innerHTML = "";
    uploadedVideos.forEach(filename => {
        const option = document.createElement("option");
        option.value = filename;
        option.textContent = filename;
        if (filename === selectedVideo) option.selected = true;
        dropdown.appendChild(option);
    });
}

// Update the file input label only when a new file is chosen
function selectVideo() {
    const dropdown = document.getElementById("videoList");
    selectedVideo = dropdown.value;
    localStorage.setItem("selectedVideo", selectedVideo);

    // Reset file label text back to default when a video is selected from the dropdown
    document.getElementById("fileLabel").textContent = "Choose a video";

    // Optionally reset file input value so the file selection doesn't appear in the input
    document.getElementById("fileInput").value = '';
}


function uploadVideo() {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");
    const file = fileInput.files[0];

    if (!file) return alert("No file selected.");

    const formData = new FormData();
    formData.append("video", file);

    fetch("/upload", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            uploadedVideos.push(data.filename);
            localStorage.setItem("uploadedVideos", JSON.stringify(uploadedVideos));
            selectedVideo = data.filename;
            localStorage.setItem("selectedVideo", selectedVideo);
            updateVideoList();
            alert("Upload successful!");

            fileInput.value = "";
            fileLabel.textContent = "Choose a video";
        })
        .catch(err => {
            alert("Upload failed.");
            console.error("Upload error:", err);
        });
}


function playVideo() {
    if (!selectedVideo) return alert("Select a video first!");
    stopDetection();  // Hide stream if visible
    const video = document.getElementById("videoPlayer");
    video.src = `/video/${selectedVideo}`;
    video.hidden = false;
    video.play();
}

function stopVideo() {
    const video = document.getElementById("videoPlayer");
    video.pause();
    video.hidden = true;
}

function detectBanners() {
    if (!selectedVideo) return alert("No video selected!");

    const detectBtn = document.querySelector("button[onclick='detectBanners()']");
    detectBtn.disabled = true;
    detectBtn.textContent = "Detecting...";

    // Show detection stream and hide video player
    const stream = document.getElementById("videoStream");
    stream.src = `/video_feed?filename=${encodeURIComponent(selectedVideo)}`;
    document.getElementById("streamContainer").style.display = "block";
    document.getElementById("videoPlayer").hidden = true;

    fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    })
    .then(res => {
        if (!res.ok) throw new Error("Detection failed");
        return res.json();
    })
    .then(data => {
        console.log("Detection started successfully:", data);
    })
    .catch((err) => {
        alert("Detection failed!");
        console.error("Detection error:", err);
        document.getElementById("streamContainer").style.display = "none";
        stream.src = "";
    })
    .finally(() => {
        detectBtn.disabled = false;
        detectBtn.textContent = "Detect Banners";
    });
}



function stopDetection() {
    fetch('/stop_detection', { method: 'POST' })
        .then(() => {
            document.getElementById("streamContainer").style.display = "none";
            document.getElementById("videoStream").src = ""; // Stop stream
        })
        .catch(err => console.error("Error stopping detection:", err));
}

function showLocationsPage() {
    const videoSelect = document.getElementById("videoList");
    const selectedVideo = videoSelect.value;
    if (!selectedVideo) {
        alert("Please select a video first.");
        return;
    }
    window.location.href = `/locations?video=${selectedVideo}`;
}


function deleteVideo() {
    if (!selectedVideo) return alert("No video selected!");

    const confirmDelete = confirm(`Are you sure you want to delete "${selectedVideo}"?`);
    if (!confirmDelete) return;

    fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedVideos = uploadedVideos.filter(v => v !== selectedVideo);
            selectedVideo = uploadedVideos.length ? uploadedVideos[0] : "";
            localStorage.setItem("uploadedVideos", JSON.stringify(uploadedVideos));
            localStorage.setItem("selectedVideo", selectedVideo);
            updateVideoList();
            stopVideo();
            stopDetection();
            alert("Video deleted.");
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(err => {
        alert("Error deleting video.");
        console.error("Delete error:", err);
    });
}

window.addEventListener("load", () => {
    fetch('/videos')
        .then(res => res.json())
        .then(existingVideos => {
            uploadedVideos = existingVideos;
            selectedVideo = localStorage.getItem("selectedVideo") || "";
            updateVideoList();

            if (selectedVideo && uploadedVideos.includes(selectedVideo)) {
                const video = document.getElementById("videoPlayer");
                video.src = `/video/${selectedVideo}`;
            }
        })
        .catch(err => {
            console.error('Error fetching videos from server:', err);
        });
});
