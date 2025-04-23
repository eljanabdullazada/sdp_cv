let uploadedVideos = JSON.parse(localStorage.getItem("uploadedVideos")) || [];
let selectedVideo = "";

function updateFileName() {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");
    fileLabel.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "Choose a file";
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

function selectVideo() {
    const dropdown = document.getElementById("videoList");
    selectedVideo = dropdown.value;
    localStorage.setItem("selectedVideo", selectedVideo);
}

function uploadVideo() {
    const fileInput = document.getElementById("fileInput");
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

    // Start the MJPEG live stream
    const stream = document.getElementById("videoStream");
    stream.src = `/video_feed?filename=${encodeURIComponent(selectedVideo)}`;
    document.getElementById("streamContainer").style.display = "block";

    // Hide regular video player
    document.getElementById("videoPlayer").hidden = true;

    fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    })
    .catch(() => alert("Detection failed!"))
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

function showLocations() {
    if (!selectedVideo) return alert("No video selected!");
    window.location.href = `/locations?video=${encodeURIComponent(selectedVideo)}`;
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
